"""OminAI HQ - Harness Versionado de Evaluacion y Separacion de Holdout (PZ-011A).

Implementa el motor de benchmark determinista offline para evaluar el comportamiento
del runtime y los especialistas frente a las 10 categorias de casos del contrato
conforme a CONTRATO-MVP-v1.md seccion 11.8, PT-005 y CT-010-012.
"""

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import app.evaluation_report as evaluation_report


class EvaluationHarnessError(Exception):
    """Excepcion controlada en el harness de evaluacion."""
    pass


class EvaluationHarness:
    """Motor de ejecucion y calificacion de benchmarks versionados."""

    def __init__(
        self,
        manifest_path: str = "evaluation/dataset_manifest.json",
        report_generator: Optional[evaluation_report.EvaluationReportGenerator] = None,
    ) -> None:
        self.manifest_path = Path(manifest_path)
        self.report_generator = report_generator or evaluation_report.EvaluationReportGenerator()

    def load_manifest(self) -> Tuple[bool, Optional[dict], Optional[str]]:
        """Carga y valida el manifest de datasets."""
        if not self.manifest_path.exists():
            return False, None, f"Manifest no encontrado en {self.manifest_path}."

        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return True, data, None
        except Exception as e:
            return False, None, f"Fallo al leer manifest: {str(e)}"

    def load_dev_cases(self, base_dir: Optional[str] = None) -> Tuple[bool, List[dict], Optional[str]]:
        """Carga los casos de desarrollo verificando estrictamente la huella SHA-256 declarada en el manifest."""
        ok_m, manifest, err_m = self.load_manifest()
        if not ok_m or not manifest:
            return False, [], err_m

        dev_spec = manifest.get("splits", {}).get("development", {})
        rel_file = dev_spec.get("file", "evaluation/dev_cases.json")
        expected_hash = dev_spec.get("sha256")

        dev_path = (Path(base_dir) / rel_file) if base_dir else Path(rel_file)
        if not dev_path.exists():
            return False, [], f"Archivo de casos de desarrollo {dev_path} no encontrado."

        try:
            with open(dev_path, "rb") as f:
                raw_bytes = f.read()

            actual_hash = hashlib.sha256(raw_bytes).hexdigest()
            if actual_hash != expected_hash:
                return False, [], f"CHECKSUM_MISMATCH: La huella de {dev_path} ({actual_hash}) no coincide con el manifest ({expected_hash})."

            cases = json.loads(raw_bytes.decode("utf-8"))
            return True, cases, None
        except Exception as e:
            return False, [], f"Fallo al procesar casos de desarrollo: {str(e)}"

    def sanitize_agent_input(self, case: dict) -> dict:
        """Aisla exclusivamente los datos de entrada para el agente, eliminando expectativas del evaluador."""
        return copy.deepcopy(case.get("input_mission", {}))

    def evaluate_case(self, case: dict, runner_fn: Callable[[dict], dict]) -> dict:
        """Ejecuta un caso individual entregando solo la entrada saneada y calificando la respuesta."""
        agent_input = self.sanitize_agent_input(case)
        try:
            actual_result = runner_fn(agent_input)
        except Exception as e:
            actual_result = {
                "verdict": "UNHANDLED_EXCEPTION",
                "state": "ERROR",
                "error": str(e),
            }

        expected_verdict = case.get("expected_verdict")
        expected_state = case.get("expected_state")

        actual_verdict = actual_result.get("verdict")
        actual_state = actual_result.get("state")

        # Verificar presencia de bloqueadores o uso de herramientas prohibidas en resultado
        blockers = self.report_generator.screen_adversarial_blockers(
            candidate_output=actual_result,
            used_prohibited_tools=bool(actual_result.get("used_prohibited_tools")),
            missing_human_approval=bool(actual_result.get("missing_human_approval")),
            fake_evidence_detected=bool(actual_result.get("fake_evidence_detected")),
        )

        verdict_ok = actual_verdict == expected_verdict
        state_ok = (expected_state is None) or (actual_state == expected_state)
        # Si el caso esperaba un veredicto de exito/pasa pero contiene bloqueadores no declarados, rechazar
        if blockers and expected_verdict in ("SUCCESS", "PASA", "AUTORIZADA_PARA_EJECUTAR"):
            passed = False
        else:
            passed = verdict_ok and state_ok

        return {
            "case_id": case.get("case_id"),
            "category": case.get("category"),
            "passed": passed,
            "expected_verdict": expected_verdict,
            "actual_verdict": actual_verdict,
            "expected_state": expected_state,
            "actual_state": actual_state,
            "blockers_detected": blockers,
            "score": 1.0 if passed else 0.0,
        }

    def run_benchmark(
        self,
        cases: List[dict],
        runner_fn: Callable[[dict], dict],
        holdout_cases: Optional[List[dict]] = None,
    ) -> dict:
        """Ejecuta la suite completa de desarrollo y opcionalmente el set holdout reservado."""
        results = []
        category_stats: Dict[str, dict] = {}

        for case in cases:
            res = self.evaluate_case(case, runner_fn)
            results.append(res)
            cat = res["category"]
            if cat not in category_stats:
                category_stats[cat] = {"total": 0, "passed": 0}
            category_stats[cat]["total"] += 1
            if res["passed"]:
                category_stats[cat]["passed"] += 1

        total_cases = len(results)
        passed_cases = sum(1 for r in results if r["passed"])
        accuracy = (passed_cases / total_cases) if total_cases > 0 else 0.0

        holdout_results = []
        if holdout_cases:
            for hcase in holdout_cases:
                hres = self.evaluate_case(hcase, runner_fn)
                holdout_results.append(hres)

        return {
            "total_cases_evaluated": total_cases,
            "passed_cases": passed_cases,
            "accuracy": accuracy,
            "category_breakdown": category_stats,
            "holdout_evaluated": bool(holdout_cases),
            "holdout_status": "COMPLETO" if holdout_cases else "HOLDOUT_NO_PROPORCIONADO_EVALUACION_PARCIAL",
            "results": results,
            "holdout_results": holdout_results,
        }
