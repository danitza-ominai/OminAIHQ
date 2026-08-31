"""OminAI HQ - Politicas y Repositorio de Demo Publica Cloud (PZ-014A).

Implementa el control de cupo diario (5 ejecuciones maximas por dia), aislamiento
de datos publicos frente a datos privados, y persistencia transaccional del contador
conforme a CONTRATO-MVP-v1.md seccion 11.2, 11.4, 11.9 y PT-007/008.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

import app.local_repository as local_repository

DAILY_DEMO_EXECUTION_LIMIT = 5


class CloudDemoPolicyManager:
    """Gestiona los limites de cuota de demo publica y aislamiento de ejecucion."""

    def __init__(
        self,
        repository: Optional[local_repository.LocalRepository] = None,
        daily_limit: int = DAILY_DEMO_EXECUTION_LIMIT,
    ) -> None:
        self.repository = repository or local_repository.LocalRepository()
        self.daily_limit = daily_limit
        self._init_table()

    def _init_table(self) -> None:
        """Crea la tabla de ejecuciones de demo si no existe."""
        with self.repository._conn:
            self.repository._conn.execute("""
                CREATE TABLE IF NOT EXISTS demo_quota (
                    quota_date TEXT PRIMARY KEY,
                    executions_count INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL
                );
            """)

    def _get_today_str(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def get_today_executions_count(self, today_str: Optional[str] = None) -> int:
        """Obtiene la cantidad de ejecuciones realizadas en la fecha indicada."""
        d_str = today_str or self._get_today_str()
        cur = self.repository._conn.execute(
            "SELECT executions_count FROM demo_quota WHERE quota_date = ?;",
            (d_str,),
        )
        row = cur.fetchone()
        return row["executions_count"] if row else 0

    def try_acquire_demo_execution(self, today_str: Optional[str] = None) -> Tuple[bool, int, Optional[str]]:
        """Intenta registrar una nueva ejecucion publica respetando el limite de 5 por dia."""
        d_str = today_str or self._get_today_str()
        now_iso = datetime.now(timezone.utc).isoformat()

        with self.repository._conn:
            cur = self.repository._conn.execute(
                "SELECT executions_count FROM demo_quota WHERE quota_date = ?;",
                (d_str,),
            )
            row = cur.fetchone()
            current_count = row["executions_count"] if row else 0

            if current_count >= self.daily_limit:
                return (
                    False,
                    current_count,
                    f"CUOTA_DEMO_DIARIA_AGOTADA: Limite diario de {self.daily_limit} ejecuciones alcanzado para {d_str}. Solo disponible lectura de ejemplos.",
                )

            new_count = current_count + 1
            self.repository._conn.execute(
                """
                INSERT INTO demo_quota (quota_date, executions_count, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(quota_date) DO UPDATE SET
                    executions_count = excluded.executions_count,
                    updated_at = excluded.updated_at;
                """,
                (d_str, new_count, now_iso),
            )

        return True, new_count, None
