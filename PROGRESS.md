# Workshop Progress — Agentic AI with MCP & Strands

## Module 4 — Multi-Agent Research Workflow (Graph Pattern)
**Status:** Completed ✅  
**Date:** 2025-12-23  
**Location:** `strands_multi_agent_example/graph/researcher.py`

### What I validated
- Graph executes 4 nodes in order: `research → analysis + fact_check → report`
- Research node uses `http_request` tool for web lookup
- End-to-end run produces a final report with sources + execution stats

### Proof logs
- `proof/module4_quantum.log` (Quantum computers)
- `proof/module4_lemon.log` (Lemon cures cancer)
- `proof/module4_interest-rate.log` (Interest rates claim)

### Commands used
```bash
printf "What are quantum computers?\nexit\n" | timeout 90s python strands_multi_agent_example/graph/researcher.py | tee proof/module4_quantum.log
printf "Lemon cures cancer\nexit\n" | timeout 90s python strands_multi_agent_example/graph/researcher.py | tee proof/module4_lemon.log
printf "Interest rates have been decreasing recently\nexit\n" | timeout 90s python strands_multi_agent_example/graph/researcher.py | tee proof/module4_interest-rate.log
```
#### Notes

One earlier run hit Bedrock service capacity limits (serviceUnavailableException); retry succeeded.

---

## Module 5 — Memory Agent with Strands (FAISS Backend)
**Status:** Completed ✅  
**Date:** 2025-12-23  
**Location:** `strands_memory_agent_example/memory_agent.py`

### What I validated
- Persistent memory using `mem0_memory` tool with FAISS backend
- Memory operations:
  - `store` (user preferences)
  - `retrieve` (semantic similarity search)
  - `list` (all memories for a user)
- Tool chaining: memory retrieval → LLM response generation
- User-scoped memory isolation via `user_id`

### Proof logs
- `proof/module5_memory.log`

### Commands used
```bash
pip install faiss-cpu
```
printf "My name is J. I like seafood. I have a dog.\nWhat do I like?\nTell me everything you know about me\nexit\n" \
| timeout 120s python strands_memory_agent_example/memory_agent.py \
| tee proof/module5_memory.log

#### Notes

FAISS CPU backend used (no OpenSearch dependency)

Memory persistence verified within session

Retrieval relevance scores confirmed


---
