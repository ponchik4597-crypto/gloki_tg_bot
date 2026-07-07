---
name: llm_service_fix
description: Fix OpenRouter endpoint, model ID, and request headers for LLMService
source: auto-skill
extracted_at: '2026-06-01T15:45:00.000Z'
---

## Problem
The bot received HTML responses or 404 errors from the OpenRouter API because:
- The endpoint was set to the base URL `https://openrouter.ai` instead of the chat completions endpoint.
- The model identifier used (`google/gemini-2.5-flash:free`) is not available on OpenRouter, resulting in a *No endpoints found* error.
- The request lacked an explicit `Accept: application/json` header, causing the server to return an HTML page.

## Fixes applied
1. **Correct endpoint** – Updated `LLMService` initialization to use the full Chat Completions URL:
   ```python
   endpoint="https://openrouter.ai/api/v1/chat/completions"
   ```
2. **Dynamic endpoint usage** – In `LLMService.call_llm` the target endpoint is now:
   ```python
   target_endpoint = endpoint or self.endpoint
   ```
   This allows an optional override while defaulting to the configured endpoint.
3. **Model identifier** – Switched to a supported OpenRouter model:
   ```python
   "model": "openrouter/meta-llama/llama-3-8b-instruct:free"
   ```
   The identifier is provided via `self.settings["model_params"]`.
4. **Accept header** – Added `"Accept": "application/json"` to the request headers to force JSON responses.
5. **Payload composition** – Payload now merges any `model_params` from settings, removing the hard‑coded model field.

## Result
After these changes the LLMService correctly receives JSON responses from OpenRouter, no longer logs *Server sent non‑JSON* or 404 errors, and the fallback handler can return proper AI answers.
