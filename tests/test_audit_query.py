"""Pruebas exhaustivas para la Auditoria Consultable y Trazas Minimizadas (PZ-009D).

Valida reconstruccion de trayectoria, deteccion de eventos duplicados, aislamiento estricto por mision,
sanitizacion de CoT, secretos y rutas privadas, y preservacion de la integridad historica.
"""

import unittest

import app.audit_query as audit_query
import app.hq_runtime as hq_runtime


class TestAuditQuery(unittest.TestCase):
    """Suite de pruebas para PZ-009D."""

    def setUp(self) -> None:
        self.engine = audit_query.AuditQueryEngine()
        self.runtime = hq_runtime.HQRuntime(audit_engine=self.engine)

    def test_ac01_reconstruct_full_trajectory(self) -> None:
        """AC-01: Reconstruir recorrido completo con fuentes, aprobaciones, checkpoints y etapas."""
        events = [
            {
                "event_id": "EVT-001",
                "mission_id": "MSN-AUDIT-001",
                "actor": "usuario_humano",
                "actor_role": "usuario_humano",
                "action": "Ingesta inicial de mision",
                "result_summary": "Mision registrada en estado BORRADOR",
            },
            {
                "event_id": "EVT-002",
                "mission_id": "MSN-AUDIT-001",
                "actor": "chief_of_staff",
                "actor_role": "chief_of_staff",
                "action": "Propuesta de plan de 4 tareas",
                "result_summary": "Plan formulado y checkpoint generado",
                "checkpoint_id": "CHK-001",
            },
            {
                "event_id": "EVT-003",
                "mission_id": "MSN-AUDIT-001",
                "actor": "usuario_humano",
                "actor_role": "usuario_humano",
                "action": "Aprobacion humana de plan",
                "decision_id": "DEC-PLAN-001",
                "result_summary": "Plan aprobado para ejecucion",
            },
            {
                "event_id": "EVT-004",
                "mission_id": "MSN-AUDIT-001",
                "actor": "governance_risk",
                "actor_role": "governance_risk",
                "action": "Dictamen de gobernanza",
                "result_summary": "Dictamen emitido: PASA",
            },
        ]

        for ev in events:
            ok, err = self.engine.record_event(ev)
            self.assertTrue(ok, f"Fallo al registrar evento: {err}")

        traj = self.engine.reconstruct_trajectory("MSN-AUDIT-001")
        self.assertEqual(traj["total_events"], 4)
        self.assertEqual(len(traj["approvals_recorded"]), 1)
        self.assertEqual(len(traj["checkpoints_recorded"]), 1)
        self.assertIn("Ingesta inicial de mision", traj["stages_passed"])

    def test_ac02_duplicate_events_and_missing_identifiers_rejected(self) -> None:
        """AC-02: Rechazar identificadores duplicados y eventos sin datos obligatorios."""
        ev1 = {
            "event_id": "EVT-DUP-001",
            "mission_id": "MSN-001",
            "action": "Accion 1",
            "result_summary": "Resumen 1",
        }
        ok1, _ = self.engine.record_event(ev1)
        self.assertTrue(ok1)

        # Intento de duplicado
        ok_dup, err_dup = self.engine.record_event(ev1)
        self.assertFalse(ok_dup)
        self.assertIn("duplicado", err_dup)

        # Intento sin mission_id
        ok_bad, err_bad = self.engine.record_event({"event_id": "EVT-BAD"})
        self.assertFalse(ok_bad)
        self.assertIn("mission_id", err_bad)

    def test_ac03_strict_mission_isolation_and_cot_secret_scrubbing(self) -> None:
        """AC-03: Aislamiento estricto entre misiones; eliminacion de CoT, secretos y rutas privadas."""
        # Evento de mision 1 con CoT y secreto
        ev_m1 = {
            "event_id": "EVT-M1-01",
            "mission_id": "MSN-ALFA",
            "action": "Ejecucion con CoT",
            "result_summary": "Resultado <thought>Razonamiento interno oculto</thought> con api_key='sk-1234567890abcdef' en C:\\Users\\Admin\\secret.json",
        }

        # Evento de mision 2
        ev_m2 = {
            "event_id": "EVT-M2-01",
            "mission_id": "MSN-BETA",
            "action": "Accion de mision Beta",
            "result_summary": "Datos de Beta",
        }

        self.engine.record_event(ev_m1)
        self.engine.record_event(ev_m2)

        # 1. Consultar MSN-ALFA no debe contener nada de MSN-BETA
        res_alfa = self.engine.query_timeline("MSN-ALFA")
        self.assertEqual(len(res_alfa), 1)
        self.assertEqual(res_alfa[0]["mission_id"], "MSN-ALFA")

        summary_alfa = res_alfa[0]["result_summary"]
        self.assertNotIn("<thought>", summary_alfa)
        self.assertNotIn("sk-1234567890abcdef", summary_alfa)
        self.assertNotIn("C:\\Users\\Admin", summary_alfa)
        self.assertIn("[COT_ELIMINADO]", summary_alfa)
        self.assertIn("[REDACTED_SECRET]", summary_alfa)
        self.assertIn("[RUTA_LOCAL_PROTEGIDA]", summary_alfa)

        # 2. Consultar MSN-BETA
        res_beta = self.engine.query_timeline("MSN-BETA")
        self.assertEqual(len(res_beta), 1)
        self.assertEqual(res_beta[0]["mission_id"], "MSN-BETA")

    def test_ac04_fault_comparison_preserves_unaltered_history(self) -> None:
        """AC-04: Registrar un fallo preserva la cronologia exacta anterior sin alterar la historia."""
        self.engine.record_event({
            "event_id": "EVT-OK-01",
            "mission_id": "MSN-FAULT-001",
            "action": "Inicio",
            "result_summary": "Ok",
        })
        self.engine.record_event({
            "event_id": "EVT-ERR-02",
            "mission_id": "MSN-FAULT-001",
            "action": "Fallo en paso 2",
            "result_summary": "Recurso no disponible",
            "error_code": "RESOURCE_UNAVAILABLE",
        })

        traj = self.engine.reconstruct_trajectory("MSN-FAULT-001")
        self.assertEqual(traj["total_events"], 2)
        self.assertEqual(len(traj["errors_recorded"]), 1)
        self.assertEqual(traj["errors_recorded"][0]["error_code"], "RESOURCE_UNAVAILABLE")

    def test_ac05_runtime_integration(self) -> None:
        """AC-05: El AuditQueryEngine se encuentra accesible en HQRuntime."""
        self.assertIsNotNone(self.runtime.audit_engine)
        self.assertIsInstance(self.runtime.audit_engine, audit_query.AuditQueryEngine)


class TestCanonicalAudit(unittest.TestCase):
    def test_persisted_canonical_projection_filters_and_history(self):
        from test_human_approvals import fixture
        runtime,repo,ctx,request=fixture(stage='vbp');self.addCleanup(repo.close)
        before=list(repo._conn.iterdump())
        audit=runtime.audit_engine
        trajectory=audit.reconstruct_trajectory('MSN-SIM')
        self.assertEqual(trajectory['total_events'],len(repo.list_events('MSN-SIM')))
        self.assertTrue(trajectory['checkpoints_recorded'])
        selected=audit.query_timeline('MSN-SIM',decision_id=repo.get_mission('MSN-SIM')['pending_GATE_1_PLAN'])
        self.assertTrue(selected)
        self.assertEqual(audit.query_timeline('MSN-FOREIGN'),[])
        self.assertEqual(audit.query_timeline('MSN-SIM',task_id='TSK-FOREIGN'),[])
        tasks=audit.query_timeline('MSN-SIM',task_id='TSK-001-RESEARCH')
        self.assertEqual(len(tasks),2)
        self.assertEqual([event['new_state'] for event in tasks],['EN_CURSO','COMPLETA'])
        self.assertTrue(all(event['attempt']==1 for event in tasks))
        self.assertTrue(audit.query_timeline('MSN-SIM',source_locator='MSN-SIM'))
        ev = dict(repo.list_events('MSN-SIM')[-1])
        ev.update(event_id='EVT-SCRUB', idempotency_key='EVT-SCRUB', result_summary='<thought>PRIVATE</thought> password=1234567890123456 C:\\private\\data')
        repo.save_event(ev)
        output = repr(audit.query_timeline('MSN-SIM'))
        self.assertNotIn('PRIVATE', output)
        self.assertNotIn('1234567890123456', output)
        self.assertNotIn('C:\\private', output)
        stored_ev = repo.get_object('event', 'EVT-SCRUB')
        self.assertNotIn('PRIVATE', stored_ev['result_summary'])
        self.assertIn('[COT_ELIMINADO]', stored_ev['result_summary'])
        self.assertIn('[REDACTED_SECRET]', stored_ev['result_summary'])
        self.assertIn('[RUTA_LOCAL_PROTEGIDA]', stored_ev['result_summary'])

if __name__ == "__main__":
    unittest.main()
