"""Pruebas offline del limite ADK; ninguna abre red ni usa credenciales reales."""

import os
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import app.adk_provider as adk_provider
import app.runtime_config as runtime_config


class FakeEvent:
    def __init__(self, text, usage, *, thought_text=None, tool=False, final=True):
        parts = []
        if thought_text:
            parts.append(SimpleNamespace(text=thought_text, thought=True, function_call=None))
        if text is not None:
            parts.append(SimpleNamespace(text=text, thought=False, function_call=None))
        if tool:
            parts.append(SimpleNamespace(text=None, thought=False, function_call=object()))
        self.content = SimpleNamespace(parts=parts)
        self.usage_metadata = usage
        self.error_code = None
        self._final = final
        self._tool = tool

    def is_final_response(self):
        return self._final

    def get_function_calls(self):
        return [object()] if self._tool else []


def usage(prompt=250, candidates=100, thoughts=50, tools=0):
    return SimpleNamespace(
        prompt_token_count=prompt,
        candidates_token_count=candidates,
        thoughts_token_count=thoughts,
        tool_use_prompt_token_count=tools,
    )


class TestADKProvider(unittest.TestCase):
    def test_real_pricing_includes_thinking_as_output(self):
        cfg = runtime_config.RuntimeConfig(execution_mode="REAL")
        self.assertEqual(
            cfg.calculate_call_cost("gemini-3.5-flash", 1000, 500), 0.006
        )
        self.assertEqual(cfg.pricing_checked_on, "2026-08-31")
        self.assertIn("ai.google.dev", cfg.pricing_source)

    def test_real_mode_requires_credential_without_mock_fallback(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as ctx:
                adk_provider.ADKModelClientProvider()
        self.assertIn("fallback a mock prohibido", str(ctx.exception))

    def test_injected_adk_events_normalize_final_text_and_all_output_tokens(self):
        captured = {}

        def executor(**kwargs):
            captured.update(kwargs)
            return [
                FakeEvent(
                    '{"status":"ok"}',
                    usage(),
                    thought_text="razonamiento que no debe salir",
                )
            ]

        provider = adk_provider.ADKModelClientProvider(
            api_key="credencial-sintetica", executor=executor
        )
        result = provider.call_model(
            "gemini-3.5-flash",
            "Sistema",
            "Prompt",
            timeout_seconds=45,
            max_output_tokens=4096,
            response_schema={"type": "object"},
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.input_tokens, 250)
        self.assertEqual(result.output_tokens, 150)
        self.assertNotIn("razonamiento", result.content)
        self.assertEqual(captured["max_output_tokens"], 4096)
        self.assertEqual(captured["response_schema"], {"type": "object"})

    def test_missing_usage_is_indeterminate_and_tool_event_is_rejected(self):
        missing = adk_provider.ADKModelClientProvider(
            api_key="sintetica", executor=lambda **_: [FakeEvent("{}", None)]
        ).call_model(
            "gemini-3.5-flash", "s", "p", response_schema={"type": "object"}
        )
        self.assertFalse(missing.usage_confirmed)

        tool = adk_provider.ADKModelClientProvider(
            api_key="sintetica",
            executor=lambda **_: [FakeEvent("{}", usage(tools=1), tool=True)],
        ).call_model(
            "gemini-3.5-flash", "s", "p", response_schema={"type": "object"}
        )
        self.assertEqual(tool.status_code, 422)
        self.assertTrue(tool.usage_confirmed)

    def test_exception_does_not_expose_secret_and_marks_usage_unknown(self):
        def explode(**_):
            raise RuntimeError("https://endpoint/?key=credencial-secreta")

        result = adk_provider.ADKModelClientProvider(
            api_key="credencial-secreta", executor=explode
        ).call_model(
            "gemini-3.5-flash", "s", "p", response_schema={"type": "object"}
        )
        self.assertFalse(result.usage_confirmed)
        self.assertNotIn("credencial", result.error_message or "")

    def test_401_and_403_exceptions_are_permission_failures_with_unknown_usage(self):
        class ProviderError(Exception):
            def __init__(self, code):
                super().__init__("key=credencial-secreta")
                self.code = code

        for code in (401, 403):
            with self.subTest(code=code):
                def reject(**_):
                    raise ProviderError(code)

                result = adk_provider.ADKModelClientProvider(
                    api_key="credencial-secreta", executor=reject
                ).call_model(
                    "gemini-3.5-flash", "s", "p", response_schema={"type": "object"}
                )
                self.assertEqual(result.status_code, code)
                self.assertFalse(result.usage_confirmed)
                self.assertFalse(result.is_transient)
                self.assertNotIn("credencial", result.error_message or "")

    def test_preflight_requires_exact_pinned_version(self):
        provider = adk_provider.ADKModelClientProvider(api_key="sintetica")
        with patch.object(adk_provider.util, "find_spec", return_value=object()), patch.object(
            adk_provider.metadata, "version", return_value="2.7.1"
        ):
            self.assertFalse(provider.preflight()[0])
        with patch.object(adk_provider.util, "find_spec", return_value=object()), patch.object(
            adk_provider.metadata, "version", return_value="2.8.0"
        ):
            self.assertTrue(provider.preflight()[0])


if __name__ == "__main__":
    unittest.main()
