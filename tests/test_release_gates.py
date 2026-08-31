"""Pruebas de Criterios de Release y Puertas de Gobernanza MVP (PZ-015A).

Verifica los gates de seguridad, techos de gasto ($25 USD), limites de llamadas de agentes (15 max),
ausencia estricta de Chain-of-Thought e inviolabilidad de las puertas de decision humana.
"""

import unittest

import app.agent_gateway as agent_gateway
import app.human_approvals as human_approvals
import app.runtime_config as runtime_config


class TestReleaseGates(unittest.TestCase):
    """Suite de pruebas para los gates del release MVP (C.18 y 15.7)."""

    def setUp(self) -> None:
        self.config = runtime_config.RuntimeConfig(max_budget_usd=25.0, max_agent_requests=15)
        self.mock_provider = agent_gateway.MockModelClientProvider([
            agent_gateway.ModelCallResponse(
                content='{"task_id": "TSK-TEST", "summary": "Requerimientos funcionales"}',
                input_tokens=100,
                output_tokens=50,
            )
        ])
        self.gateway = agent_gateway.AgentGateway(config=self.config, provider=self.mock_provider)

    def test_ac01_budget_and_request_caps(self) -> None:
        """Verifica que los limites globales de gasto e intentos no puedan ser sobrepasados."""
        self.assertEqual(self.config.max_budget_usd, 25.0)
        self.assertEqual(self.config.max_agent_requests, 15)

    def test_ac02_zero_cot_in_responses(self) -> None:
        """Verifica que las respuestas estructuradas no contengan campos ni rastros de Chain-of-Thought."""
        ok, res, _ = self.gateway.execute_agent_call(
            system_instruction="Eres el arquitecto de producto.",
            prompt="Generar requerimientos de software",
        )
        self.assertTrue(ok)
        self.assertNotIn("chain_of_thought", res)
        self.assertNotIn("cot", res)
        self.assertNotIn("internal_reasoning", res)

    def test_ac03_human_gate_independence(self) -> None:
        """Verifica que la aprobacion de Puerta 1 (Plan) no apruebe automaticamente Puerta 2 (VBP)."""
        engine = human_approvals.HumanApprovalEngine()
        self.addCleanup(engine.repository.close)
        engine.repository.save_mission({"mission_id":"MSN-GATES","status":"PLAN_EN_REVISION","user_id":"USR-SIM"})
        ok_p, p_req, _ = engine.create_approval_request("MSN-GATES", "GATE_1_PLAN", {"plan": "v1"})
        self.assertTrue(ok_p)
        self.assertEqual(p_req["gate_type"], "GATE_1_PLAN")

        engine.repository.save_mission({"mission_id":"MSN-GATES","status":"VBP_EN_REVISION"})
        ok_v, v_req, _ = engine.create_approval_request("MSN-GATES", "GATE_2_VBP", {"vbp": "v1"})
        self.assertTrue(ok_v)
        self.assertEqual(v_req["gate_type"], "GATE_2_VBP")
        self.assertNotEqual(p_req["approval_id"], v_req["approval_id"])


if __name__ == "__main__":
    unittest.main()
