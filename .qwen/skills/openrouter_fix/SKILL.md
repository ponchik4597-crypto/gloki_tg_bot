---
name: openrouter_fix
description: Fix OpenRouter request configuration (endpoint, headers, model ID) for ai_service
source: auto-skill
extracted_at: '2026-05-31T15:20:00.000Z'
---

## Goal
Ensure that the AI service correctly communicates with OpenRouter, using the proper endpoint, JSON Accept header, and valid model identifier.

## Steps
1. **Check token handling** – read `AI_TOKEN` from environment, fallback to `OPENAI_API_KEY` if missing.
2. **Set correct URL** – use `https://openrouter.ai/api/v1/chat/completions`.
3. **Add required headers** – `Content-Type: application/json` and `Accept: application/json`.
4. **Use valid model ID** – `meta-llama/llama-3-8b-instruct:free` (no `openrouter/` prefix).
5. **Update payload** – include system prompt and user message.
6. **Log errors** – provide clear log messages for missing token or non‑200 responses.

## Verification
- Run the bot and trigger the fallback handler.
- Observe logs: `OpenRouter статус` should be `200`.
- The bot should return a Russian answer without JSON parsing errors.

## Notes
- After changing any environment variable, restart the bot (see `user_restart_project` memory).
- This skill consolidates the changes made in `src/services/ai_service.py`.
