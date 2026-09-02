# Tasks.md — RAG Chatbot Learning Roadmap

Maintained by Professor Vasseur (see `CLAUDE.md`). Checkboxes are only ticked once Lothair has *understood* the task, not just gotten code to run. This plan can be adjusted as we go, but changes should be discussed with Lothair first.

Hardware constraint carried through the whole plan: **RTX 3070, 8 GB VRAM**.

---

## Phase 0 — Foundations

- [ ] 0.1 Confirm dev environment: Python version, virtual env / conda, git, CUDA toolkit + driver version, `nvidia-smi` working.
- [ ] 0.2 Verify GPU is visible to Python (e.g. via `torch.cuda.is_available()`) and understand what "VRAM" actually limits.
- [ ] 0.3 Define, in your own words: what is RAG, and what problem does it solve that a plain LLM doesn't?
- [ ] 0.4 Define, in your own words: what does it mean to "host" an LLM locally, and what are the moving parts (weights, runtime/inference engine, API layer)?

## Phase 1 — Hosting an open-source LLM locally

- [ ] 1.1 Compare inference runtimes (e.g. Ollama, llama.cpp, vLLM, text-generation-webui) — trade-offs relevant to a single 8 GB GPU.
- [ ] 1.2 Understand quantization (what it is, GGUF vs GPTQ/AWQ, why 4-bit is usually the sweet spot on 8 GB VRAM) and estimate VRAM budget for a candidate model + context length.
- [ ] 1.3 Choose and justify a first model (size, quantization level) that fits the 3070's VRAM budget with headroom for context.
- [ ] 1.4 Install the chosen runtime and get the model running locally.
- [ ] 1.5 Query the model via its API (not just a chat UI) and understand the request/response shape (prompt, system message, sampling params).
- [ ] 1.6 Understand context window limits and what happens when they're exceeded.

## Phase 2 — RAG building blocks

- [ ] 2.1 Understand embeddings: what a vector represents, similarity metrics (cosine, dot product), why they enable semantic search.
- [ ] 2.2 Choose a local embedding model and justify it (quality vs. size vs. speed, and whether it also competes for the 3070's VRAM).
- [ ] 2.3 Understand chunking: why documents must be split, trade-offs of chunk size/overlap, fixed-size vs. semantic/structural chunking.
- [ ] 2.4 Choose and justify a vector store (e.g. Chroma, FAISS, Qdrant local mode) for this project's scale.
- [ ] 2.5 Design the ingestion pipeline on paper: load → clean → chunk → embed → store (+ metadata to keep, e.g. source, position).

## Phase 3 — Retrieval pipeline

- [ ] 3.1 Implement document ingestion (load a small real document set, chunk it, embed it, store it).
- [ ] 3.2 Implement top-k retrieval for a query and manually sanity-check the results (do the returned chunks actually look relevant?).
- [ ] 3.3 Understand and discuss when/why to go beyond pure vector search (e.g. hybrid search with BM25, re-ranking) — decide if it's in scope now or later.
- [ ] 3.4 Design the prompt template that combines system instructions + retrieved context + user question, and reason about token budget vs. the model's context window from Phase 1.

## Phase 4 — Wiring the chatbot

- [ ] 4.1 Connect retrieval (Phase 3) to the local LLM (Phase 1) into a single request/response flow.
- [ ] 4.2 Handle multi-turn conversation (what "memory" means here, and what to do about it given limited context length).
- [ ] 4.3 Handle the "no relevant context found" case — decide and implement the desired behavior (refuse, say "I don't know", fall back to general knowledge, etc.) and justify the choice.
- [ ] 4.4 Wrap the flow behind a simple local API (e.g. FastAPI) with a clear request/response contract.

## Phase 5 — Interface

- [ ] 5.1 Choose a UI approach (e.g. Streamlit, Gradio, or a minimal custom frontend) and justify it for this project's needs.
- [ ] 5.2 Build a minimal chat UI that talks to the API from Phase 4.
- [ ] 5.3 Add basic UX niceties as needed (streaming responses, showing retrieved sources, error states).

## Phase 6 — Evaluation & iteration

- [ ] 6.1 Define what "good" looks like for this chatbot (relevance, faithfulness/no hallucination, latency) and how to check for each, even informally.
- [ ] 6.2 Run a set of test questions against the system and diagnose failures (bad retrieval vs. bad generation vs. bad prompt).
- [ ] 6.3 Tune based on findings (chunk size, k, embedding model, prompt, or model choice) and re-test.

## Phase 7 — Polish & wrap-up

- [ ] 7.1 Add basic logging/error handling for the pipeline.
- [ ] 7.2 Review VRAM usage under real load and confirm the system stays within the 3070's budget.
- [ ] 7.3 Write down, in Lothair's own words, the full architecture end to end — this is the real "final exam" for the project.
- [ ] 7.4 (Optional/stretch) Packaging or deployment considerations (Docker, persistence, etc.) if Lothair wants to take it further.

---

## Notes for the tutor

- Phases are a default order, not a straitjacket — e.g. Phase 1 and Phase 2 have no hard dependency and could interleave if that suits Lothair better.
- Re-open a checked task if a later phase reveals a real gap in understanding, rather than silently patching over it.
