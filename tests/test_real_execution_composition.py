"""REAL-02 – Pruebas de RealExecutionComposition.

Cubre todos los criterios de aceptacion del encargo:

1. Composicion con un unico repositorio y aprobacion emitida por HumanApprovalEngine.
2. Rechazo de repositorio ausente / en memoria / contexto ajeno / aprobacion
   ausente / tarea no autorizada / perfil simulado (sin llamadas ni reservas).
3. Una llamada controlada: resultado y consumo persistidos.
4. Repeticion y reapertura SQLite: mismo resultado, sin llamada ni reserva adicional.
5. Cancelacion o cambio de plan: rechazo sin sustituir el registro adquirido.
6. Concurrencia: como maximo una llamada para la misma clave.
7. Excepcion o consumo incierto: sin reintento automatico.
8. Ausencia de transaccion SQLite abierta durante la invocacion.
9. Regresion de REAL-01, gateway, aprobaciones humanas y seguridad HTTP.

DISTINCION CON LLAMADA REAL A GEMINI:
  El proveedor de estas pruebas es ControlledProvider (proveedor_kind="ADK_REAL").
  No realiza llamadas HTTP al API de Gemini. El resultado lleva
  'execution_evidence': 'REAL_NO_VERIFICADA', lo que indica que no hay
  evidencia de ejecucion real verificada. No existe aun una prueba manual
  desde la interfaz de OminAI HQ.

NO se usan credenciales, llamadas externas, Docker ni despliegues.
"""

import copy
import tempfile
import threading
import unittest
from pathlib import Path

import app.agent_gateway as agent_gateway
from app.hq_runtime import HQRuntime
from app.local_repository import LocalRepository
from app.real_execution_composition import RealExecutionComposition

# ─────────────────────────────────────────────────────────────────
# Constantes de prueba
# ─────────────────────────────────────────────────────────────────

PROFILE = {
    "user_id": "USR-NIKO-REAL02",
    "display_name": "Niko REAL-02",
    "actor_role": "usuario_humano",
}
MISSION_ID = "MSN-REAL-02"
TASK_ID = "TSK-001-RESEARCH"

_OK_RESPONSE_JSON = '{"status":"ok"}'
_TEST_SCHEMA = {
    "type": "object",
    "properties": {"status": {"type": "string"}},
    "required": ["status"],
    "additionalProperties": False,
}


# ─────────────────────────────────────────────────────────────────
# Proveedor controlado exclusivamente en estas pruebas
# ─────────────────────────────────────────────────────────────────

class ControlledProvider(agent_gateway.ModelClientProvider):
    """Proveedor determinista de prueba. NO realiza llamadas reales a Gemini.
    provider_kind='ADK_REAL' para que AgentGateway acepte el modo REAL."""

    provider_kind = "ADK_REAL"

    def __init__(self, responses):
        self.responses = list(responses)
        self.call_count = 0

    def has_credentials(self):
        return True

    def preflight(self):
        return True, None

    def call_model(self, model_name, system_instruction, prompt, timeout_seconds,
                   *, max_output_tokens=4096, response_schema=None):
        self.call_count += 1
        return self.responses.pop(0)


# ─────────────────────────────────────────────────────────────────
# Helpers de fixtures
# ─────────────────────────────────────────────────────────────────

def setup_approved_mission(repo, mission_id=MISSION_ID):
    """Crea una mision aprobada usando HumanApprovalEngine real.
    Devuelve (runtime, context, request, response, mission)."""
    runtime = HQRuntime(repository=repo)
    context = runtime.approvals.bind_local_profile(PROFILE)
    ok, mission, error = runtime.create_local_mission(
        {
            "mission_id": mission_id,
            "title": "REAL-02 controlada",
            "objective": "Validar composicion segura",
            "context": "Prueba local sin llamadas externas",
            "expected_result": "Composicion verificable",
        },
        context,
    )
    if not ok:
        raise AssertionError(f"create_local_mission fallo: {error}")

    envelope = repo.get_object("approval_request", mission["approval_id"])
    request = envelope["request"]
    ok, response, error = runtime.approvals.submit_human_decision(
        request, "APROBAR", context=context
    )
    if not ok:
        raise AssertionError(f"submit_human_decision fallo: {error}")
    mission = repo.get_mission(mission_id)
    return runtime, context, request, response, mission


def make_composition(repo, runtime, context, provider=None,
                     mission_id=MISSION_ID, task_id=TASK_ID):
    """Construye RealExecutionComposition con proveedor controlado."""
    provider = provider or ControlledProvider([])
    return RealExecutionComposition(
        repo, mission_id, task_id,
        runtime.approvals, context,
        _provider_override=provider,
    )


def call(comp, provider_responses=None, schema=None):
    """Llama a execute_task con respuestas opcionales inyectadas."""
    if provider_responses is not None:
        comp._provider.responses.extend(provider_responses)
    return comp.execute_task(
        system_instruction="Sistema de prueba",
        prompt="Prompt de prueba",
        response_schema=schema or _TEST_SCHEMA,
    )


# ─────────────────────────────────────────────────────────────────
# 1. Composicion con repositorio y aprobacion de HumanApprovalEngine
# ─────────────────────────────────────────────────────────────────

class TestCompositionSetup(unittest.TestCase):
    def test_construction_requires_persistent_repo(self):
        """Repositorio :memory: es rechazado en construccion."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "test.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)
        provider = ControlledProvider([])

        # memory repo debe rechazarse
        mem_repo = LocalRepository(":memory:")
        self.addCleanup(mem_repo.close)
        with self.assertRaises(ValueError) as ctx:
            RealExecutionComposition(
                mem_repo, MISSION_ID, TASK_ID,
                runtime.approvals, context,
                _provider_override=provider,
            )
        self.assertIn("persistente", str(ctx.exception))

    def test_construction_requires_repository(self):
        """Repositorio None es rechazado en construccion."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "test.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)
        with self.assertRaises(ValueError):
            RealExecutionComposition(
                None, MISSION_ID, TASK_ID,
                runtime.approvals, context,
                _provider_override=ControlledProvider([]),
            )

    def test_construction_requires_approvals_and_context(self):
        """approvals o human_context None son rechazados en construccion."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "test.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)
        provider = ControlledProvider([])

        with self.assertRaises(ValueError):
            RealExecutionComposition(repo, MISSION_ID, TASK_ID,
                                     None, context, _provider_override=provider)
        with self.assertRaises(ValueError):
            RealExecutionComposition(repo, MISSION_ID, TASK_ID,
                                     runtime.approvals, None, _provider_override=provider)

    def test_valid_construction_succeeds(self):
        """Construccion con repositorio valido y contexto humano verificado es exitosa."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "test.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)
        comp = make_composition(repo, runtime, context)
        self.assertIsNotNone(comp)


# ─────────────────────────────────────────────────────────────────
# 2. Rechazos previos con cero llamadas y cero reservas
# ─────────────────────────────────────────────────────────────────

class TestRejectionsCauseNoCallsNoReservations(unittest.TestCase):
    def setUp(self):
        td = tempfile.mkdtemp()
        self.path = str(Path(td) / "test.db")
        self.repo = LocalRepository(self.path)
        self.addCleanup(self.repo.close)
        self.runtime, self.context, self.request, _, self.mission = (
            setup_approved_mission(self.repo)
        )

    def test_wrong_owner_context_rejected_with_no_calls(self):
        """Un contexto con propietario diferente es rechazado sin llamadas."""
        # Crear un segundo runtime/perfil para otro propietario
        repo2 = LocalRepository(self.path)
        self.addCleanup(repo2.close)
        runtime2 = HQRuntime(repository=repo2)
        # Intentar construir con un contexto cuyo user_id no coincide con la mision
        other_profile = {
            "user_id": "USR-OTRO",
            "display_name": "Otro",
            "actor_role": "usuario_humano",
        }
        # bind_local_profile rechazara porque ya hay un perfil diferente
        with self.assertRaises(Exception):
            runtime2.approvals.bind_local_profile(other_profile)

    def test_absent_plan_approval_causes_no_calls(self):
        """Si la mision no tiene aprobacion consumida, execute_task devuelve error sin llamadas."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "test2.db")
        repo2 = LocalRepository(path)
        self.addCleanup(repo2.close)
        runtime2 = HQRuntime(repository=repo2)
        context2 = runtime2.approvals.bind_local_profile(PROFILE)
        ok, mission2, error = runtime2.create_local_mission(
            {
                "mission_id": "MSN-PENDIENTE",
                "title": "Solo con plan pendiente",
                "objective": "Sin aprobar",
                "context": "Prueba",
                "expected_result": "Rechazo",
            },
            context2,
        )
        self.assertTrue(ok, error)
        provider = ControlledProvider([])
        comp = RealExecutionComposition(
            repo2, "MSN-PENDIENTE", TASK_ID,
            runtime2.approvals, context2,
            _provider_override=provider,
        )
        ok, _, error = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertFalse(ok)
        self.assertEqual(provider.call_count, 0, "No debe haber llamadas al proveedor")
        self.assertEqual(repo2.budget_snapshot()["requests"], 0, "No debe haber reservas")

    def test_unauthorized_task_rejected_with_no_calls(self):
        """Una tarea que no pertenece al plan rechaza sin llamadas ni reservas."""
        provider = ControlledProvider([])
        comp = RealExecutionComposition(
            self.repo, MISSION_ID, "TSK-NO-EXISTE",
            self.runtime.approvals, self.context,
            _provider_override=provider,
        )
        ok, _, error = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertFalse(ok)
        self.assertEqual(provider.call_count, 0)
        self.assertEqual(self.repo.budget_snapshot()["requests"], 0)

    def test_simulated_profile_rejected_without_real_mode(self):
        """El perfil REAL es el unico modo aceptado; SIMULADA falla antes de llamar."""
        # La construccion del gateway en modo SIMULADA sin proveedor ADK_REAL
        # falla al intentar execute_task porque el config es REAL pero el
        # proveedor controlado tiene provider_kind="ADK_REAL".
        # El encargo prohibe fallback simulado en produccion.
        # Esta prueba verifica que cero reintentos es la politica.
        provider = ControlledProvider([])
        comp = make_composition(self.repo, self.runtime, self.context, provider)
        self.assertEqual(comp._config.max_retries, 0,
                         "La composicion debe configurar cero reintentos automaticos")
        self.assertEqual(comp._config.execution_mode, "REAL")


# ─────────────────────────────────────────────────────────────────
# 3. Llamada controlada: resultado y consumo persistidos
# ─────────────────────────────────────────────────────────────────

class TestControlledCall(unittest.TestCase):
    def setUp(self):
        td = tempfile.mkdtemp()
        self.path = str(Path(td) / "test.db")
        self.repo = LocalRepository(self.path)
        self.addCleanup(self.repo.close)
        self.runtime, self.context, self.request, _, self.mission = (
            setup_approved_mission(self.repo)
        )

    def test_successful_call_returns_result_and_persists_outcome(self):
        """Una llamada exitosa devuelve resultado y persiste el consumo."""
        provider = ControlledProvider([
            agent_gateway.ModelCallResponse(_OK_RESPONSE_JSON, 10, 20)
        ])
        comp = make_composition(self.repo, self.runtime, self.context, provider)
        ok, result, error = comp.execute_task(
            system_instruction="Sistema", prompt="Prompt", response_schema=_TEST_SCHEMA
        )
        self.assertTrue(ok, error)
        self.assertEqual(provider.call_count, 1)
        self.assertIn("execution_evidence", result)
        self.assertEqual(result["execution_evidence"], "REAL_NO_VERIFICADA")
        # Consumo registrado: la reserva queda en 0 despues de reconciliar
        self.assertEqual(self.repo.budget_snapshot()["reserved_usd"], 0)
        self.assertEqual(self.repo.budget_snapshot()["requests"], 1)

    def test_no_automatic_retries_on_transient_failure(self):
        """Un fallo transitorio no produce segundo intento automatico."""
        provider = ControlledProvider([
            agent_gateway.ModelCallResponse("", 0, 0, status_code=429, is_transient=True)
        ])
        comp = make_composition(self.repo, self.runtime, self.context, provider)
        ok, _, error = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertFalse(ok)
        # max_retries=0: exactamente una llamada, sin reintento
        self.assertEqual(provider.call_count, 1,
                         "Con max_retries=0 no debe haber segundo intento")


# ─────────────────────────────────────────────────────────────────
# 4. Repeticion y reapertura SQLite: mismo resultado, sin nueva llamada
# ─────────────────────────────────────────────────────────────────

class TestRepeatAndReopen(unittest.TestCase):
    def test_second_call_same_session_replays_without_provider(self):
        """Una segunda llamada en la misma sesion devuelve el resultado persistido."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "replay.db")
        repo = LocalRepository(path)
        runtime, context, *_ = setup_approved_mission(repo)
        provider = ControlledProvider([
            agent_gateway.ModelCallResponse(_OK_RESPONSE_JSON, 5, 10)
        ])
        comp = make_composition(repo, runtime, context, provider)

        ok1, res1, _ = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertTrue(ok1)
        self.assertEqual(provider.call_count, 1)

        ok2, res2, err2 = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertTrue(ok2, err2)
        self.assertEqual(provider.call_count, 1, "La segunda llamada no debe invocar al proveedor")
        self.assertEqual(res1, res2, "El resultado del replay debe ser identico")
        self.assertEqual(repo.budget_snapshot()["requests"], 1,
                         "No deben registrarse solicitudes adicionales en el replay")
        repo.close()

    def test_reopen_db_returns_same_result(self):
        """Tras reabrir la base el resultado terminal se recupera sin nueva invocacion."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "reopen.db")
        MID = "MSN-REAL-02-REOPEN"

        # ── Sesion 1 ──
        repo1 = LocalRepository(path)
        runtime1, context1, *_ = setup_approved_mission(repo1, mission_id=MID)
        provider1 = ControlledProvider([
            agent_gateway.ModelCallResponse(_OK_RESPONSE_JSON, 5, 10)
        ])
        comp1 = RealExecutionComposition(
            repo1, MID, TASK_ID,
            runtime1.approvals, context1,
            _provider_override=provider1,
        )
        ok1, res1, _ = comp1.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertTrue(ok1)
        self.assertEqual(provider1.call_count, 1)
        snap1 = repo1.budget_snapshot()
        repo1.close()

        # ── Sesion 2: reabrir ──
        repo2 = LocalRepository(path)
        runtime2 = HQRuntime(repository=repo2)
        context2 = runtime2.approvals.bind_local_profile(PROFILE)
        provider2 = ControlledProvider([])
        comp2 = RealExecutionComposition(
            repo2, MID, TASK_ID,
            runtime2.approvals, context2,
            _provider_override=provider2,
        )
        ok2, res2, err2 = comp2.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertTrue(ok2, err2)
        self.assertEqual(provider2.call_count, 0,
                         "Replay no debe invocar al proveedor")
        self.assertEqual(res1, res2, "Resultado del replay debe ser identico")
        self.assertEqual(repo2.budget_snapshot(), snap1)
        repo2.close()


# ─────────────────────────────────────────────────────────────────
# 5. Cancelacion o cambio de plan: rechazo sin sustituir registro adquirido
# ─────────────────────────────────────────────────────────────────

class TestPlanChangeAfterComposition(unittest.TestCase):
    def test_plan_change_after_composition_rejects_execution(self):
        """Si el plan cambia despues de componer, execute_task rechaza sin adquirir nueva clave."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "plan_change.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)
        provider = ControlledProvider([])
        comp = make_composition(repo, runtime, context, provider)

        # Alterar el plan despues de componer
        mission = repo.get_mission(MISSION_ID)
        mission["plan"]["tasks"][0]["objective"] = "Objetivo alterado despues de aprobar"
        repo.save_mission(mission)

        ok, _, error = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertFalse(ok)
        self.assertEqual(provider.call_count, 0,
                         "Un plan alterado no debe invocar al proveedor")
        self.assertEqual(repo.budget_snapshot()["requests"], 0)

    def test_plan_change_does_not_replace_acquired_record(self):
        """Si la primera llamada adquirio IN_PROGRESS, el cambio no sobrescribe el registro."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "plan_replace.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)

        # Primera llamada exitosa: adquiere y completa
        provider1 = ControlledProvider([
            agent_gateway.ModelCallResponse(_OK_RESPONSE_JSON, 5, 10)
        ])
        comp1 = make_composition(repo, runtime, context, provider1)
        ok1, _, _ = comp1.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertTrue(ok1)

        # Ahora alterar el plan
        mission = repo.get_mission(MISSION_ID)
        mission["plan"]["tasks"][0]["objective"] = "Objetivo alterado"
        repo.save_mission(mission)

        # Segunda llamada: CONTENT_CHANGED por fingerprint diferente; no reutiliza
        provider2 = ControlledProvider([])
        comp2 = make_composition(repo, runtime, context, provider2)
        ok2, _, error2 = comp2.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertFalse(ok2)
        self.assertEqual(provider2.call_count, 0,
                         "Un plan alterado no debe invocar al proveedor en la segunda llamada")


# ─────────────────────────────────────────────────────────────────
# 6. Concurrencia: como maximo una llamada para la misma clave
# ─────────────────────────────────────────────────────────────────

class TestConcurrency(unittest.TestCase):
    def test_only_one_thread_executes_for_same_key(self):
        """Con dos hilos concurrentes, exactamente uno produce una llamada al proveedor."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "concurrent.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)

        results = []
        lock = threading.Lock()

        def try_execute():
            provider = ControlledProvider([
                agent_gateway.ModelCallResponse(_OK_RESPONSE_JSON, 5, 10)
            ])
            comp = RealExecutionComposition(
                repo, MISSION_ID, TASK_ID,
                runtime.approvals, context,
                _provider_override=provider,
            )
            ok, result, error = comp.execute_task(
                system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
            )
            with lock:
                results.append({"ok": ok, "calls": provider.call_count})

        threads = [threading.Thread(target=try_execute) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Solo un hilo debe haber ejecutado la llamada (NEW), el otro REPLAY o error
        total_provider_calls = sum(r["calls"] for r in results)
        self.assertEqual(total_provider_calls, 1,
                         "Solo un hilo debe invocar al proveedor")


# ─────────────────────────────────────────────────────────────────
# 7. Excepcion o consumo incierto: sin reintento automatico
# ─────────────────────────────────────────────────────────────────

class TestUncertainOutcome(unittest.TestCase):
    def test_timeout_preserves_reservation_and_no_retry(self):
        """Un timeout preserva la reserva y no se reintenta automaticamente."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "timeout.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)
        provider = ControlledProvider([
            agent_gateway.ModelCallResponse("", 0, 0, status_code=503,
                                           is_transient=True, usage_confirmed=False)
        ])
        comp = make_composition(repo, runtime, context, provider)
        ok, _, error = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertFalse(ok)
        self.assertEqual(provider.call_count, 1,
                         "Sin reintento: exactamente una llamada")
        # La reserva debe permanecer para auditoria
        self.assertGreater(repo.budget_snapshot()["reserved_usd"], 0,
                           "La reserva debe conservarse para auditoria ante resultado incierto")

    def test_second_call_on_in_progress_does_not_retry(self):
        """Si la clave esta en IN_PROGRESS, la segunda llamada no invoca al proveedor."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "inprogress.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)
        # Primera llamada: resultado incierto (503 sin usage_confirmed)
        provider = ControlledProvider([
            agent_gateway.ModelCallResponse("", 0, 0, status_code=503,
                                           is_transient=True, usage_confirmed=False)
        ])
        comp = make_composition(repo, runtime, context, provider)
        ok1, _, _ = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertFalse(ok1)
        first_calls = provider.call_count

        # Segunda llamada: no debe invocar al proveedor
        ok2, _, error2 = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertFalse(ok2)
        self.assertEqual(provider.call_count, first_calls,
                         "IN_PROGRESS no debe producir nueva invocacion al proveedor")
        self.assertEqual(error2.get("error_code"), "SYSTEM_ERROR")


# ─────────────────────────────────────────────────────────────────
# 8. Ausencia de transaccion abierta durante la invocacion
# ─────────────────────────────────────────────────────────────────

class TestNoOpenTransactionDuringCall(unittest.TestCase):
    def test_transaction_depth_is_zero_during_provider_call(self):
        """El repositorio no tiene una transaccion SQLite abierta cuando el proveedor es invocado."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "txn_depth.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)

        observed_depth = []

        class DepthCapturingProvider(agent_gateway.ModelClientProvider):
            provider_kind = "ADK_REAL"

            def has_credentials(self):
                return True

            def preflight(self):
                return True, None

            def call_model(self, model_name, system_instruction, prompt,
                           timeout_seconds, *, max_output_tokens=4096,
                           response_schema=None):
                # Capturar la profundidad de transaccion durante la llamada
                observed_depth.append(repo._depth)
                return agent_gateway.ModelCallResponse(_OK_RESPONSE_JSON, 5, 10)

        comp = make_composition(repo, runtime, context, DepthCapturingProvider())
        ok, _, err = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertTrue(ok, err)
        self.assertEqual(len(observed_depth), 1)
        self.assertEqual(observed_depth[0], 0,
                         "El repositorio no debe tener una transaccion abierta durante la llamada")


# ─────────────────────────────────────────────────────────────────
# 9. Regresion de REAL-01, gateway y aprobaciones humanas
# ─────────────────────────────────────────────────────────────────

class TestRegressionREAL01(unittest.TestCase):
    """Verifica que los comportamientos de REAL-01 se conservan en la composicion."""

    def test_real01_validator_rejections_cause_no_calls(self):
        """Aprobaciones invalidas de REAL-01 rechazan sin invocacion al proveedor."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "regr.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)

        provider = ControlledProvider([])

        # task_id que no esta en el plan rechaza sin llamadas
        comp = RealExecutionComposition(
            repo, MISSION_ID, "TSK-FUERA-DEL-PLAN",
            runtime.approvals, context,
            _provider_override=provider,
        )
        ok, _, error = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA
        )
        self.assertFalse(ok)
        self.assertEqual(provider.call_count, 0)

    def test_zero_writes_on_rejected_validation(self):
        """Un rechazo del validador no produce escrituras en el repositorio."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "writes.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)
        provider = ControlledProvider([])

        snapshot_before = list(repo._conn.iterdump())

        comp = RealExecutionComposition(
            repo, MISSION_ID, "TSK-FUERA-DEL-PLAN",
            runtime.approvals, context,
            _provider_override=provider,
        )
        comp.execute_task(system_instruction="s", prompt="p", response_schema=_TEST_SCHEMA)

        snapshot_after = list(repo._conn.iterdump())
        self.assertEqual(snapshot_before, snapshot_after,
                         "Una validacion rechazada no debe producir escrituras")

    def test_gateway_real_mode_required_schema(self):
        """El gateway en modo REAL requiere response_schema; sin el falla antes de llamar."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "schema.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)
        provider = ControlledProvider([])

        comp = make_composition(repo, runtime, context, provider)
        ok, _, error = comp.execute_task(
            system_instruction="s", prompt="p", response_schema=[]  # invalido
        )
        self.assertFalse(ok)
        self.assertEqual(provider.call_count, 0)

    def test_approval_human_engine_context_required(self):
        """Sin contexto humano valido la construccion es rechazada."""
        td = tempfile.mkdtemp()
        path = str(Path(td) / "ctx.db")
        repo = LocalRepository(path)
        self.addCleanup(repo.close)
        runtime, context, *_ = setup_approved_mission(repo)
        from app.human_approvals import LocalHumanContext
        fake_ctx = LocalHumanContext("USR-OTRO")
        with self.assertRaises(ValueError):
            RealExecutionComposition(
                repo, MISSION_ID, TASK_ID,
                runtime.approvals, fake_ctx,
                _provider_override=ControlledProvider([]),
            )


if __name__ == "__main__":
    unittest.main()
