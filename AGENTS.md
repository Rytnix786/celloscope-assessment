# Agent Rules — Celloscope AI/ML Take-Home

## Read first, every session
1. Read this file in full before planning any task.
2. Read the relevant SKILL.md file(s) under `H:\Projects\celloscope-assessment\SKILLS_Main_Added` for the current task before writing any code. Do not skip this even if the task seems simple.
3. Produce a plan Artifact (file list + order + verification approach) before editing anything. Wait for explicit approval before executing.
4. Work exactly one phase at a time, scoped to what the current prompt asks. Do not start the next phase unannounced, and do not add anything not explicitly requested — no extra endpoints, no extra abstractions, no infra (queues, caches, orchestration) that wasn't asked for.

## Non-negotiable constraints
- Layer separation is graded mechanically:
  - `adapters/` is the ONLY layer allowed to import a provider SDK, model library, or OCR/STT library.
  - `services/` must NEVER import a FastAPI type (Request, Response, UploadFile, HTTPException, APIRouter).
  - `api/` only does HTTP routing, request/response models (Pydantic), and validation.
- Every commit is small and does ONE thing. Commit messages explain WHY, not just what changed.
- NEVER run `git push` or any command that publishes to a remote without asking me first and getting an explicit "yes, push."
- NEVER commit `.env`, API keys, or any credential. Check every diff before proposing a commit message.
- If a value can't be confidently parsed, preserve it in `raw_line` and leave the parsed field null/flagged. Never guess.
- After finishing a phase: stop and write a plain-English explanation (5–10 sentences) of what you built and why, as if you were prepping me to defend it live. I will be asked to walk through this code with no notice — an explanation I can't reproduce myself is a failure state, not a nice-to-have.

## Stack decisions locked
- Python 3.11+, FastAPI, type hints throughout.
- `docker compose up` on a clean clone must boot on mock adapters only — zero credentials, zero model download, zero network call.
- Real adapters activate only via `.env`.
