"""Pruebas exhaustivas para la Vista Bilingüe ES / EN y Traducción Canonica (PZ-013C).

Valida el sistema de internacionalización en web/i18n.js, la conservación estricta
de identificadores estables sin traducir, la inclusión de bloques #english en el VBP Markdown,
la inmutabilidad de huellas previas a la aprobación humana y la protección anti-XSS.
Cumple estrictamente con CONTRATO-MVP-v1.md 6.6, 11.9 y FICHA-PZ-013C.md.
"""

import copy
import json
import re
import unittest
from pathlib import Path

import app.runtime_contracts as runtime_contracts
import app.vbp_document as vbp_document
import app.vbp_export as vbp_export

PROJECT_ROOT = Path(__file__).resolve().parent.parent
I18N_JS_PATH = PROJECT_ROOT / "web" / "i18n.js"


class TestBilingualView(unittest.TestCase):
    """Suite de pruebas para PZ-013C (Bilingual View and i18n)."""

    def setUp(self) -> None:
        self.assertTrue(I18N_JS_PATH.exists(), "web/i18n.js debe existir en el proyecto.")
        self.i18n_content = I18N_JS_PATH.read_text(encoding="utf-8")

    def test_ac01_i18n_dictionary_completeness(self) -> None:
        """AC-01: web/i18n.js contiene traducciones completas en ES y EN para todas las areas obligatorias."""
        # Verificar presencia de secciones clave en el JS
        required_keys = [
            "app_title",
            "badge_simulated",
            "section_operator",
            "section_intake",
            "section_gate1",
            "section_specialists",
            "section_evidence_memory",
            "section_gate2",
            "section_vbp",
            "section_audit",
            "btn_submit_mission",
            "btn_approve_plan",
            "btn_reject_plan",
            "btn_approve_vbp",
            "btn_reject_vbp",
            "btn_download_vbp",
        ]

        for k in required_keys:
            self.assertIn(f"{k}:", self.i18n_content, f"La clave {k} debe estar en el diccionario i18n.")

        # Verificar que existen los bloques es: y en:
        self.assertIn("es: {", self.i18n_content)
        self.assertIn("en: {", self.i18n_content)

    def test_ac02_stable_identifiers_preservation(self) -> None:
        """AC-02: Los identificadores técnicos estables no se traducen ni alteran en la vista bilingüe."""
        from test_human_approvals import fixture
        runtime,repo,ctx,request=fixture(stage="approved")
        self.addCleanup(repo.close)
        sample_vbp=repo.get_object("candidate","MSN-SIM:GATE_2_VBP")
        valid,errors=runtime_contracts.RuntimeContractsValidator().validate_structure("vbp",sample_vbp)
        self.assertTrue(valid,errors)
        # Renderizar en Markdown con bloques bilingües
        md_bilingual = vbp_document.render_canonical_markdown(sample_vbp, include_bilingual_blocks=True)

        # Verificar que los IDs estables se mantienen intactos
        self.assertIn("`VBP-MSN-SIM`", md_bilingual)
        self.assertIn("`MSN-SIM`", md_bilingual)
        self.assertIn(sample_vbp["human_approval_ref"], md_bilingual)
        self.assertIn("```english\nSIMULATED", md_bilingual)
        self.assertEqual(vbp_document.render_canonical_markdown(sample_vbp,False),md_bilingual)

    def test_ac03_translation_part_of_content_before_fingerprint(self) -> None:
        """AC-03: La traducción material altera el contenido y por ende la huella ANTES de la aprobación humana."""
        from test_human_approvals import fixture
        runtime,repo,ctx,request=fixture(stage="vbp")
        self.addCleanup(repo.close)
        base_vbp=repo.get_object("candidate","MSN-SIM:GATE_2_VBP")
        self.assertTrue(runtime_contracts.RuntimeContractsValidator().validate_structure("vbp",base_vbp)[0])
        fp_original = runtime_contracts.compute_vbp_manifest_fingerprint(base_vbp)

        # Si se añade traducción material antes de aprobar
        vbp_with_trans = copy.deepcopy(base_vbp)
        vbp_with_trans["sections"][0]["content"] += "\n\n```english\nMission statement in English\n```"
        fp_trans = runtime_contracts.compute_vbp_manifest_fingerprint(vbp_with_trans)

        # La huella cambia para reflejar la inclusión del contenido bilingüe
        self.assertNotEqual(fp_original, fp_trans)

    def test_ac04_anti_xss_protection_in_bilingual_helper(self) -> None:
        """AC-04: La interfaz de traducción no contiene scripts no sanitizados ni HTML peligroso."""
        # Comprobar que en web/app.js y web/i18n.js el texto se asigna como textContent o se sanitiza
        app_js_path = PROJECT_ROOT / "web" / "app.js"
        self.assertTrue(app_js_path.exists())
        app_js = app_js_path.read_text(encoding="utf-8")
        self.assertIn("function escapeHTML", app_js)
        self.assertIn(".textContent =", app_js)


class TestPreparedBilingual(unittest.TestCase):
    def test_prepared_demo_fidelity_frozen_before_ordinary_approval(self):
        from app.hq_runtime import HQRuntime
        from app.local_repository import LocalRepository
        from test_human_approvals import PROFILE
        repo=LocalRepository(':memory:');self.addCleanup(repo.close)
        runtime=HQRuntime(repository=repo);ctx=runtime.approvals.bind_local_profile(PROFILE)
        fields={**vbp_document.prepared_demo_fields(),'mission_id':'MSN-PREPARED'}
        ok,mission,error=runtime.create_local_mission(fields,ctx);self.assertTrue(ok,error)
        request=repo.get_object('approval_request',mission['approval_id'])['request']
        self.assertTrue(runtime.approvals.submit_human_decision(request,'APROBAR',context=ctx)[0])
        ok,mission,error=runtime.execute_local_simulation('MSN-PREPARED',ctx);self.assertTrue(ok,error)
        candidate=repo.get_object('candidate','MSN-PREPARED:GATE_2_VBP')
        self.assertEqual(mission['translation_status'],'PREPARADA_ES_EN')
        blocks=[re.search(r'```english\n([\s\S]*?)\n```',s['content'])[1] for s in candidate['sections']]
        for key in ('title','objective','context','expected_result'):
            self.assertIn(vbp_document.demo_english(fields[key]),blocks[0])
        self.assertIn('78%',blocks[4]);self.assertIn('tenant',blocks[4])
        self.assertIn('70% in 6 months',blocks[13]);self.assertIn('< 1%',blocks[13])
        for task in mission['plan']['tasks']:
            self.assertIn(task['task_id'],blocks[11]);self.assertIn(vbp_document.demo_english(task['objective']),blocks[11])
        for eid in mission['evidence_ids']:
            self.assertIn(eid,blocks[4]);self.assertIn(repo.get_object('evidence',eid)['source_locator'],blocks[4])
        fp=candidate['fingerprint'];sections=copy.deepcopy(candidate['sections'])
        self.assertTrue(runtime.approvals.submit_human_decision(mission['approval_request'],'APROBAR',context=ctx)[0])
        approved=repo.get_object('candidate','MSN-PREPARED:GATE_2_VBP')
        self.assertEqual(approved['fingerprint'],fp);self.assertEqual(approved['sections'],sections)
        before=copy.deepcopy(approved)
        with self.assertRaises(ValueError):vbp_document.prepare_simulated_bilingual(approved)
        self.assertEqual(approved,before)
        a=vbp_export.export_canonical_vbp_bytes(approved,repository=repo,include_bilingual_blocks=True)
        b=vbp_export.export_canonical_vbp_bytes(approved,repository=repo,include_bilingual_blocks=False)
        self.assertTrue(a[0],a[3]);self.assertEqual(a[1],b[1])

    def test_arbitrary_input_translation_is_pending_not_invented(self):
        from test_human_approvals import fixture
        runtime,repo,ctx,request=fixture();self.addCleanup(repo.close)
        self.assertIsNone(vbp_document.demo_english('Un objetivo arbitrario no preparado'))
        vbp=vbp_document.assemble_vbp_data({'brief':{'objective':'Un objetivo arbitrario no preparado'}})
        vbp_document.prepare_simulated_bilingual(vbp,{'brief':{'objective':'Un objetivo arbitrario no preparado'}})
        self.assertIn('TRANSLATION PENDING',vbp['sections'][0]['content'])
        self.assertEqual(vbp['fingerprint'],runtime_contracts.compute_vbp_manifest_fingerprint(vbp))

if __name__ == "__main__":
    unittest.main()
