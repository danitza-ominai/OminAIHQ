"""REAL-01 – Almacen idempotente durable de llamadas reales.

Componente de producto: DurableCallIdempotencyStore.

Implementa el puerto DurableCallIdempotencyStore de AgentGateway mediante
transacciones y objetos persistidos del repositorio (durable_objects SQLite).

Protocolo de tres estados por clave logica (mission_id, task_id):
- NEW         -> La clave no existia; se registra como IN_PROGRESS antes de
                 ejecutar. El llamador debe ejecutar y luego llamar complete().
- IN_PROGRESS -> La clave existe pero aun no hay resultado terminal. Bloquear.
- REPLAY      -> Existe resultado terminal; devolver sin ejecutar de nuevo.

Invariantes:
- Un resultado terminal (TERMINAL) nunca se sobrescribe.
- begin() y complete() revalidan la mision, tarea, aprobacion y contenido
  persistidos; la huella entregada al constructor no concede autoridad.
- Si el contenido autorizado cambia, begin() devuelve CONTENT_CHANGED en lugar
  de recuperar o reiniciar el registro; la discrepancia requiere revision.
- Las transacciones SQLite garantizan exclusion mutua entre hilos concurrentes.

Contratos aplicados:
- CONTRATO-MVP-v1.md ss4.3 (idempotencia), RF-022, RNF-005, RNF-006.
- AGENTS.md: No impone Firestore; compatible con SQLite en pruebas.
"""

from __future__ import annotations

import re
from typing import Optional, Tuple

from app.agent_gateway import (
    DurableCallIdempotencyStore,
    PersistedCallOutcome,
    ValidatedRealExecutionMandate,
)

# Prefijo de namespace para los objetos en durable_objects.
_KIND = "real_call_idempotency"

# Estados internos persistidos en el payload.
_STATE_IN_PROGRESS = "IN_PROGRESS"
_STATE_TERMINAL = "TERMINAL"
_SHA256_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")


def _make_key(mission_id: str, task_id: str) -> str:
    """Clave compuesta unica e inequivoca para la dupla (mision, tarea)."""
    return f"{mission_id}::{task_id}"


def _valid_identity(value: object) -> bool:
    return isinstance(value, str) and bool(value) and value == value.strip()


def _valid_fingerprint(value: object) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None


class RepositoryDurableCallStore(DurableCallIdempotencyStore):
    """Almacen idempotente durable sobre las transacciones del repositorio.

    Parametros
    ----------
    repository:
        Instancia de LocalRepository ya inicializada. Inyeccion explicita
        obligatoria.
    authorized_content_fingerprint : str
        Huella SHA-256 esperada del contenido concreto autorizado para la llamada.
        Una huella ausente o invalida falla cerrado; una huella diferente de
        la aprobacion persistida o de la adquirida impide recuperar o completar.
        Este valor por si solo nunca concede autoridad.
    authorization_validator:
        Validador de producto que comprueba en cada operacion la mision, tarea
        y aprobacion persistidas. Por defecto se usa LocalApprovalRecordValidator.

    Nota: esta clase no es una cache en memoria. Cada operacion lee y escribe
    en el repositorio SQLite para garantizar durabilidad entre reinicios.
    """

    def __init__(
        self,
        repository,
        *,
        authorized_content_fingerprint: Optional[str] = None,
        authorization_validator=None,
    ) -> None:
        if repository is None:
            raise ValueError("INVALID_INPUT: El repositorio es obligatorio.")
        if authorization_validator is None:
            from app.real_execution_authority import LocalApprovalRecordValidator

            authorization_validator = LocalApprovalRecordValidator(repository)
        self._repo = repository
        self._authorized_fp = authorized_content_fingerprint
        self._authorization_validator = authorization_validator

    def _current_authorized_fingerprint(
        self,
        mission_id: str,
        task_id: str,
    ) -> Optional[str]:
        """Lee y valida la autoridad vigente dentro de la transaccion llamadora."""
        mission = self._repo.get_mission(mission_id)
        if not isinstance(mission, dict):
            return None
        owner_id = mission.get("user_id")
        approval_id = mission.get("approval_id")
        if not _valid_identity(owner_id) or not _valid_identity(approval_id):
            return None

        mandate = self._authorization_validator.validate(
            mission_id=mission_id,
            task_id=task_id,
            owner_id=owner_id,
            approval_id=approval_id,
        )
        if (
            not isinstance(mandate, ValidatedRealExecutionMandate)
            or mandate.mission_id != mission_id
            or mandate.task_id != task_id
            or mandate.owner_id != owner_id
            or mandate.approval_id != approval_id
            or mandate.decision != "APROBAR"
            or mandate.persisted is not True
            or mandate.is_current is not True
        ):
            return None

        envelope = self._repo.get_object("approval_request", approval_id)
        if not isinstance(envelope, dict):
            return None
        request = envelope.get("request")
        if not isinstance(request, dict):
            return None
        fingerprint = request.get("fingerprint")
        if (
            request.get("approval_id") != approval_id
            or request.get("mission_id") != mission_id
            or request.get("gate_type") != "GATE_1_PLAN"
            or not _valid_fingerprint(fingerprint)
        ):
            return None
        return fingerprint

    # ------------------------------------------------------------------
    # Interfaz publica (contrato DurableCallIdempotencyStore)
    # ------------------------------------------------------------------

    def begin(
        self,
        *,
        mission_id: str,
        task_id: str,
    ) -> Tuple[str, Optional[PersistedCallOutcome]]:
        """Intenta adquirir la clave idempotente para (mission_id, task_id).

        Devuelve una tupla (estado, resultado_o_None):
        - ("NEW", None)             -> Clave nueva; registrada como IN_PROGRESS.
        - ("IN_PROGRESS", None)     -> Clave en curso; bloquear sin reintentar.
        - ("REPLAY", outcome)       -> Resultado terminal disponible.
        - ("CONTENT_CHANGED", None) -> Contenido aprobado alterado; rechazar.
        - ("ERROR", None)           -> Error de repositorio o invariante roto.

        La transaccion SQLite garantiza exclusion mutua: si dos hilos
        concurrentes llaman a begin() con la misma clave, solo uno recibe NEW.
        """
        if not _valid_identity(mission_id) or not _valid_identity(task_id):
            return "ERROR", None
        if not _valid_fingerprint(self._authorized_fp):
            return "ERROR", None

        key = _make_key(mission_id, task_id)

        try:
            with self._repo.transaction():
                current_fp = self._current_authorized_fingerprint(
                    mission_id, task_id
                )
                if current_fp is None:
                    return "ERROR", None
                if current_fp != self._authorized_fp:
                    return "CONTENT_CHANGED", None

                record = self._repo.get_object(_KIND, key)

                if record is None:
                    # Primera vez: registrar como IN_PROGRESS antes de ejecutar.
                    self._repo.put_object(_KIND, key, {
                        "state": _STATE_IN_PROGRESS,
                        "mission_id": mission_id,
                        "task_id": task_id,
                        "authorized_fp": current_fp,
                        "outcome": None,
                    })
                    return "NEW", None

                if not isinstance(record, dict):
                    return "ERROR", None
                if record.get("mission_id") != mission_id or record.get("task_id") != task_id:
                    return "ERROR", None
                stored_fp = record.get("authorized_fp")
                if not _valid_fingerprint(stored_fp):
                    return "ERROR", None
                if stored_fp != current_fp:
                    return "CONTENT_CHANGED", None

                state = record.get("state")
                if state == _STATE_TERMINAL:
                    raw = record.get("outcome")
                    if not isinstance(raw, dict):
                        # Registro TERMINAL sin outcome valido: corrupto.
                        return "ERROR", None

                    outcome = PersistedCallOutcome(
                        ok=raw.get("ok", False),
                        result=raw.get("result"),
                        error=raw.get("error"),
                    )
                    return "REPLAY", outcome

                if state == _STATE_IN_PROGRESS:
                    return "IN_PROGRESS", None

                # Estado desconocido: fallo cerrado.
                return "ERROR", None

        except Exception:
            return "ERROR", None

    def complete(
        self,
        *,
        mission_id: str,
        task_id: str,
        outcome: PersistedCallOutcome,
    ) -> None:
        """Registra el resultado terminal de la llamada.

        Precondicion: begin() ya fue llamado y devolvio "NEW" para esta clave.
        Si el registro no existe o no esta en estado IN_PROGRESS, lanza
        ValueError (no sobrescribe resultados terminales).

        Raises
        ------
        ValueError
            Si la clave no fue reclamada, ya tiene un resultado terminal, o
            si ocurre un error de repositorio.
        """
        if not isinstance(outcome, PersistedCallOutcome):
            raise ValueError("INVALID_INPUT: outcome debe ser PersistedCallOutcome.")
        if not _valid_identity(mission_id) or not _valid_identity(task_id):
            raise ValueError("INVALID_INPUT: Identidad de llamada invalida.")
        if not _valid_fingerprint(self._authorized_fp):
            raise ValueError("INVALID_INPUT: Huella autorizada ausente o invalida.")

        key = _make_key(mission_id, task_id)

        try:
            with self._repo.transaction():
                current_fp = self._current_authorized_fingerprint(
                    mission_id, task_id
                )
                if current_fp is None:
                    raise ValueError(
                        "PERMISSION_DENIED: La autoridad de ejecucion ya no esta vigente."
                    )
                if current_fp != self._authorized_fp:
                    raise ValueError(
                        "PERMISSION_DENIED: El contenido aprobado vigente cambio."
                    )

                record = self._repo.get_object(_KIND, key)

                if record is None:
                    raise ValueError(
                        "INVALID_INPUT: Clave no registrada; llame a begin() primero."
                    )

                if not isinstance(record, dict):
                    raise ValueError("INVALID_INPUT: Registro de llamada corrupto.")
                if record.get("mission_id") != mission_id or record.get("task_id") != task_id:
                    raise ValueError("INVALID_INPUT: Identidad adquirida no coincide.")
                stored_fp = record.get("authorized_fp")
                if not _valid_fingerprint(stored_fp) or stored_fp != current_fp:
                    raise ValueError("INVALID_INPUT: Huella adquirida no coincide.")

                if record.get("state") == _STATE_TERMINAL:
                    raise ValueError(
                        "INVALID_INPUT: El resultado terminal ya esta persistido; "
                        "no se sobrescribe."
                    )

                if record.get("state") != _STATE_IN_PROGRESS:
                    raise ValueError(
                        f"INVALID_INPUT: Estado inesperado '{record.get('state')}'; "
                        "no se puede completar."
                    )

                self._repo.put_object(_KIND, key, {
                    "state": _STATE_TERMINAL,
                    "mission_id": record["mission_id"],
                    "task_id": record["task_id"],
                    "authorized_fp": stored_fp,
                    "outcome": {
                        "ok": outcome.ok,
                        "result": outcome.result,
                        "error": outcome.error,
                    },
                })

        except ValueError:
            raise
        except Exception as exc:
            raise ValueError(
                f"SYSTEM_ERROR: No se pudo persistir el resultado terminal: {exc}"
            ) from exc
