"""Pruebas exhaustivas para el Registro de Evidencias y Procedencia (PZ-009A).

Valida soporte multifuente, prevencion de referencias cruzadas entre misiones,
coherencia de fechas, deteccion y registro de contradicciones, revalidacion pre-aprobacion
ante desaparicion de originales y preservacion historica con VERIFICABILIDAD_INCOMPLETA.
"""

import unittest
from datetime import datetime, timezone

import app.evidence_registry as evidence_registry
import app.hq_runtime as hq_runtime


class TestEvidenceRegistry(unittest.TestCase):
    """Suite de pruebas para PZ-009A."""

    def setUp(self) -> None:
        self.registry = evidence_registry.EvidenceRegistry()
        self.runtime = hq_runtime.HQRuntime()

    def test_ac01_one_source_supports_multiple_claims_and_cross_mission_rejected(self) -> None:
        """AC-01: Una fuente respalda multiples evidencias; referencias cruzadas entre misiones se rechazan."""
        now_iso = datetime.now(timezone.utc).isoformat()
        source_loc = "https://wikipedia.org/wiki/Enterprise_Resource_Planning"
        source_body = "ERP integra procesos de compras, inventario y finanzas en una base unificada."

        evd1 = evidence_registry.create_evidence_record(
            evidence_id="EVD-001",
            mission_id="MSN-001",
            claim_id="CLM-001",
            title="Definicion de ERP",
            source_locator=source_loc,
            excerpt_or_summary="ERP integra procesos de compras, inventario y finanzas",
            publication_date="2025-01-01T00:00:00Z",
            retrieval_date=now_iso,
        )

        evd2 = evidence_registry.create_evidence_record(
            evidence_id="EVD-002",
            mission_id="MSN-001",
            claim_id="CLM-002",
            title="Automatizacion con ERP",
            source_locator=source_loc,
            excerpt_or_summary="integra procesos de compras",
            publication_date="2025-01-01T00:00:00Z",
            retrieval_date=now_iso,
        )

        # 1. Registrar ambas bajo la misma fuente
        ok1, err1 = self.registry.register_evidence(evd1, source_content=source_body)
        self.assertTrue(ok1)
        ok2, err2 = self.registry.register_evidence(evd2, source_content=source_body)
        self.assertTrue(ok2)

        evds_for_source = self.registry.get_evidences_for_source(source_loc)
        self.assertEqual(len(evds_for_source), 2)

        # 2. Intento de registrar evidencia de otra mision cruzada
        evd_cross = evidence_registry.create_evidence_record(
            evidence_id="EVD-CROSS-001",
            mission_id="MSN-OTRA-999",
            claim_id="CLM-003",
            title="Claim de otra mision",
            source_locator=source_loc,
            excerpt_or_summary="ERP integra",
            publication_date="2025-01-01T00:00:00Z",
            retrieval_date=now_iso,
        )
        ok_cross, err_cross = self.registry.register_evidence(evd_cross, expected_mission_id="MSN-001")
        self.assertFalse(ok_cross)
        self.assertIn("cruzada rechazada", err_cross)

    def test_ac02_temporal_coherence_and_stale_data_handling(self) -> None:
        """AC-02: Fechas de publicacion y consulta diferenciadas; incoherencias temporales son rechazadas."""
        evd_incoherent = evidence_registry.create_evidence_record(
            evidence_id="EVD-TIME-ERR",
            mission_id="MSN-001",
            claim_id="CLM-ERR",
            title="Dato temporalmente incoherente",
            source_locator="https://example.com/doc",
            excerpt_or_summary="Extracto",
            publication_date="2026-06-01T00:00:00Z",
            retrieval_date="2024-01-01T00:00:00Z",
        )
        ok, err = self.registry.register_evidence(evd_incoherent)
        self.assertFalse(ok)
        self.assertIn("Incoherencia temporal", err)

    def test_ac03_withdrawn_original_blocks_gate_before_approval(self) -> None:
        """AC-03: Retirar la fuente original antes de la aprobacion bloquea la puerta con EVIDENCIA_NO_DISPONIBLE."""
        loc = "https://wikipedia.org/wiki/Supply_Chain"
        now_iso = datetime.now(timezone.utc).isoformat()
        evd = evidence_registry.create_evidence_record(
            evidence_id="EVD-SC-001",
            mission_id="MSN-001",
            claim_id="CLM-SC-001",
            title="Cadena de suministro",
            source_locator=loc,
            excerpt_or_summary="Cadena de suministro optimizada",
            publication_date="2025-01-01T00:00:00Z",
            retrieval_date=now_iso,
        )
        ok_reg, _ = self.registry.register_evidence(evd, source_content="Texto de la cadena de suministro")
        self.assertTrue(ok_reg)

        # 1. Antes del retiro, disponibilidad OK
        ok_before, missing_before, _ = self.registry.validate_availability_before_gate(["EVD-SC-001"])
        self.assertTrue(ok_before)
        self.assertEqual(len(missing_before), 0)

        # 2. Retirar original
        self.registry.withdraw_source(loc)

        # 3. Tras el retiro, validacion falla
        ok_after, missing_after, err_env = self.registry.validate_availability_before_gate(["EVD-SC-001"])
        self.assertFalse(ok_after)
        self.assertIn("EVD-SC-001", missing_after)
        self.assertEqual(err_env["functional_reason"], "EVIDENCIA_REQUERIDA")
        self.assertEqual(err_env["message"], "EVIDENCIA_NO_DISPONIBLE")
        self.assertEqual(err_env["suggested_state"], "PAUSADA")

    def test_ac04_contradictions_preserve_both_sources_and_create_pending_decision(self) -> None:
        """AC-04: Contradicciones documentales preservan ambas fuentes y generan decision pendiente."""
        now_iso = datetime.now(timezone.utc).isoformat()
        evd_a = evidence_registry.create_evidence_record(
            evidence_id="EVD-A",
            mission_id="MSN-001",
            claim_id="CLM-A",
            title="Proyeccion Optimista",
            source_locator="https://fuente-a.com/reporte",
            excerpt_or_summary="Crecimiento del 15%",
            publication_date="2025-01-01T00:00:00Z",
            retrieval_date=now_iso,
            limitations=["Estudio regional"],
        )
        evd_b = evidence_registry.create_evidence_record(
            evidence_id="EVD-B",
            mission_id="MSN-001",
            claim_id="CLM-B",
            title="Proyeccion Conservadora",
            source_locator="https://fuente-b.com/reporte",
            excerpt_or_summary="Contraccion del 5%",
            publication_date="2025-02-01T00:00:00Z",
            retrieval_date=now_iso,
            limitations=["Estudio global"],
        )

        ok_a, _ = self.registry.register_evidence(evd_a, source_content="Informe A")
        self.assertTrue(ok_a)
        ok_b, _ = self.registry.register_evidence(evd_b, source_content="Informe B")
        self.assertTrue(ok_b)

        rec = self.registry.record_contradiction(
            "EVD-A",
            "EVD-B",
            topic="Tasa de crecimiento proyectada",
            description="La fuente A estima crecimiento positivo mientras la fuente B proyecta contraccion.",
        )

        self.assertEqual(rec["status"], "PENDIENTE_DECISION_HUMANA")
        self.assertEqual(rec["evidence_a"], "EVD-A")
        self.assertEqual(rec["evidence_b"], "EVD-B")
        self.assertIsNotNone(self.registry.get_evidence("EVD-A"))
        self.assertIsNotNone(self.registry.get_evidence("EVD-B"))

    def test_ac05_post_approval_source_loss_marks_incomplete_verifiability(self) -> None:
        """AC-05: Si tras aprobacion se pierde la fuente, se conserva el VBP historico marcando VERIFICABILIDAD_INCOMPLETA."""
        now_iso = datetime.now(timezone.utc).isoformat()
        loc = "https://wikipedia.org/wiki/API"
        evd = evidence_registry.create_evidence_record(
            evidence_id="EVD-API-001",
            mission_id="MSN-001",
            claim_id="CLM-API-001",
            title="Estandar API",
            source_locator=loc,
            excerpt_or_summary="APIs REST permiten integraciones desacopladas",
            publication_date="2025-01-01T00:00:00Z",
            retrieval_date=now_iso,
        )
        ok_reg, _ = self.registry.register_evidence(evd, source_content="Documentacion de API")
        self.assertTrue(ok_reg)

        # Simular VBP candidato aprobado
        vbp_approved = {
            "vbp_id": "VBP-MSN-001-v1",
            "manifest": {
                "evidence_items_covered": ["EVD-API-001"],
            },
            "status": "APROBADA",
        }

        # 1. Antes de eliminar la fuente -> COMPLETA
        eval1 = self.registry.assess_post_approval_verifiability(vbp_approved)
        self.assertEqual(eval1["verifiability_status"], "COMPLETA")

        # 2. Eliminar fuente original
        self.registry.withdraw_source(loc)

        # 3. Tras eliminacion -> VERIFICABILIDAD_INCOMPLETA preservando el VBP
        eval2 = self.registry.assess_post_approval_verifiability(vbp_approved)
        self.assertEqual(eval2["verifiability_status"], "VERIFICABILIDAD_INCOMPLETA")
        self.assertEqual(eval2["vbp_id"], "VBP-MSN-001-v1")
        self.assertIn("no se encuentran disponibles", eval2["verifiability_details"])


if __name__ == "__main__":
    unittest.main()
