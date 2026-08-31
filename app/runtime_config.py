"""Configuracion no secreta de los modos SIMULADA y REAL del gateway."""

from decimal import Decimal, ROUND_CEILING
import os
from pathlib import Path
from typing import Dict, Optional, Tuple


GLOBAL_MAX_BUDGET_USD = 25.0
MAX_AGENT_REQUESTS_PER_MISSION = 15
DEFAULT_TIMEOUT_SECONDS = 300
DEFAULT_MAX_RETRIES = 1

SIMULATED_MODE = "SIMULADA"
REAL_MODE = "REAL"
REAL_MODEL_ID = "gemini-3.5-flash"
REAL_PRICE_SOURCE = "https://ai.google.dev/gemini-api/docs/pricing"
REAL_PRICE_CHECKED_ON = "2026-08-31"

# Fixtures historicos. No representan precios actuales ni autorizan gasto.
MODEL_PRICING: Dict[str, Tuple[float, float]] = {
    "gemini-2.5-pro": (1.25, 5.00),
    "gemini-2.5-flash": (0.15, 0.60),
}

# Gemini Developer API, tarifa Standard consultada en la fecha indicada.
# La salida incluye los tokens de pensamiento.
REAL_MODEL_PRICING: Dict[str, Tuple[float, float]] = {
    REAL_MODEL_ID: (1.50, 9.00),
}

BUDGET_THRESHOLDS = [0.70, 0.90, 1.00]


def configured_repository_path():
    """Evita que una demo configurada caiga en un ledger aislado."""
    path = os.environ.get("OMINAI_LOCAL_DB")
    if os.environ.get("OMINAI_LOCAL_DEMO") == "1" or path:
        if not path or path == ":memory:" or not Path(path).is_absolute():
            raise ValueError(
                "INVALID_INPUT: La demo integrada requiere OMINAI_LOCAL_DB absoluto."
            )
        return str(Path(path).resolve())
    return ":memory:"


class RuntimeConfig:
    """Perfil del runtime; no concede por si mismo permiso de red o gasto."""

    def __init__(
        self,
        model_id: Optional[str] = None,
        fallback_model_id: str = "gemini-2.5-flash",
        max_budget_usd: float = GLOBAL_MAX_BUDGET_USD,
        max_agent_requests: int = MAX_AGENT_REQUESTS_PER_MISSION,
        timeout_seconds: Optional[int] = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        pricing_table: Optional[Dict[str, Tuple[float, float]]] = None,
        is_demo_mode: bool = False,
        daily_demo_execution_limit: int = 5,
        execution_mode: str = SIMULATED_MODE,
        max_input_tokens: int = 4096,
        max_output_tokens: int = 4096,
    ) -> None:
        if execution_mode not in (SIMULATED_MODE, REAL_MODE):
            raise ValueError("INVALID_INPUT: Modo de proveedor no permitido.")
        self.execution_mode = execution_mode
        self.model_id = model_id or (
            REAL_MODEL_ID if execution_mode == REAL_MODE else "gemini-2.5-pro"
        )
        self.fallback_model_id = fallback_model_id
        self.max_budget_usd = max_budget_usd
        self.max_agent_requests = max_agent_requests
        self.timeout_seconds = timeout_seconds or (
            45 if execution_mode == REAL_MODE else DEFAULT_TIMEOUT_SECONDS
        )
        self.max_retries = min(1, max(0, max_retries))
        self.max_input_tokens = max_input_tokens
        self.max_output_tokens = max_output_tokens
        self.pricing_table = (
            pricing_table
            if pricing_table is not None
            else (REAL_MODEL_PRICING if execution_mode == REAL_MODE else MODEL_PRICING)
        )
        self.pricing_source = (
            REAL_PRICE_SOURCE if execution_mode == REAL_MODE else "FIXTURE_SINTETICO"
        )
        self.pricing_checked_on = (
            REAL_PRICE_CHECKED_ON if execution_mode == REAL_MODE else None
        )
        self.is_demo_mode = is_demo_mode
        self.daily_demo_execution_limit = daily_demo_execution_limit

    def has_valid_credentials(self) -> bool:
        """Solo comprueba presencia; nunca imprime ni persiste el valor."""
        key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        return bool(key and key.strip())

    def validate_real_profile(self) -> Tuple[bool, Optional[str]]:
        """Valida el perfil no secreto antes de reservar o invocar."""
        if self.execution_mode != REAL_MODE:
            return False, "El perfil no selecciona modo REAL."
        if self.model_id != REAL_MODEL_ID:
            return False, "Modelo real fuera de la lista permitida."
        if self.pricing_table.get(self.model_id) != REAL_MODEL_PRICING[self.model_id]:
            return False, "Tarifa real ausente o distinta del perfil fechado."
        if self.pricing_source != REAL_PRICE_SOURCE or not self.pricing_checked_on:
            return False, "Fuente o fecha de tarifa real ausente."
        if not 1 <= self.max_input_tokens <= 4096:
            return False, "Limite de entrada real invalido."
        if not 1 <= self.max_output_tokens <= 4096:
            return False, "Limite de salida real invalido."
        if not 1 <= self.timeout_seconds <= 45:
            return False, "Timeout real invalido."
        if self.max_retries not in (0, 1):
            return False, "Politica de reintentos real invalida."
        return True, None

    def get_pricing(self, model_name: str) -> Tuple[float, float]:
        return self.pricing_table[model_name]

    def calculate_call_cost(
        self, model_name: str, input_tokens: int, output_tokens: int
    ) -> float:
        """Redondea hacia arriba a microdolares para no subreservar."""
        if type(input_tokens) is not int or type(output_tokens) is not int:
            raise ValueError("INVALID_INPUT: Consumo de tokens invalido.")
        if input_tokens < 0 or output_tokens < 0:
            raise ValueError("INVALID_INPUT: Consumo de tokens invalido.")
        in_rate, out_rate = self.get_pricing(model_name)
        amount = (
            Decimal(input_tokens) * Decimal(str(in_rate))
            + Decimal(output_tokens) * Decimal(str(out_rate))
        ) / Decimal(1_000_000)
        return float(amount.quantize(Decimal("0.000001"), rounding=ROUND_CEILING))

    def check_threshold_alert(self, committed_usd: float) -> Optional[float]:
        fraction = (
            committed_usd / self.max_budget_usd if self.max_budget_usd > 0 else 1.0
        )
        for threshold in reversed(BUDGET_THRESHOLDS):
            if fraction >= threshold:
                return threshold
        return None
