"""Loopback-only adapter for the durable SIMULADA runtime. No production authentication."""
import http.server
import json
import os
import re
import secrets
import socket
import sys
import time
from pathlib import Path
from typing import Optional

from app import api_contracts, hq_runtime, local_repository, vbp_document, vbp_export
from app.human_approvals import HumanApprovalError

STATIC_WEB_DIR = Path(__file__).resolve().parent.parent / "web"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000


class PreparedDownload(tuple):
    """Preparation is not delivery. The server invokes the private completion hook.

    A successful socket write/flush is not proof that a user saved the file.
    No client field or public endpoint can invoke this hook.
    """
    def __new__(cls, status, headers, payload, on_delivered):
        result = super().__new__(cls, (status, headers, payload))
        result.on_delivered = on_delivered
        return result


class LocalAPIRouter:
    def __init__(self, runtime=None, web_dir=None, demo_policy_manager=None, *, local_context=None):
        self.runtime = runtime or hq_runtime.HQRuntime()
        self.web_dir = web_dir or STATIC_WEB_DIR
        self.local_context = local_context
        self.csrf_token = secrets.token_urlsafe(32)

    def response(self, code, data=None, error=None):
        return code, {"Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store"}, json.dumps(
            api_contracts.format_api_response(code, data=data, error=error), ensure_ascii=False
        ).encode("utf-8")

    def outcome(self, result, success_code=200):
        ok, data, error = result
        if ok:
            return self.response(success_code, data)
        code = 403 if "PERMISSION_DENIED" in str(error) else 404 if "NOT_FOUND" in str(error) else 500 if "SYSTEM_ERROR" in str(error) else 409
        return self.response(code, error=error)

    def dispatch(self, method, path, headers, body_bytes=b""):
        ok, err = api_contracts.validate_request_security(headers)
        if not ok:
            return self.response(403, error=err)
        ok, err = api_contracts.validate_request_body_size(body_bytes)
        if not ok:
            return self.response(413, error=err)
        headers = {k.lower(): v for k, v in headers.items()}
        try:
            if method == "GET" and path in ("/", "/index.html", "/styles.css", "/app.js", "/i18n.js"):
                filename = "index.html" if path == "/" else path[1:]
                file = self.web_dir / filename
                return 200, {"Content-Type": api_contracts.STATIC_MIME_TYPES[file.suffix],
                             "X-Content-Type-Options": "nosniff",
                             "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"}, file.read_bytes()
        except Exception:
            return self.response(500, error="SYSTEM_ERROR: Recurso local no disponible.")
        return self._dispatch_api(method, path, headers, body_bytes)

    def _dispatch_api(self, method, path, headers, body_bytes):
        try:
            if method == "GET" and path == "/health":
                return self.response(200, {"status": "UP", "mode": "SIMULADA", "version": "0.1.0", "port": 8000})
            if any(k in headers for k in ("x-ominai-actor-role", "x-ominai-user-id")):
                return self.response(403, error="PERMISSION_DENIED: Headers de identidad no otorgan autoridad.")
            if not self.runtime.approvals.check_context(self.local_context):
                return self.response(403, error="PERMISSION_DENIED: Falta contexto humano local valido.")
            if method == "GET" and path == "/api/v1/session":
                return self.response(200, {"csrf_token": self.csrf_token, "mode": "SIMULADA"})
            if method == 'GET' and path == '/api/v1/missions/current':
                return self.response(200, self.runtime.repository.current_mission_for_owner(self.local_context.user_id))
            if method == 'GET' and path == '/api/v1/demo-template':
                return self.response(200, {'fields':vbp_document.prepared_demo_fields(), 'english':vbp_document.DEMO_TEXT_EN})
            if method in ("POST", "DELETE", "PUT", "PATCH"):
                if (headers.get("origin") not in api_contracts.ALLOWED_ORIGINS
                    or not secrets.compare_digest(headers.get("x-ominai-csrf", ""), self.csrf_token)):
                    return self.response(403, error="PERMISSION_DENIED: Proteccion CSRF requerida.")
                if body_bytes and headers.get("content-type", "").split(";")[0] != "application/json":
                    return self.response(415, error="INVALID_INPUT: Se requiere application/json.")
            try:
                body = json.loads(body_bytes) if body_bytes else {}
                if not isinstance(body, dict):
                    raise ValueError()
            except (ValueError, UnicodeError):
                return self.response(400, error="INVALID_INPUT: JSON debe ser un objeto.")
            if any(k in body for k in ("actor_role", "actor_user_id", "user_id", "actor_context", "context_humano")):
                return self.response(403, error="PERMISSION_DENIED: Identidad declarada no autorizada.")
            ctx = self.local_context
            if method == "GET" and path == "/api/v1/profile":
                profile = self.runtime.repository.get_profile(ctx.user_id)
                if not profile:
                    return self.response(403, error="PERMISSION_DENIED: Perfil no disponible.")
                return self.response(200, profile)
            if path == "/api/v1/memory":
                if method == "GET":
                    # Human administrative view, not a forged specialist role.
                    memories = []
                    for memory in self.runtime.memory.memories.values():
                        if 'deleted_at' in memory:
                            continue
                        origin = self.runtime.repository.get_mission(memory["origin_mission_id"])
                        if origin and origin.get("user_id") == ctx.user_id:
                            memories.append({**memory, "fact_text": memory.get("content", ""),
                                             'blocked': bool(self.runtime.memory._blocked(memory))})
                    return self.response(200, memories)
                if method == "POST":
                    if set(body) - {"fact_text", "mission_id", "category", 'review_at', 'review_required', 'conflict', 'material_impact'}:
                        return self.response(400, error="INVALID_INPUT: La propuesta no admite autoaprobacion.")
                    mission = self.runtime.repository.get_mission(body.get("mission_id", ""))
                    if not mission:
                        return self.response(404, error="NOT_FOUND: Mision de origen inexistente.")
                    if mission.get("user_id") != ctx.user_id:
                        return self.response(403, error="PERMISSION_DENIED: Propietario distinto.")
                    return self.outcome(self.runtime.memory.propose_memory(
                        body.get("category", "PREFERENCIA"), body.get("fact_text", ""),
                        body["mission_id"], human_approved=False, context=ctx,
                        **{key:body[key] for key in ('review_at','review_required','conflict','material_impact') if key in body}), 201)
            memory_match = re.fullmatch(r'/api/v1/memory/([A-Za-z0-9_-]+)(/approve)?', path)
            if memory_match and method in ('PUT', 'POST'):
                memid, approve = memory_match.groups()
                allowed = {'version', 'resolve_blockers', 'review_at'} if approve else {'version', 'fact_text'}
                if set(body) - allowed or type(body.get('version')) is not int:
                    return self.response(400, error='INVALID_INPUT: Version exacta y campos permitidos requeridos.')
                if approve and method == 'POST':
                    ok = self.runtime.memory.approve_memory(memid, context=ctx, version=body['version'],
                        resolve_blockers=body.get('resolve_blockers', False), review_at=body.get('review_at'))
                    return self.response(200, {'memory_id':memid, 'approved_version':body['version']}) if ok else self.response(409, error='PERMISSION_DENIED: Memoria, version o revision no autorizada.')
                if not approve and method == 'PUT':
                    return self.outcome(self.runtime.memory.update_memory(memid, body.get('fact_text'), context=ctx, version=body['version']))
            if method == "DELETE" and path.startswith("/api/v1/memory/"):
                mid = path.rsplit("/", 1)[-1]
                memory = self.runtime.memory.memories.get(mid)
                if not memory:
                    return self.response(404, error="NOT_FOUND: Memoria inexistente.")
                origin = self.runtime.repository.get_mission(memory["origin_mission_id"])
                if not origin or origin.get("user_id") != ctx.user_id:
                    return self.response(403, error="PERMISSION_DENIED: Propietario distinto.")
                if body != {"confirm_memory_id": mid, "version": memory.get("version")}:
                    return self.response(400, error="INVALID_INPUT: Confirme el identificador exacto.")
                if not self.runtime.memory.delete_memory(mid, context=ctx, version=body.get("version")):
                    return self.response(409, error="INVALID_INPUT: Memoria no eliminada.")
                return self.response(200, {"deleted_memory_id": mid})
            if method == "POST" and path == "/api/v1/missions":
                return self.outcome(self.runtime.create_local_mission(body, ctx), 201)
            match = re.fullmatch(r"/api/v1/missions/([A-Za-z0-9_-]+)(/.*)?", path)
            if not match:
                return self.response(404, error="NOT_FOUND: Ruta inexistente.")
            mid, sub = match[1], match[2] or ""
            mission = self.runtime.repository.get_mission(mid)
            if not mission:
                return self.response(404, error="NOT_FOUND: Mision inexistente.")
            if mission.get("user_id") != ctx.user_id:
                return self.response(403, error="PERMISSION_DENIED: Propietario distinto.")
            if method == "GET" and sub == "":
                return self.response(200, {**mission, "budget": self.runtime.repository.budget_snapshot()})
            if method == "GET" and sub == "/plan":
                req = self.runtime.repository.get_object("approval_request", mission.get("pending_GATE_1_PLAN", ""))
                return self.response(200, {"plan": mission.get("plan"), "brief": mission.get("brief"),
                                          "approval_request": req["request"] if req else None,
                                          "fingerprint": req["request"]["fingerprint"] if req else None})
            if method == "POST" and sub == "/decisions":
                if set(body) - {"approval_request", "decision", "comment", "conditions", "risks"}:
                    return self.response(400, error="INVALID_INPUT: Campos de decision no admitidos.")
                request = body.get("approval_request")
                if not isinstance(request, dict) or request.get("mission_id") != mid:
                    return self.response(400, error="INVALID_INPUT: Mision cruzada.")
                return self.outcome(self.runtime.approvals.submit_human_decision(
                    request, body.get("decision"), comment=body.get("comment", ""),
                    conditions=body.get("conditions"), risks=body.get("risks"), context=ctx))
            if method == "POST" and sub == "/renew-approval":
                gate = body.get("gate_type")
                candidate = self.runtime.repository.get_object("candidate", mid + ":" + str(gate))
                if not candidate:
                    return self.response(404, error="NOT_FOUND: Candidato inexistente.")
                result = self.runtime.approvals.create_approval_request(mid, gate, candidate)
                if result[0] and gate == "GATE_2_VBP":
                    mission = self.runtime.repository.get_mission(mid)
                    mission["approval_request"] = result[1]
                    ok, error = self.runtime.repository.save_mission(mission)
                    if not ok:
                        return self.response(500, error="SYSTEM_ERROR: Renovacion no confirmada.")
                return self.outcome(result)
            if method == "POST" and sub in ("/execute", "/execute-step"):
                ok, data, error = self.runtime.execute_local_simulation(mid, ctx, one_step=sub == '/execute-step')
                if not ok:
                    return self.outcome((ok, data, error))
                req = self.runtime.repository.get_object("approval_request", data.get("pending_GATE_2_VBP", ""))
                vbp = self.runtime.repository.get_object("candidate", mid + ":GATE_2_VBP")
                return self.response(200, {**data, "approval_request": req["request"] if req else None,
                                          "vbp_summary": vbp, "budget": self.runtime.repository.budget_snapshot()})
            if method == "POST" and sub in ("/pause", "/cancel", "/resume"):
                return self.outcome(self.runtime.control_local_mission(mid, sub[1:], ctx, body.get("reason", "")))
            if method == "GET" and sub == "/tasks":
                return self.response(200, {"tasks": mission.get("tasks", []), "task_results": mission.get("task_results", {}),
                                          "agent_requests": mission.get("agent_requests"), "budget": self.runtime.repository.budget_snapshot()})
            if method == "GET" and sub == "/evidence":
                return self.response(200, {eid: self.runtime.repository.get_object("evidence", eid) for eid in mission.get("evidence_ids", [])})
            if method == "GET" and sub == "/audit":
                return self.response(200, self.runtime.audit_engine.reconstruct_trajectory(mid))
            if method == "GET" and sub in ("/vbp", "/vbp/export", "/vbp/download"):
                vbp = self.runtime.repository.get_object("candidate", mid + ":GATE_2_VBP")
                if not vbp:
                    return self.response(404, error="NOT_FOUND: VBP no disponible.")
                if sub == "/vbp":
                    return self.response(200, {"vbp_data": vbp, "canonical_markdown": vbp_document.render_canonical_markdown(vbp),
                                              "evaluation_report": mission.get("evaluation_report"), "fingerprint": vbp["fingerprint"]})
                ok, raw, meta, err = vbp_export.export_canonical_vbp_bytes(vbp, repository=self.runtime.repository)
                if not ok:
                    return self.response(409, error=err)
                def delivered():
                    try:
                        with self.runtime.repository.transaction():
                            current = self.runtime.repository.get_mission(mid)
                            stored = self.runtime.repository.get_object('candidate', mid + ':GATE_2_VBP')
                            valid, again, _, _ = vbp_export.export_canonical_vbp_bytes(stored, repository=self.runtime.repository)
                            if not valid or again != raw:
                                return False
                            if current['status'] == 'VBP_APROBADO':
                                current.update(status='FINALIZADA', current_state='FINALIZADA')
                                self.runtime._save_runtime_milestone(current, 'EXPORTACION_VERIFICADA')
                            return True
                    except Exception:
                        return False
                return PreparedDownload(200, {"Content-Type": "text/markdown; charset=utf-8", "Cache-Control": "no-store",
                             "Content-Disposition": 'attachment; filename="' + meta["filename"] + '"',
                             "X-Ominai-Fingerprint": meta["manifest_fingerprint"]}, raw, delivered)
            return self.response(404, error="NOT_FOUND: Ruta inexistente.")
        except Exception:
            return self.response(500, error="SYSTEM_ERROR: Operacion no confirmada; revise el estado antes de continuar.")


class OminAIHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    router = None

    def do_GET(self): self._handle_request("GET")
    def do_POST(self): self._handle_request("POST")
    def do_DELETE(self): self._handle_request("DELETE")
    def do_PUT(self): self._handle_request('PUT')
    def do_HEAD(self): self._handle_request("HEAD")

    def _read_bounded_body(self):
        lengths = self.headers.get_all("Content-Length", [])
        if len(lengths) > 1 or self.headers.get("Transfer-Encoding"):
            raise ValueError("INVALID_INPUT")
        raw = lengths[0] if lengths else "0"
        if not re.fullmatch(r"[0-9]{1,8}", raw):
            raise ValueError("INVALID_INPUT")
        length = int(raw)
        if length > api_contracts.MAX_REQUEST_BODY_BYTES:
            raise OverflowError()
        deadline = time.monotonic() + 3
        self.connection.settimeout(0.5)
        chunks = []
        while length:
            if time.monotonic() >= deadline:
                raise TimeoutError()
            chunk = self.rfile.read1(min(length, 4096))
            if not chunk:
                raise ValueError("INVALID_INPUT")
            chunks.append(chunk)
            length -= len(chunk)
        return b"".join(chunks)

    def _handle_request(self, method):
        try:
            body = self._read_bounded_body()
            result = self.router.dispatch(method, self.path, dict(self.headers.items()), body)
        except OverflowError:
            result = self.router.response(413, error="INVALID_INPUT: PAYLOAD_TOO_LARGE.")
        except (TimeoutError, socket.timeout):
            result = self.router.response(408, error="INVALID_INPUT: Tiempo de lectura agotado.")
        except ValueError:
            result = self.router.response(400, error="INVALID_INPUT: Tamano o cuerpo invalido.")
        status, headers, payload = result
        self.close_connection = True
        try:
            self.send_response(status)
            for k, v in headers.items(): self.send_header(k, v)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Connection", "close")
            self.end_headers()
            if method != 'HEAD':
                written = self.wfile.write(payload)
                if written != len(payload):
                    return
                self.wfile.flush()
                if isinstance(result, PreparedDownload):
                    result.on_delivered()
        except (OSError, TimeoutError):
            pass  # Prepared bytes alone never finalize the mission.

    def log_message(self, format, *args): pass


def create_local_server(host=DEFAULT_HOST, port=DEFAULT_PORT, router=None):
    if host != DEFAULT_HOST or port != DEFAULT_PORT:
        raise ValueError("Solo 127.0.0.1:8000 esta autorizado.")
    if router is None:
        raise ValueError("Configure explicitamente repositorio y adaptador local.")
    handler = type("IsolatedLocalHandler", (OminAIHTTPRequestHandler,), {"router": router})
    return http.server.HTTPServer((host, port), handler)


def run_local_server(host=DEFAULT_HOST, port=DEFAULT_PORT, router=None):
    server = create_local_server(host, port, router)
    print("OminAI HQ - SIMULADA - http://127.0.0.1:8000", flush=True)
    server.timeout = 0.5
    deadline = time.monotonic() + 45 * 60
    try:
        while time.monotonic() < deadline:
            server.handle_request()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    db = os.environ.get("OMINAI_LOCAL_DB")
    if not db or db == ":memory:" or not Path(db).is_absolute() or os.environ.get("OMINAI_LOCAL_DEMO") != "1":
        sys.exit("Configure OMINAI_LOCAL_DB absoluto y OMINAI_LOCAL_DEMO=1. No se abrira una base por defecto.")
    repo = local_repository.LocalRepository(db)
    runtime = hq_runtime.HQRuntime(repository=repo)
    context = runtime.approvals.bind_local_profile({
        "user_id": "USR-LOCAL-DEMO", "display_name": "Usuario local SIMULADA", "actor_role": "usuario_humano",
    })
    try:
        run_local_server(router=LocalAPIRouter(runtime=runtime, local_context=context))
    finally:
        repo.close()
