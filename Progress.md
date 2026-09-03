# Progress.md — Session Log

Append-only. Never edit or delete past entries — add a new dated entry each session. See `CLAUDE.md` for the end-of-session update protocol.

---

## Learner Notes (running, updated as we learn)

- Hardware: RTX 3070, 8 GB VRAM.
- Goal: deeply understand RAG and local LLM hosting, not just get a working app — teaching approach is Socratic (see `CLAUDE.md`), no direct solutions.
- Strengths observed: strong first-principles reasoning (derived the concept of quantization himself before it was named; figured out 4-bit byte-packing unprompted); insists on empirically verifying claims rather than trusting theory alone (VRAM math vs. real nvidia-smi/Task Manager numbers, tested real API calls); iterates well through real debugging (fixed a chain of 3 real bugs — https/http, missing endpoint path, model name typo — one at a time from hints, no hand-holding needed on the actual fixes).
- Recurring confusions: SI unit prefixes (skipped "kilo" going from bytes to GB — corrected); tends to reach for an approximately-right but imprecise term on the first pass (called Ollama's server a "proxy"; called the `context` API field the "system prompt") — self-corrects quickly once asked to re-examine, doesn't need the answer handed over.
- Preferences: enjoys hands-on verification (checking real GPU/VRAM numbers, reading real stack traces) over pure theory; comfortable in a terminal and reading tracebacks directly.

---

## Session 0 — 2026-09-02 — Project setup

**Status:** Setup only, no teaching content covered yet.

- Created `CLAUDE.md` (tutor persona and rules), `Tasks.md` (full roadmap), and `Progress.md` (this file).
- Current task: **0.1** — confirm dev environment (Python, virtual env/conda, git, CUDA toolkit + driver, `nvidia-smi`).

**Next step:** Start Phase 0 — verify the environment and GPU visibility, then define RAG and local hosting in Lothair's own words before touching any code.

---

## Session 1 — 2026-09-03 — Phase 1 complete: Ollama + Llama 3.1 8B running and verified

**Status:** All of Phase 1 done except task 1.6. Model is installed, running, and successfully queried through the real API from Lothair's own code.

**Also handled (outside the curriculum, mechanical):** Reviewed new `app/` scaffolding Lothair had added (`config.py` Singleton, `logger.py`, `main.py`, `model.py` stub). Initialized `codegraph` (static dependency-graph visualizer) against `app/src`, output at `.codegraph/codegraph.html` (gitignored, rerun anytime with `codegraph app/src --output .codegraph/codegraph.html`).

**Covered / understood:**
- **1.1 — Runtime choice:** Chose **Ollama**. Justified through dialogue: automatic VRAM/layer-offload management, a registry of pre-quantized pullable models, and a persistent local HTTP server architecture. Corrected an initial "proxy" framing — Ollama's daemon *is* the inference backend, not a forwarder to one.
- **1.2 — Quantization:** Derived the concept from first principles (an 8B model at fp16 = 16GB, doesn't fit 8GB VRAM -> need fewer bits/parameter). Worked out that multiple sub-byte values can be packed into a byte (hence 4-bit is possible), and reasoned out the quality-vs-size tradeoff that makes 4-bit the practical sweet spot. Fixed a genuine gap in SI unit prefixes (bytes->KB->MB->GB->TB, had skipped "kilo") along the way.
- **1.3 — Model choice:** **Llama 3.1 8B** (Meta, official), Q4_K_M, 4.9GB, ~3.1GB headroom. Got there by evaluating and rejecting two other candidates first: `qwen3.5:9b` (real quantized size, 6.6GB, left only 1.4GB headroom — too tight, and taught the lesson that real K-quant sizes run bigger than naive bytes/param math) and `ornith:9b` (a Qwen3.5-based fine-tune specialized for agentic coding — wrong specialization for a general-purpose RAG chatbot). Chose Llama 3.1 8B for solid headroom plus being extremely well-documented for a first project.
- **1.4 — Install & run:** Installed Ollama, pulled and ran `llama3.1:8b`. Empirically verified VRAM usage two ways (`nvidia-smi`, Windows Task Manager "Dedicated GPU Memory"): Ollama itself uses ~5.7GB (close to the 4.9GB weight prediction, +~0.8GB attributed to KV cache/compute buffer reservation — correctly reasoned out that this buffer is allocated once at load time, not grown per-token). Important real-world lesson surfaced: background apps (Discord, Opera GX, Windows itself) had a ~1.4GB baseline VRAM footprint, so real free headroom while running (~0.9GB) was tighter than the theoretical 3.1GB, which had assumed nothing else was using the GPU.
- **1.5 — Querying via the real API:** Found and used the `/api/chat` endpoint (`{model, messages: [{role, content}]}`), correctly distinguishing it from `/api/generate`. Corrected a mix-up between the `system` field (system prompt) and `context` field (opaque conversation-state token blob returned by a previous response, fed into the next request). Explained temperature well, including a good self-correction (distribution only becomes truly *uniform* in the limit as T->infinity, not at typical values like 1.3-1.5). Wrote his own working request body in `model.py` and debugged it for real through three sequential errors: SSL `WRONG_VERSION_NUMBER` (was using `https://` against a plain HTTP server), `405 Method Not Allowed` (missing `/api/chat` path), and a model-name typo (`ollama3.1:8b` -> `llama3.1:8b`). Understood and explained why the API streams tokens by default and how `"stream": false` turns that off.

**Next step:** Task **1.6** — context window limits and what happens when they're exceeded — closes out Phase 1. Then on to Phase 2 (RAG building blocks: embeddings, chunking, vector store).

