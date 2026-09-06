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

- [x] 1.1 Compare inference runtimes (e.g. Ollama, llama.cpp, vLLM, text-generation-webui) — trade-offs relevant to a single 8 GB GPU. **Decision: Ollama** — automatic VRAM/layer offload management, pre-quantized model registry, persistent local HTTP server.
- [x] 1.2 Understand quantization (what it is, GGUF vs GPTQ/AWQ, why 4-bit is usually the sweet spot on 8 GB VRAM) and estimate VRAM budget for a candidate model + context length. **4-bit chosen: ~0.5 bytes/param, leaves headroom for KV cache.**
- [x] 1.3 Choose and justify a first model (size, quantization level) that fits the 3070's VRAM budget with headroom for context. **Decision: Llama 3.1 8B (Meta, official, general-purpose), Q4_K_M, 4.9GB — leaves ~3.1GB headroom for KV cache.** (Considered qwen3.5:9b [1.4GB headroom, too tight] and its ornith:9b coding fine-tune [wrong specialization for a general RAG chatbot] first — chose Llama 3.1 8B for solid headroom margin plus being extremely well-documented for a first project.)
- [x] 1.4 Install the chosen runtime and get the model running locally. **Verified empirically: Ollama itself uses ~5.7GB VRAM (4.9GB weights + ~0.8GB KV cache/compute buffers, matching prediction). Windows + background apps (Discord, Opera GX, etc.) baseline ~1.4GB — real free headroom while running ~0.9GB, tighter than the theoretical 3.1GB since that ignored background app usage.**
- [x] 1.5 Query the model via its API (not just a chat UI) and understand the request/response shape (prompt, system message, sampling params). **Used /api/chat with {model, messages:[{role,content}]}; debugged https->http, missing /api/chat path, and model name typo along the way; understood streaming (default) vs stream:false for a single response.**
- [x] 1.6 Understand context window limits and what happens when they're exceeded. **When the fixed-size KV cache buffer fills, the engine (llama.cpp/Ollama) silently evicts the oldest tokens ("context shifting") rather than erroring — no crash, just quiet forgetting (system prompt or early context can drop unnoticed). Mitigation for later (task 4.2): context compaction/summarization to shrink history while preserving key info.**

## Phase 2 — RAG building blocks

- [x] 2.1 Understand embeddings: what a vector represents, similarity metrics (cosine, dot product), why they enable semantic search. **Derived cosine similarity from the dot product + norms (dot / (norm_a * norm_b)), understood it deliberately ignores magnitude to compare direction/meaning only. End-to-end retrieval pipeline explained correctly: embed query -> cosine similarity vs. stored chunk vectors -> top-k -> hand only the matching chunks (not whole source docs) to the LLM as context, to avoid polluting/blowing the context window.**
- [x] 2.2 Choose a local embedding model and justify it (quality vs. size vs. speed, and whether it also competes for the 3070's VRAM). **Decision: snowflake-arctic-embed:33m, ~67MB.** Reasoned that embedding models (tens-hundreds of millions of params) are 20-300x smaller than the 8B chat LLM, so quantization/VRAM isn't the real constraint in isolation — but realized the embedding model and the chat LLM must be resident in VRAM *simultaneously* during a turn (load/unload cycling to avoid this was considered and rejected: reload latency on every message would make the chat unresponsive). Given the real ~0.9GB free headroom measured in session 1, picked the smallest variant; can revisit for a bigger/higher-quality variant later once retrieval quality is actually measurable (Phase 6). Also correctly ruled out parallelizing embedding calls — this is a personal single-user project, not a multi-request service, so throughput isn't the bottleneck, model size/latency is.**
- [x] 2.3 Understand chunking: why documents must be split, trade-offs of chunk size/overlap, fixed-size vs. semantic/structural chunking. **Understood: naive fixed-N-char splitting crops mid-word/sentence and loses cross-boundary continuity. Overlap (duplicating a bit of text between consecutive chunks) fixes continuity loss. Recursive/hierarchical splitting (cascading separator priority: paragraph -> line -> sentence -> word -> char) avoids bad cut points without enumerating every document structure by hand. Semantic chunking (embedding-based topic-shift detection) noted as the advanced alternative. Chunk size trade-off: too small loses context, too big dilutes the embedding across unrelated topics so it may not score high enough on similarity to be retrieved even if the answer is technically present.**
- [x] 2.4 Choose and justify a vector store (e.g. Chroma, FAISS, Qdrant local mode) for this project's scale. **Decision: build it himself with numpy (brute-force cosine similarity over an in-memory/on-disk list of {vector, chunk_text, source, ...metadata}), not a library.** Correctly reasoned that brute-force search is computationally fine at personal-project scale (hundreds/thousands of chunks) — fancy ANN indexing (Chroma/FAISS/Qdrant) only pays off at much larger scale. Explicitly considered and initially leaned toward a library (weighed the real cost of DIY: metadata storage, persistence), then deliberately chose DIY anyway for the stated reason of understanding and controlling the whole layer rather than treating retrieval as a black box — a legitimate, well-reasoned choice given the project's learning goals.**
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
