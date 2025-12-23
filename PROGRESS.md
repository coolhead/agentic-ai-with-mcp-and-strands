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
