"""Pruebas exhaustivas para los contratos de runtime (PZ-003C).

Valida metavalidacion Draft 2020-12, ejemplos positivos y negativos de task,
agent-result, evidence y vbp, rechazo estricto de CoT, limites,
completitud de las 18 secciones del VBP, huellas sin autorreferencia y regresion completa.
"""

import builtins
import importlib.util
import io
import os
import sys
from contextlib import ExitStack, redirect_stdout, redirect_stderr
import copy
import hashlib
import json
import socket
import subprocess
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import jsonschema
from jsonschema import Draft202012Validator

import app.runtime_contracts as runtime_contracts

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_RUNTIME_DIR = PROJECT_ROOT / "contracts" / "runtime"


class TestRuntimeContracts(unittest.TestCase):
    """Suite de pruebas para los contratos de runtime PZ-003C."""

    def setUp(self) -> None:
        self.validator = runtime_contracts.RuntimeContractsValidator()
        self.now_iso = "2026-08-30T20:00:00+00:00"

        # Ejemplo positivo canonico de Tarea
        self.valid_task = {
            "schema_version": "1.0.0",
            "task_id": "TSK-001-RESEARCH",
            "mission_id": "MSN-001",
            "mission_version": 1,
            "agent_role": "research_evidence_analyst",
            "objective": "Investigar mercado y regulaciones del sector",
            "question": "Cuales son los requisitos normativos aplicables?",
            "authorized_context": {
                "brief_version": 1,
                "input_refs": ["brief"],
                "evidence_refs": [],
            },
            "approved_decisions": ["DEC-001-ALCANCE"],
            "structured_inputs": {"focus": "regulacion"},
            "expected_output": {
                "description": "Informe estructurado de investigacion",
                "acceptance_criteria": ["Citar al menos 2 fuentes"],
            },
            "allowed_tool_categories": [
                "recuperacion_interna_solo_lectura",
                "investigacion_externa_solo_lectura",
            ],
            "prohibitions": ["No contactar proveedores externos"],
            "limits": {
                "max_attempts": 2,
                "max_seconds": 300,
                "max_budget_usd": 5.0,
                "max_depth": 0,
                "max_breadth": 1,
            },
            "escalation_rules": ["Escalar si ninguna fuente primaria esta disponible"],
            "category": "razonamiento",
            "dependencies": [],
            "status": "PENDIENTE",
            "attempt": 0,
        }

        # Ejemplo positivo canonico de Evidencia
        raw_evidence = {
            "schema_version": "1.0.0",
            "evidence_id": "EVD-001",
            "mission_id": "MSN-001",
            "mission_version": 1,
            "claim_id": "CLM-001",
            "title": "Reporte Oficial de Regulacion 2026",
            "author_or_organization": "Organismo Regulador",
            "source_type": "DOCUMENTO_LOCAL",
            "source_locator": "docs/regulacion_2026.pdf",
            "location_in_source": "Pagina 12, seccion 3.1",
            "publication_date": "2026-01-15T00:00:00+00:00",
            "retrieval_date": self.now_iso,
            "excerpt_or_summary": "Las plataformas B2B deben registrar auditoria estricta.",
            "collector": "research_evidence_analyst",
            "confidence": "ALTA",
            "confidence_justification": "Fuente primaria oficial vigente.",
            "limitations": ["Aplica unicamente a territorio nacional."],
            "contradictions": [],
            "verification_status": "VALIDADA",
        }
        raw_evidence["fingerprint"] = runtime_contracts.compute_evidence_fingerprint(raw_evidence)
        self.valid_evidence = raw_evidence

        # Ejemplo positivo canonico de Resultado de Agente (15 campos de seccion 5.2)
        raw_result = {
            "schema_version": "1.0.0",
            "result_id": "RES-001",
            "task_id": "TSK-001-RESEARCH",
            "mission_id": "MSN-001",
            "mission_version": 1,
            "agent_role": "research_evidence_analyst",
            "status": "SUCCESS",
            "summary": "Investigacion completada satisfactoriamente.",
            "findings": ["Requisitos de auditoria plenamente identificados."],
            "evidence_refs": ["EVD-001"],
            "assumptions": [],
            "limitations": ["Informacion acotada al marco regulatorio actual."],
            "approved_decisions_used": ["DEC-001-ALCANCE"],
            "proposals": ["Proceder con el diseno conceptual."],
            "pending_decisions": [],
            "risks": ["Posible actualizacion normativa a fin de ano."],
            "artifacts": ["ART-001-INFORME"],
            "attempt_count": 1,
            "tool_actions_summary": [
                {
                    "action": "consulta_documento",
                    "tool_or_category": "recuperacion_interna_solo_lectura",
                    "relevant_input_summary": "docs/regulacion_2026.pdf",
                    "result_summary": "Lectura exitosa de la seccion 3.1",
                }
            ],
            "errors": [],
            "recommended_next_step": "Avanzar a tarea TSK-002-ARCH",
            "timestamp": self.now_iso,
            "idempotency_key": "IDEMP-RES-001",
        }
        raw_result["fingerprint"] = runtime_contracts.compute_agent_result_fingerprint(raw_result)
        self.valid_agent_result = raw_result

        # Ejemplo positivo canonico de VBP con las 18 secciones
        sections = []
        for idx, name in enumerate(runtime_contracts.VBP_SECTION_NAMES, start=1):
            sections.append({
                "section_number": idx,
                "section_name": name,
                "status": "COMPLETA",
                "responsible_role": "product_architect" if idx != 5 else "research_evidence_analyst",
                "content": f"# Seccion {idx}: {name}\nContenido validado.",
            })

        raw_vbp = {
            "schema_version": "1.0.0",
            "vbp_id": "VBP-001",
            "mission_id": "MSN-001",
            "mission_version": 1,
            "version": 1,
            "title": "VBP del Portal B2B",
            "created_at": self.now_iso,
            "evidence_cutoff_date": self.now_iso,
            "language": "es",
            "contract_version": "1.2-aprobada",
            "functional_leads": {x["section_name"]: x["responsible_role"] for x in sections},
            "approval_status": "BORRADOR",
            "human_approval_ref": None,
            "included_components": ["brief", "plan", "evidence", "architecture"],
            "missing_or_error_components": [],
            "sections": sections,
        }
        raw_vbp["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(raw_vbp)
        self.valid_vbp = raw_vbp


    def context(self, kind=None, data=None):
        # Registros sinteticos SIMULADOS; no son decisiones humanas reales.
        with open(PROJECT_ROOT / "contracts/core/examples/mission.valid.json", encoding="utf-8") as stream:
            mission = json.load(stream)["test_data"]
        mission["mission_id"] = "MSN-001"
        mission["approval_refs"] = ["APP-DEC"]
        approval = {
            "schema_version": "1.0.0", "approval_id": "APP-DEC", "user_id": mission["user_id"],
            "actor": "usuario_simulado_test", "actor_role": "usuario_humano",
            "action_approved": "Decision de alcance SIMULADA", "version_or_fingerprint": "v1",
            "timestamp": self.now_iso, "decision": "APROBAR", "comment": "SIMULADA",
            "conditions": [], "expiration": None, "status": "CONSUMIDA", "idempotency_key": "IDEMP-DEC",
        }
        def descriptor(ref):
            return {"ref_id": ref, "mission_id": "MSN-001", "mission_version": 1}
        task = copy.deepcopy(data if kind == "task" else self.valid_task)
        if kind == "agent-result":
            task["attempt"] = data["attempt_count"] if type(data.get("attempt_count")) is int else 1
        decision = dict(descriptor("DEC-001-ALCANCE"), approval_ref="APP-DEC")
        return {
            "mission": mission, "tasks": [task], "evidence": [copy.deepcopy(data if kind == "evidence" else self.valid_evidence)],
            "approvals": [approval], "inputs": [descriptor("brief"), descriptor(self.valid_evidence["source_locator"])],
            "decisions": [decision], "claims": [descriptor("CLM-001")],
            "artifacts": [descriptor(ref) for ref in ("ART-001-INFORME", "brief", "plan", "evidence", "architecture")],
        }

    def check(self, kind, data, context=None, validator=None):
        v = validator or self.validator
        method = {"task": v.validate_task, "agent-result": v.validate_agent_result,
                  "evidence": v.validate_evidence, "vbp": v.validate_vbp_assembly}[kind]
        ctx = self.context(kind, data) if context is None else context
        before = repr((data, ctx))
        result = method(data, context=ctx)
        self.assertEqual(repr((data, ctx)), before, "El validador no debe alterar los registros")
        return result

    def reject(self, kind, data, code="INVALID_INPUT", context=None, validator=None):
        ok, errors = self.check(kind, data, context, validator)
        self.assertFalse(ok)
        self.assertEqual([e["error_code"] for e in errors], [code])
        for error in errors:
            self.validator._core_validators["error"].validate(error)
            self.assertNotIn("SYNTHETIC_SENTINEL", json.dumps(error))
        return errors

    def seal(self, kind, data):
        compute = {"agent-result": runtime_contracts.compute_agent_result_fingerprint,
                   "evidence": runtime_contracts.compute_evidence_fingerprint,
                   "vbp": runtime_contracts.compute_vbp_manifest_fingerprint}.get(kind)
        if compute:
            data["fingerprint"] = compute(data)
        return data

    def test_ac01_metavalidation_and_positive_examples(self) -> None:
        """AC-01: Metavalidar los 4 schemas con Draft 2020-12 y verificar ejemplos positivos."""
        task_s, res_s, evd_s, vbp_s = runtime_contracts.load_runtime_contracts()

        Draft202012Validator.check_schema(task_s)
        Draft202012Validator.check_schema(res_s)
        Draft202012Validator.check_schema(evd_s)
        Draft202012Validator.check_schema(vbp_s)

        ok_t, err_t = self.check("task", self.valid_task)
        self.assertTrue(ok_t, f"Errores en tarea valida: {err_t}")

        ok_e, err_e = self.check("evidence", self.valid_evidence)
        self.assertTrue(ok_e, f"Errores en evidencia valida: {err_e}")

        ok_r, err_r = self.check("agent-result", self.valid_agent_result)
        self.assertTrue(ok_r, f"Errores en resultado valido: {err_r}")

        ok_v, err_v = self.check("vbp", self.valid_vbp)
        self.assertTrue(ok_v, f"Errores en VBP valido: {err_v}")

    def test_ac02_rejection_of_cot_extra_fields_and_invalid_types(self) -> None:
        """AC-02: Rechazar campos extra, Chain-of-Thought, tipos invalidos y fechas malformadas."""
        # 1. Inyeccion de Chain-of-Thought en resultado de agente
        bad_cot_result = copy.deepcopy(self.valid_agent_result)
        bad_cot_result["thought"] = "Razonamiento interno que no debe exponerse"
        ok, errs = self.check("agent-result", bad_cot_result)
        self.assertFalse(ok)
        self.assertEqual(errs[0]["error_code"], "INVALID_INPUT")

        # 2. Inyeccion de campo extra en tarea
        bad_task_extra = copy.deepcopy(self.valid_task)
        bad_task_extra["unauthorized_field"] = 123
        ok_t, errors_t = self.check("task", bad_task_extra)
        self.assertFalse(ok_t)
        self.assertEqual(errors_t[0]["error_code"], "INVALID_INPUT")

        # 3. Booleano usado como presupuesto (tipo invalido)
        bad_budget_task = copy.deepcopy(self.valid_task)
        bad_budget_task["limits"]["max_budget_usd"] = True
        ok_b, errors_b = self.check("task", bad_budget_task)
        self.assertFalse(ok_b)
        self.assertEqual(errors_b[0]["error_code"], "INVALID_INPUT")

        # 4. Fecha invalida en evidencia
        bad_date_evd = copy.deepcopy(self.valid_evidence)
        bad_date_evd["retrieval_date"] = "2026-02-30 25:00:00"
        bad_date_evd["fingerprint"] = runtime_contracts.compute_evidence_fingerprint(bad_date_evd)
        ok_d, errors_d = self.check("evidence", bad_date_evd)
        self.assertFalse(ok_d)
        self.assertEqual(errors_d[0]["error_code"], "INVALID_INPUT")

    def test_ac03_rejection_of_cyclic_dependencies_and_unknown_roles(self) -> None:
        """AC-03: Rechazar autodependencias y roles ajenos a los 5 autorizados."""
        # 1. Autodependencia en tarea
        bad_dep_task = copy.deepcopy(self.valid_task)
        bad_dep_task["dependencies"] = [bad_dep_task["task_id"]]
        ok, errs = self.check("task", bad_dep_task)
        self.assertFalse(ok)
        self.assertTrue(any("autodependencia" in e["message"] for e in errs))
        self.assertEqual(errs[0]["error_code"], "INVALID_INPUT")

        # 2. Rol desconocido
        bad_role_task = copy.deepcopy(self.valid_task)
        bad_role_task["agent_role"] = "marketing_lead"
        ok_r, errors_r = self.check("task", bad_role_task)
        self.assertFalse(ok_r)
        self.assertEqual(errors_r[0]["error_code"], "INVALID_INPUT")

    def test_ac04_vbp_18_sections_completeness_and_pending_status(self) -> None:
        """AC-04: Detectar secciones VBP ausentes y validar pending_reason obligatorio en PENDIENTE."""
        # 1. VBP con seccion eliminada (17 en lugar de 18)
        bad_vbp_missing = copy.deepcopy(self.valid_vbp)
        bad_vbp_missing["sections"] = bad_vbp_missing["sections"][:-1]
        bad_vbp_missing["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(bad_vbp_missing)
        ok_m, errs_m = self.check("vbp", bad_vbp_missing)
        self.assertFalse(ok_m)
        self.assertEqual(errs_m[0]["error_code"], "INVALID_INPUT")

        # 2. Seccion PENDIENTE sin pending_reason debe fallar
        bad_vbp_pending = copy.deepcopy(self.valid_vbp)
        bad_vbp_pending["sections"][0]["status"] = "PENDIENTE"
        bad_vbp_pending["sections"][0]["pending_reason"] = "   "  # Vacio
        bad_vbp_pending["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(bad_vbp_pending)
        ok_p, errors_p = self.check("vbp", bad_vbp_pending)
        self.assertFalse(ok_p)
        self.assertEqual(errors_p[0]["error_code"], "INVALID_INPUT")

        # 3. Seccion PENDIENTE con pending_reason valido debe pasar
        valid_vbp_pending = copy.deepcopy(self.valid_vbp)
        valid_vbp_pending["sections"][0]["status"] = "PENDIENTE"
        valid_vbp_pending["sections"][0]["pending_reason"] = "Pendiente de consolidacion final con el usuario"
        valid_vbp_pending["fingerprint"] = runtime_contracts.compute_vbp_manifest_fingerprint(valid_vbp_pending)
        ok_vp, errs_vp = self.check("vbp", valid_vbp_pending)
        self.assertTrue(ok_vp, f"Errores con seccion pendiente valida: {errs_vp}")

    def test_ac05_fingerprint_invariance_and_no_side_effects(self) -> None:
        """AC-05: Invarianza ante orden de claves, rechazo de huella manipulada y 0 efectos en import."""
        # 1. Invarianza de huellas ante orden de claves
        evd1 = copy.deepcopy(self.valid_evidence)
        evd2 = {k: evd1[k] for k in reversed(list(evd1.keys()))}
        fp1 = runtime_contracts.compute_evidence_fingerprint(evd1)
        fp2 = runtime_contracts.compute_evidence_fingerprint(evd2)
        self.assertEqual(fp1, fp2)

        # 2. Huella alterada no coincide
        evd_tampered = copy.deepcopy(self.valid_evidence)
        evd_tampered["title"] = "Titulo Alterado"
        ok_t, errs_t = self.check("evidence", evd_tampered)
        self.assertFalse(ok_t)
        self.assertTrue(any("no coincide" in e["message"] for e in errs_t))
        self.assertEqual(errs_t[0]["error_code"], "INVALID_INPUT")

        # 3. Comprobar que no hay efectos secundarios
        with patch("socket.socket", side_effect=RuntimeError("Red prohibida")), patch(
            "subprocess.Popen", side_effect=RuntimeError("Subprocesos prohibidos")
        ):
            ok_res, _ = self.check("agent-result", self.valid_agent_result)
        self.assertTrue(ok_res)


    def test_h1_all_fingerprints_require_exact_format_and_matching_content(self):
        cases = [("agent-result", self.valid_agent_result, "summary"), ("evidence", self.valid_evidence, "title"),
                 ("vbp", self.valid_vbp, "title")]
        for kind, original, field in cases:
            for fp in ("arbitrary-invalid-hash", "sha256:", "sha256:" + "a"*63, "sha256:"+"A"*64,
                       "sha256:"+"a"*64+"\n", "sha256:"+"0"*64, None, False):
                with self.subTest(kind=kind, fp_type=type(fp).__name__, length=len(fp) if type(fp) is str else None):
                    self.reject(kind, dict(original, fingerprint=fp))
            changed = copy.deepcopy(original)
            changed[field] = "SYNTHETIC_SENTINEL"
            self.reject(kind, changed)

    def test_h1_canonical_keys_array_order_and_hash_domains(self):
        for kind, original, field in (("agent-result",self.valid_agent_result,"findings"),
                                       ("evidence",self.valid_evidence,"limitations"),
                                       ("vbp",self.valid_vbp,"sections")):
            with self.subTest(kind=kind):
                ordered = {key: copy.deepcopy(original[key]) for key in reversed(original)}
                self.assertEqual(self.seal(kind,ordered)["fingerprint"],original["fingerprint"])
                self.assertTrue(self.check(kind,ordered)[0])
                changed = copy.deepcopy(original)
                if kind != "vbp":
                    changed[field] = ["primero", "segundo"]
                    self.seal(kind,changed)
                    self.assertTrue(self.check(kind,changed)[0])
                changed[field].reverse()
                self.reject(kind,changed)
                previous=changed["fingerprint"]
                self.seal(kind,changed)
                self.assertNotEqual(previous,changed["fingerprint"])
                self.assertTrue(self.check(kind,changed)[0])
        vbp=dict(self.valid_vbp,approval_status="APROBADO",human_approval_ref="APP-SIMULADA")
        self.assertEqual(runtime_contracts.compute_vbp_manifest_fingerprint(vbp),self.valid_vbp["fingerprint"])
        # Aunque metadatos no integran la huella, no eluden la comprobacion de aprobacion.
        self.reject("vbp",vbp,"NOT_FOUND")
        vbp["version"]+=1
        self.assertNotEqual(runtime_contracts.compute_vbp_manifest_fingerprint(vbp),self.valid_vbp["fingerprint"])

    def test_h2_task_limits_required_exact_and_exceeded(self):
        for field, good, bad in (("max_attempts",2,3),("max_seconds",300,301),("max_budget_usd",25,25.01),
                                 ("max_depth",0,1),("max_breadth",1,2)):
            with self.subTest(field=field):
                data=copy.deepcopy(self.valid_task);data["limits"][field]=good
                self.assertTrue(self.check("task",data)[0])
                for value in (bad,99999,True,False,None,"2",[],{}):
                    data["limits"][field]=value
                    self.reject("task",data)
                del data["limits"][field]
                self.reject("task",data)
        data=copy.deepcopy(self.valid_task);data["limits"]["max_budget_usd"]=0
        self.assertTrue(self.check("task",data)[0])
        for attempt in (0,1,2):
            self.assertTrue(self.check("task",dict(self.valid_task,attempt=attempt))[0])
        self.reject("task",dict(self.valid_task,attempt=3))
        data=copy.deepcopy(self.valid_task);data["limits"]["max_attempts"]=1;data["attempt"]=2
        self.reject("task",data)

    def test_h2_result_attempts_match_task_and_limit(self):
        for attempt in (1,2):
            data=self.seal("agent-result",dict(self.valid_agent_result,attempt_count=attempt))
            self.assertTrue(self.check("agent-result",data)[0])
        for attempt in (0,3,999,False,"1"):
            self.reject("agent-result",self.seal("agent-result",dict(self.valid_agent_result,attempt_count=attempt)))
        data=copy.deepcopy(self.valid_agent_result)
        ctx=self.context("agent-result",data);ctx["tasks"][0]["attempt"]=0
        self.reject("agent-result",data,context=ctx)
        ctx["tasks"][0]["limits"]["max_attempts"]=1
        ctx["tasks"][0]["attempt"]=1
        self.reject("agent-result",self.seal("agent-result",dict(data,attempt_count=2)),context=ctx)

    def test_h2_complete_graph_duplicates_missing_crossed_and_cycles(self):
        def task(name,deps):
            return dict(copy.deepcopy(self.valid_task),task_id=name,dependencies=deps)
        for rows,code in (([task("A",["B"]),task("B",["A"])],"INVALID_INPUT"),
                          ([task("A",["B"]),task("B",["C"]),task("C",["A"])],"INVALID_INPUT"),
                          ([task("A",["missing"])],"NOT_FOUND"),
                          ([task("A",["B","B"]),task("B",[])],"INVALID_INPUT"),
                          ([task("A",[]) ,task("A",[])],"INVALID_INPUT")):
            for row in rows:
                with self.subTest(tasks=len(rows),task=row["task_id"],code=code):
                    ctx=self.context();ctx["tasks"]=rows
                    self.reject("task",row,code,ctx)
        rows=[task("A",[]),task("B",["A"]),task("C",["A","B"])]
        ctx=self.context();ctx["tasks"]=rows
        for row in rows:
            self.assertTrue(self.check("task",row,ctx)[0])
        for field,value,code in (("mission_id","OTHER","PERMISSION_DENIED"),("mission_version",2,"INVALID_INPUT")):
            changed=copy.deepcopy(ctx);changed["tasks"][0][field]=value
            self.reject("task",changed["tasks"][-1],code,changed)

    def test_h2_context_required_and_no_structural_integrity_claim(self):
        for kind,data,method in (("task",self.valid_task,self.validator.validate_task),
                                  ("evidence",self.valid_evidence,self.validator.validate_evidence),
                                  ("agent-result",self.valid_agent_result,self.validator.validate_agent_result),
                                  ("vbp",self.valid_vbp,self.validator.validate_vbp_assembly)):
            with self.subTest(kind=kind):
                ok,errors=method(data)
                self.assertFalse(ok);self.assertEqual(errors[0]["error_code"],"NOT_FOUND")
                self.assertEqual(self.validator.validate_structure(kind,data),(True,[]))
                self.reject(kind,data,"NOT_FOUND",{})

    def test_h2_missing_reference_groups_and_version_ownership(self):
        cases=[("task",self.valid_task,"inputs"),("task",self.valid_task,"decisions"),
               ("task",self.valid_task,"approvals"),("task",self.valid_task,"tasks"),
               ("agent-result",self.valid_agent_result,"evidence"),("agent-result",self.valid_agent_result,"artifacts"),
               ("evidence",self.valid_evidence,"claims"),("vbp",self.valid_vbp,"artifacts")]
        for kind,data,group in cases:
            with self.subTest(kind=kind,group=group):
                ctx=self.context(kind,data);ctx[group]=[]
                self.reject(kind,data,"NOT_FOUND",ctx)
        for group in ("tasks","evidence","inputs","decisions","claims","artifacts"):
            for field,value,code in (("mission_id","OTHER","PERMISSION_DENIED"),("mission_version",2,"INVALID_INPUT")):
                with self.subTest(group=group,field=field):
                    ctx=self.context();ctx[group][0][field]=value
                    if group=="evidence":self.seal("evidence",ctx[group][0])
                    self.reject("task",self.valid_task,code,ctx)
        ctx=self.context();ctx["approvals"][0]["user_id"]="OTHER"
        self.reject("task",self.valid_task,"PERMISSION_DENIED",ctx)
        for group in ("tasks","evidence","approvals","inputs","decisions","claims","artifacts"):
            ctx=self.context();ctx[group].append(copy.deepcopy(ctx[group][0]))
            self.reject("task",self.valid_task,context=ctx)

    def test_h2_mission_limits_counters_and_brief_versions(self):
        for field,maximum in runtime_contracts.MISSION_LIMITS.items():
            with self.subTest(limit=field):
                ctx=self.context();ctx["mission"]["limits"][field]=maximum+1
                self.reject("task",self.valid_task,context=ctx)
        for field in self.context()["mission"]["counters"]:
            ctx=self.context();ctx["mission"]["counters"][field]=999
            self.reject("task",self.valid_task,context=ctx)
        ctx=self.context();ctx["mission"]["limits"]["max_budget_usd"]=4
        self.reject("task",self.valid_task,context=ctx)
        ctx=self.context();ctx["mission"]["brief_version"]=2
        self.reject("task",self.valid_task,context=ctx)
        ctx=self.context();ctx["tasks"][0]["objective"]="distinto"
        self.reject("task",self.valid_task,context=ctx)

    def test_h2_output_schema_and_transitive_evidence_references(self):
        task=copy.deepcopy(self.valid_task)
        task["expected_output"]["schema_ref"]="https://example.invalid/missing"
        self.reject("task",task,"NOT_FOUND")
        task["expected_output"]["schema_ref"]=self.validator.agent_result_schema["$id"]
        self.assertTrue(self.check("task",task)[0])
        for field in ("claim_id","source_locator"):
            ctx=self.context("agent-result",self.valid_agent_result)
            ctx["evidence"][0][field]="missing"
            self.seal("evidence",ctx["evidence"][0])
            self.reject("agent-result",self.valid_agent_result,"NOT_FOUND",ctx)
        ctx=self.context();ctx["mission"]["approval_refs"]*=2
        self.reject("task",self.valid_task,context=ctx)

    def test_h3_closed_objects_reject_nested_fields_and_do_not_leak(self):
        for field in ("chain_of_thought","internal_reasoning","thought","SYNTHETIC_SENTINEL"):
            for target in ("structured_inputs","authorized_context","expected_output","limits"):
                data=copy.deepcopy(self.valid_task);data[target][field]="SYNTHETIC_SENTINEL"
                self.reject("task",data)
            data=copy.deepcopy(self.valid_agent_result)
            data["tool_actions_summary"][0][field]="SYNTHETIC_SENTINEL"
            self.reject("agent-result",self.seal("agent-result",data))
            data=copy.deepcopy(self.valid_vbp);data["functional_leads"][field]={"nested":"SYNTHETIC_SENTINEL"}
            self.reject("vbp",self.seal("vbp",data))
            data=copy.deepcopy(self.valid_vbp);data["sections"][0][field]="SYNTHETIC_SENTINEL"
            self.reject("vbp",self.seal("vbp",data))
        for kind,data,field in (("task",self.valid_task,"agent_role"),("evidence",self.valid_evidence,"confidence"),
                                ("agent-result",self.valid_agent_result,"status"),("vbp",self.valid_vbp,"approval_status")):
            self.reject(kind,self.seal(kind,dict(data,**{field:"SYNTHETIC_SENTINEL"})))
        data=copy.deepcopy(self.valid_task);data["structured_inputs"]["focus"]={"nested":"SYNTHETIC_SENTINEL"}
        self.reject("task",data)

    def test_h3_core_errors_local_resolution_and_incompatible_policies(self):
        for category in ("INVALID_INPUT","NOT_FOUND","PERMISSION_DENIED","TRANSIENT_FAILURE","SCHEMA_INVALID",
                         "DEPENDENCY_FAILED","BUDGET_EXHAUSTED","SYSTEM_ERROR"):
            error=runtime_contracts.demo_intake.make_error_payload(category,"Error sintetico SIMULADA")
            if category == "TRANSIENT_FAILURE":
                error.update(retry_allowed=True,max_retries=1,required_action="reintentar_una_vez")
            elif category == "DEPENDENCY_FAILED":
                error.update(required_action="bloquear_tareas_descendientes_y_notificar")
            elif category == "BUDGET_EXHAUSTED":
                error.update(required_action="pausar_y_pedir_decision_humana")
            data=self.seal("agent-result",dict(self.valid_agent_result,errors=[error],status="FAILED"))
            self.assertTrue(self.check("agent-result",data)[0])
            for field,value in (("internal_reasoning","SYNTHETIC_SENTINEL"),("current_attempt",999),("retry_allowed","false")):
                bad=copy.deepcopy(data);bad["errors"][0][field]=value
                self.reject("agent-result",self.seal("agent-result",bad))
        for errors in ([{}],[{"internal_reasoning":"SYNTHETIC_SENTINEL"}],[[]],[None]):
            self.reject("agent-result",self.seal("agent-result",dict(self.valid_agent_result,errors=errors)))
        self.assertEqual(self.validator.agent_result_schema["properties"]["errors"]["items"],
                         {"$ref":"https://ominai.dev/contracts/core/error.schema.json"})

    def test_h4_each_section_missing_duplicate_swapped_empty_and_pending(self):
        for index in range(18):
            with self.subTest(section=index+1):
                data=copy.deepcopy(self.valid_vbp);del data["sections"][index]
                self.reject("vbp",self.seal("vbp",data))
                data=copy.deepcopy(self.valid_vbp);data["sections"][index]=copy.deepcopy(data["sections"][(index+1)%18])
                self.reject("vbp",self.seal("vbp",data))
                for content in (""," ","\n\t"):
                    data=copy.deepcopy(self.valid_vbp);data["sections"][index]["content"]=content
                    self.reject("vbp",self.seal("vbp",data))
                data=copy.deepcopy(self.valid_vbp);section=data["sections"][index]
                section.update(status="PENDIENTE",content="",pending_reason="Falta evidencia")
                self.assertTrue(self.check("vbp",self.seal("vbp",data))[0])
                for field in ("responsible_role","pending_reason"):
                    bad=copy.deepcopy(data);del bad["sections"][index][field]
                    self.reject("vbp",self.seal("vbp",bad))
        data=copy.deepcopy(self.valid_vbp);a,b=data["sections"][:2]
        a["section_name"],b["section_name"]=b["section_name"],a["section_name"]
        self.reject("vbp",self.seal("vbp",data))
        data=copy.deepcopy(self.valid_vbp);data["functional_leads"]["Mision"]="sistema"
        self.reject("vbp",self.seal("vbp",data))
        self.assertTrue(self.check("vbp",self.valid_vbp)[0])
        self.reject("vbp",self.seal("vbp",dict(self.valid_vbp,contract_version="1.0.0")))
        self.reject("vbp",self.seal("vbp",dict(self.valid_vbp,schema_version="1.2-aprobada")))

    def approved_vbp(self,status="APROBADO"):
        data=dict(copy.deepcopy(self.valid_vbp),approval_status=status,human_approval_ref="APP-VBP")
        ctx=self.context("vbp",data)
        app=copy.deepcopy(ctx["approvals"][0])
        app.update(approval_id="APP-VBP",action_approved="Aprobacion del VBP VBP-001 v1 de la mision MSN-001",
                   version_or_fingerprint=data["fingerprint"],idempotency_key="IDEMP-VBP-SIMULADA",
                   decision={"APROBADO":"APROBAR","APROBADO_CON_EXCEPCION":"APROBAR_CON_EXCEPCION","RECHAZADO":"RECHAZAR"}[status],
                   conditions=["Condicion sintetica"],comment="Motivo sintetico SIMULADA")
        ctx["approvals"].append(app);ctx["mission"]["approval_refs"].append(app["approval_id"])
        return data,ctx

    def test_h4_vbp_approval_reference_status_user_fingerprint_and_version(self):
        for status in ("APROBADO","APROBADO_CON_EXCEPCION","RECHAZADO"):
            data,ctx=self.approved_vbp(status)
            self.assertTrue(self.check("vbp",data,ctx)[0])
            self.reject("vbp",dict(data,human_approval_ref=None),context=ctx)
            self.reject("vbp",dict(data,human_approval_ref="missing"),"NOT_FOUND",ctx)
            for field,value,code in (("user_id","OTHER","PERMISSION_DENIED"),("action_approved","Otro plan","PERMISSION_DENIED"),
                                     ("version_or_fingerprint","sha256:"+"0"*64,"PERMISSION_DENIED")):
                bad=copy.deepcopy(ctx);bad["approvals"][-1][field]=value
                self.reject("vbp",data,code,bad)
            changed=self.seal("vbp",dict(data,version=2))
            self.reject("vbp",changed,"PERMISSION_DENIED",ctx)
            bad=copy.deepcopy(ctx);bad["approvals"][-1].update(status="PENDIENTE",decision=None)
            self.reject("vbp",data,"PERMISSION_DENIED",bad)
        for status in ("BORRADOR","EN_REVISION"):
            self.reject("vbp",dict(self.valid_vbp,approval_status=status,human_approval_ref="APP-VBP"))
            self.assertTrue(self.check("vbp",dict(self.valid_vbp,approval_status=status))[0])

    def test_h5_invalid_types_keys_cycles_and_nonfinite_numbers_are_controlled(self):
        for kind,base in (("task",self.valid_task),("evidence",self.valid_evidence),
                          ("agent-result",self.valid_agent_result),("vbp",self.valid_vbp)):
            for value in (None,True,1,1.0,"text",[],()):
                self.reject(kind,value,context=self.context())
            data=copy.deepcopy(base);data[42]="SYNTHETIC_SENTINEL"
            self.reject(kind,data,context=self.context())
        for field in ("section_number","section_name"):
            for value in ([],{},None,True):
                data=copy.deepcopy(self.valid_vbp);data["sections"][0][field]=value
                self.reject("vbp",self.seal("vbp",data))
        for number in (float('nan'),float('inf'),float('-inf')):
            data=copy.deepcopy(self.valid_task);data["limits"]["max_budget_usd"]=number
            self.reject("task",data)
            self.reject("agent-result",dict(self.valid_agent_result,attempt_count=number))
            ctx=self.context();ctx["mission"]["limits"]["max_budget_usd"]=number
            self.reject("task",self.valid_task,context=ctx)
        data=copy.deepcopy(self.valid_task);data["structured_inputs"]["focus"]=data
        self.reject("task",data,context=self.context())
        with self.assertRaises(runtime_contracts.ContractError) as captured:
            runtime_contracts.compute_evidence_fingerprint(dict(self.valid_evidence,score=float('nan')))
        self.assertEqual(captured.exception.payload["error_code"],"INVALID_INPUT")

    def test_h5_schema_compatibility_empty_changed_missing_and_meta_invalid(self):
        schemas=runtime_contracts.load_runtime_contracts()
        overrides=[({}, {}, {}, {}),(),[],[None]*4]
        for index in range(4):
            for mutation in (lambda x:x.clear(),lambda x:x.update(type="unknown-type"),
                             lambda x:x.update(additionalProperties=True),lambda x:x.update(required=[]),
                             lambda x:x.update(**{'$schema':'https://example.invalid/schema'})):
                changed=copy.deepcopy(schemas);mutation(changed[index]);overrides.append(changed)
        changed=copy.deepcopy(schemas);changed[1]["properties"]["errors"]["items"]={"$ref":"https://example.invalid/remote"}
        overrides.append(changed)
        for index,override in enumerate(overrides):
            with self.subTest(override=index):
                validator=runtime_contracts.RuntimeContractsValidator(override)
                self.reject("task",{},"SYSTEM_ERROR",self.context(),validator)
        valid=copy.deepcopy(schemas);validator=runtime_contracts.RuntimeContractsValidator(valid)
        valid[0].clear()
        self.assertTrue(self.check("task",self.valid_task,validator=validator)[0])
        validator.task_schema.clear()
        self.reject("task",{},"SYSTEM_ERROR",self.context(),validator)

    def test_h5_io_dependency_failure_and_invalid_dates_are_sanitized(self):
        original_open=builtins.open
        for exception,code in ((FileNotFoundError("SYNTHETIC_SENTINEL"),"NOT_FOUND"),
                               (PermissionError("SYNTHETIC_SENTINEL"),"SYSTEM_ERROR")):
            def fail(file,*args,**kwargs):
                if str(file).endswith('task.schema.json'):raise exception
                return original_open(file,*args,**kwargs)
            with patch('builtins.open',side_effect=fail):
                validator=runtime_contracts.RuntimeContractsValidator()
            self.reject("task",{},code,self.context(),validator)
        with patch.dict(sys.modules,{"jsonschema":None}):
            module=self.fresh_module()
            validator=module.RuntimeContractsValidator()
            ok,errors=validator.validate_task({})
            self.assertFalse(ok);self.assertEqual(errors[0]["error_code"],"SYSTEM_ERROR")
        for field in ("publication_date","retrieval_date"):
            for value in ("2026-02-30T01:00:00Z","2026-08-30","SYNTHETIC_SENTINEL"):
                self.reject("evidence",self.seal("evidence",dict(self.valid_evidence,**{field:value})))

    def fresh_module(self):
        spec=importlib.util.spec_from_file_location('runtime_contracts_probe',runtime_contracts.__file__)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_h6_fresh_import_and_all_paths_have_zero_effect_attempts(self):
        attempts=[]
        def forbidden(*args,**kwargs):
            attempts.append('forbidden')
            raise OSError('SYNTHETIC_SENTINEL')
        def readonly(original):
            def guard(file,mode='r',*args,**kwargs):
                if any(flag in mode for flag in 'wax+'):return forbidden()
                return original(file,mode,*args,**kwargs)
            return guard
        original_os_open=os.open
        def safe_os_open(path,flags,*args,**kwargs):
            if flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):return forbidden()
            return original_os_open(path,flags,*args,**kwargs)
        with ExitStack() as stack:
            for target in ('socket.socket','socket.create_connection','socket.getaddrinfo','urllib.request.urlopen',
                           'subprocess.Popen','subprocess.run','os.system','os.popen','os.mkdir','os.remove','os.unlink',
                           'os.rename','os.replace','os.rmdir'):
                stack.enter_context(patch(target,side_effect=forbidden))
            stack.enter_context(patch('builtins.open',side_effect=readonly(builtins.open)))
            stack.enter_context(patch('io.open',side_effect=readonly(io.open)))
            stack.enter_context(patch('os.open',side_effect=safe_os_open))
            with redirect_stdout(io.StringIO()) as out,redirect_stderr(io.StringIO()) as err:
                module=self.fresh_module()
            self.assertEqual(out.getvalue(),'');self.assertEqual(err.getvalue(),'')
            validator=module.RuntimeContractsValidator()
            for kind,data in (("task",self.valid_task),("agent-result",self.valid_agent_result),
                              ("evidence",self.valid_evidence),("vbp",self.valid_vbp)):
                self.assertTrue(self.check(kind,data,validator=validator)[0])
                self.reject(kind,dict(data,internal_reasoning="SYNTHETIC_SENTINEL"),validator=validator)
            data=self.seal("agent-result",dict(self.valid_agent_result,errors=[runtime_contracts.demo_intake.make_error_payload('SYSTEM_ERROR','SIMULADA')]))
            self.assertTrue(self.check("agent-result",data,validator=validator)[0])
            with patch.dict(sys.modules,{"jsonschema":None}):
                unavailable=self.fresh_module().RuntimeContractsValidator()
                ok,errors=unavailable.validate_task({})
                self.assertFalse(ok);self.assertEqual(errors[0]["error_code"],"SYSTEM_ERROR")
        self.assertEqual(attempts,[],"Ni siquiera se permite intentar un efecto y capturar su excepcion")


if __name__ == "__main__":
    unittest.main()
