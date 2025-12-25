## Workshop Modules – Execution Proof & Notes

This section documents **per-module execution evidence** for the AI for Bharat – Strands Agents Workshop.
Each module includes a proof artifact captured during live execution.

---

### Module 1 – Environment Setup & Validation
**Objective**
- Verify local Python environment
- Validate Strands + MCP dependencies
- Ensure CLI and runtime readiness

**Proof**
- `proof/module1_environment_setup.log`

**Status**
- ✅ Environment initialized successfully
- ✅ Dependencies installed and verified

---

### Module 2 – MCP Calculator (Server ↔ Client Integration)
**Objective**
- Implement an MCP server exposing calculator tools
- Validate MCP client discovery and direct tool invocation
- Confirm tool execution independent of LLM inference

**Proof**
- `proof/module2_mcp_calculator.log`

**What Was Validated**
- MCP server started successfully
- Tool discovery completed (`list_tools_sync`)
- Direct tool execution via MCP client:
  - `add(16,16) → 32`
  - `multiply(16,16) → 256`

**Important Note**
> MCP tool discovery in Strands may return `MCPAgentTool` objects rather than plain dictionaries.
> Tool execution correctness was validated via successful `call_tool_sync` responses with deterministic outputs.
>
> This confirms **MCP integration and tool wiring are correct**, independent of any LLM or Bedrock model behavior.

**Status**
- ✅ MCP server operational
- ✅ Tool discovery successful
- ✅ Direct tool calls validated

---

### Module 3 – Teacher’s Assistant (Multi-Agent Routing)
**Objective**
- Implement an orchestrator agent
- Route user queries to domain-specific agents (Math, Language, CS)
- Validate multi-agent coordination

**Proof**
- `proof/module3_teachers_assistant_agent.log`

**What Was Validated**
- Query routing logic
- Domain-specific agent invocation
- Correct responses from specialized agents

**Status**
- ✅ Multi-agent orchestration working
- ✅ Routing and delegation validated

---

### Module 4 – Reasoning & Domain Experiments
**Objective**
- Test structured reasoning across multiple domains
- Validate agent responses for non-trivial prompts

**Proof**
- `proof/module4_interest-rate.log`
- `proof/module4_lemon.log`
- `proof/module4_quantum.log`

**Status**
- ✅ Reasoning agents executed successfully

---

### Module 5 – Memory Agent
**Objective**
- Persist and retrieve contextual information
- Validate memory-backed agent behavior

**Proof**
- `proof/module5_memory.log`

**Status**
- ✅ Memory storage and recall validated

---

### Module 6 – Meta-Tooling (Dynamic Tool Creation)
**Objective**
- Dynamically create, load, and execute tools at runtime
- Validate Strands meta-tooling capabilities

**Proof**
- `proof/module6_meta_tooling.log`

**Status**
- ✅ Runtime tool generation and execution successful

---

### Module 7 – Streamlit UI & Model Experiments
**Objective**
- Integrate agents with Streamlit UI
- Test multiple models for tool compatibility

**Proof**
- `proof/module7_streamlit_*.jpg`

**Status**
- ✅ UI execution captured
- ✅ Model compatibility behavior documented


## Module 8 — Amazon Bedrock AgentCore (POC → Production)

AgentCore is a managed suite for deploying and operating agentic apps securely at scale. Instead of building custom infrastructure for session isolation, identity, memory, and observability, AgentCore provides composable services (Runtime, Identity, Gateway, Memory, Observability, Code Interpreter, Browser).

### 8.2 AgentCore Runtime — Hosting a Strands Agent
**Goal:** Package an agent as an AgentCore-compatible service and deploy to managed runtime (ARM64 container, /invocations + /ping).

**Proof (Local Execution)**
- MCP server running via Streamable HTTP
- Tool discovery validated using MCP local client
- Tool schemas and metadata returned correctly

**Proof (Remote Execution – Planned)**
- AgentCore Runtime deployment steps documented
- OAuth + Cognito configuration steps validated conceptually
- Remote execution blocked due to expired workshop credentials (STS/SSO)


### 8.2 AgentCore Runtime — Hosting an MCP Server (OAuth via Cognito)
**Goal:** Deploy an MCP tool server (add_numbers, multiply_numbers, greet_user) to AgentCore Runtime, protected by OAuth authorizer.
**Proof:** Cognito setup output (masked), AgentCore configure/launch output (ARN), remote MCP client tool listing with bearer token.

**Note on Remote Deployment (Workshop Constraint)**

Local MCP server and client validation was completed successfully, confirming
tool exposure, discovery, and protocol correctness.

Remote AgentCore deployment requires active AWS workshop credentials (STS/SSO).
During execution, the workshop-issued credentials expired and could not be
refreshed within the lab session window.

All remote deployment and invocation steps are documented and verified
against official Amazon Bedrock AgentCore documentation.


This mirrors real-world cloud environments where credential expiry,
SSO misconfiguration, or role revocation can block deployments despite
correct application logic.



## Event: AWS workshop - "ai for bharat" - Week 5: "Building agentic workflows in Python"
## Author: Raghavendra S

Email-Id: sraghavendra1512@gmail.com
