# luchat — context for the next chat

Open this project in Cursor: `/Volumes/core/Projects/luchat`  
Then start a **new agent chat** and `@summary.md`.

## Course repo (reference only — do not mix code into it)

**Path:** `/Volumes/core/Projects/llm_engineering`  
Udemy LLM Engineering (Ed Donner). Finished **weeks 1–3** in Jupyter notebooks. Notebooks did not feel like real practice, so this separate app exists.

Useful course files:

- `week1/day1.ipynb` — scrape site, messages, `openai.chat.completions.create`
- `week1/day2.ipynb` — OpenAI-compatible endpoints, Ollama, homework: website summarizer with local model
- `week1/scraper.py` — `fetch_website_contents`
- `week1/day4.ipynb`, `week1/day5.ipynb` — brochure / business flow
- **No `week1/day3.ipynb`** — that file never existed. Day 3 is `week2/day3.ipynb`
- Week 2 Gradio chat UIs in `week2/`

Course `.env` (gitignored): `OPENAI_API_KEY` in that repo root. Copy the same key into luchat later; do not commit it.

## Machine constraints

- MacBook Air **8GB RAM**, internal disk almost full
- **1TB external SSD** at `/Volumes/core` — course, luchat, and Ollama **models** live here
- SSD sometimes ejects mid-save → `.ipynb` JSON can truncate (`Unexpected end of JSON input`). Fix from git: `git restore <file>` if you still have a clean commit
- Plug SSD in **before** Cursor and Ollama

## Ollama (already set up)

- **App:** `/Applications/Ollama.app` (keep it there — macOS nags if the app is on the SSD)
- **Models:** `/Volumes/core/ollama` via `~/.ollama` → `/Volumes/core/ollama`
- **CLI:** `/usr/local/bin/ollama` → Applications app
- Local model to use: **`llama3.2:1b`** only (1.3GB). Do **not** pull `llama3.2` (full) or `deepseek-r1:1.5b` on this machine
- If `address already in use` on `11434`, the server is **already running** — do not run `ollama serve` again
- If notebook/API gets `ConnectError` / `APIConnectionError`: open the Ollama **app**, then `curl http://localhost:11434` should print `Ollama is running`
- OpenAI-compatible URL: `http://localhost:11434/v1`  
  `OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")`  
  `model="llama3.2:1b"`

`openai.chat.completions.create` is the **OpenAI SDK**, not built into Python. FastAPI does not call the LLM by itself — you call the SDK **inside** a FastAPI route.

## Final goal

A real chat app (not a notebook):

- **React (Vite)** = UI
- **FastAPI** = backend that calls LLMs
- Browser never holds API keys
- Switch between **Ollama (local)** and **frontier APIs** (OpenAI, later Gemini etc.)
- Practice what weeks 1–3 taught: messages, system/user prompts, chat completions, local vs paid models

Later (not required for first working chat): streaming, website summarizer port from day1/day2, scrape via `scraper.py` ideas.

## Current luchat layout

```
/Volumes/core/Projects/luchat
  pyproject.toml      # uv Python project
  uv.lock
  src/luchat/         # only __init__.py so far
  web/                # Vite React app (ESLint), npm
  summary.md          # this file
```

Package manager: **npm** for `web/` (pnpm is installed globally `12.6.0` but unused here — do not mix).  
Linter: **ESLint**.

## Deps already installed

**Python (uv):** `fastapi`, `uvicorn`, `python-dotenv`, `openai` (+ FastAPI stack: pydantic, starlette, httpx, etc.)

**React:** `web/` created with `npm create vite@latest web -- --template react`, `npm install` done, Vite was running.

No extra LLM package on the frontend.

## Next implementation (start here)

1. Add FastAPI `main.py` (root or `src/luchat/main.py`)
   - CORS allow `http://localhost:5173`
   - `POST /chat` body like `{ "messages": [ {"role","content"} ] }`
   - Call `openai.chat.completions.create`
   - Start with Ollama `llama3.2:1b`
2. `.env` next to the API (`OPENAI_API_KEY=...`) — gitignore it
3. Two terminals:
   - API: `cd /Volumes/core/Projects/luchat && uv run uvicorn ... --reload --port 8000`  
     (exact module path: `main:app` if `main.py` is at repo root, or `luchat.main:app` if under `src/luchat`)
   - UI: `cd web && npm run dev` (port 5173)
4. React: chat input + list; `fetch("http://localhost:8000/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages }) })`

## uv note

On this SSD, uv may warn about hardlinks. Harmless. Optional: `export UV_LINK_MODE=copy`

## Jupyter lessons (if you go back to the course)

- Notebook variables exist only after cells run **in this kernel session**
- `from openai import OpenAI` is not the same as `openai = OpenAI()`
- After kernel restart or SSD remount: run from the top again
- Kernel: `.venv (Python 3.12.x)` in the course repo

## Git note (course repo)

Cannot `git push` to `ed-donner/llm_engineering` (403). PRs need a **fork** under GitHub user AsimAdam.
