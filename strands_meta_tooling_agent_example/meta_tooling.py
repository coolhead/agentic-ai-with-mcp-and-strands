#!/usr/bin/env python3
"""
Meta Tooling Example (Hardened for local Ollama)

Stable goals:
- Create tools dynamically into ./generated_tools
- Load tools at runtime (deterministic path handling)
- Provide a bootstrap command to install a known-good tool

Commands:
- list tools
- load <tool_file.py>
- bootstrap
- use <tool_name> [path]
- exit
"""

import os
import re
from pathlib import Path

from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import shell, editor, load_tool


GENERATED_DIR = Path(__file__).parent / "generated_tools"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


TOOL_BUILDER_SYSTEM_PROMPT = """You are an advanced agent that creates and uses custom Strands Agents tools.

Hard rules:
- When creating a tool, you MUST use the editor tool to write the tool file.
- You MUST write tool files ONLY to: generated_tools/<tool_name>.py (relative to the current working directory).
- After writing, you MUST use shell to run: ls -la generated_tools and confirm the file exists.
- Then you MUST use load_tool to load the file you just created.

Never invent paths like /home/user or /tools.
Never pretend you wrote a file unless it truly exists.

Tool naming:
- The tool name (function name) MUST match the file name without extension.
- TOOL_SPEC["name"] must match the function name.

When done creating a tool, you MUST print:
TOOL_CREATED: generated_tools/<tool_name>.py
"""


ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1:8b",
    temperature=0.3,
)

agent = Agent(
    model=ollama_model,
    system_prompt=TOOL_BUILDER_SYSTEM_PROMPT,
    tools=[load_tool, shell, editor],
)


# ---------- Helpers ----------
def extract_tool_created_path(text: str) -> str | None:
    m = re.search(r"TOOL_CREATED:\s*([^\s]+\.py)", text)
    return m.group(1) if m else None


def extract_first_python_code_block(text: str) -> str | None:
    m = re.search(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    return m.group(1) if m else None


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def resolve_generated_tool_path(tool_path: str) -> Path:
    p = Path(tool_path)
    if "generated_tools" in p.parts:
        filename = p.name
    else:
        filename = p.name if p.suffix == ".py" else f"{p.name}.py"
    return (GENERATED_DIR / filename).resolve()


def load_tool_via_agent(abs_path: Path) -> str:
    return str(agent(f'Use load_tool with path "{abs_path}" and load it now.'))


def list_tools() -> None:
    print("\nTools in generated_tools/:")
    os.system("ls -la generated_tools")


def manual_load(tool_filename: str) -> None:
    tool_abs = resolve_generated_tool_path(tool_filename)
    if not tool_abs.exists():
        print(f"❌ Tool file missing: {tool_abs}")
        list_tools()
        return
    print(f"✅ Loading tool from: {tool_abs}")
    print(load_tool_via_agent(tool_abs))


def handle_create_or_generic(user_input: str) -> None:
    response = agent(user_input)
    response_text = str(response)
    print(response_text)

    tool_rel = extract_tool_created_path(response_text)
    if not tool_rel:
        print("⚠️ No TOOL_CREATED marker found. Not attempting to load.")
        return

    tool_abs = resolve_generated_tool_path(tool_rel)

    if not tool_abs.exists():
        print(f"⚠️ TOOL_CREATED said {tool_rel}, but file not found at: {tool_abs}")
        print("   Attempting to extract a python code block from the model response and write it...")

        code = extract_first_python_code_block(response_text)
        if not code:
            print("❌ No python code block found in model response. Cannot write tool file.")
            list_tools()
            return

        write_file(tool_abs, code)
        print(f"✅ Wrote tool file: {tool_abs}")
        list_tools()

    print(f"✅ Loading tool from: {tool_abs}")
    print(load_tool_via_agent(tool_abs))


def use_tool_direct(tool_name: str, path: str | None) -> None:
    import importlib
    import sys

    # Ensure generated_tools is importable
    if str(GENERATED_DIR) not in sys.path:
        sys.path.insert(0, str(GENERATED_DIR))

    try:
        mod = importlib.import_module(tool_name)
    except Exception as e:
        print(f"❌ Failed to import tool '{tool_name}': {e}")
        return

    if not hasattr(mod, tool_name):
        print(f"❌ Tool function '{tool_name}' not found in module")
        return

    fn = getattr(mod, tool_name)

    tool_use = {
        "toolUseId": "direct_call",
        "input": {}
    }

    if path:
        tool_use["input"]["path"] = path

    try:
        result = fn(tool_use)
    except Exception as e:
        print(f"❌ Tool execution failed: {e}")
        return

    print("✅ Tool executed successfully")
    for c in result.get("content", []):
        if "text" in c:
            print(c["text"])


# ---------- Bootstrap a known-good tool ----------
KNOWN_GOOD_TOOL_NAME = "list_files_with_sizes.py"

KNOWN_GOOD_TOOL_CODE = r'''from typing import Any
from strands.types.tools import ToolUse, ToolResult
from pathlib import Path

TOOL_SPEC = {
    "name": "list_files_with_sizes",
    "description": "List files in a directory with human-readable sizes (B, KB, MB, GB).",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Directory to list. Defaults to current directory."},
                "include_dirs": {"type": "boolean", "description": "Include directories too (default false)."}
            },
            "required": []
        }
    }
}

def _human_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for u in units:
        if size < 1024.0 or u == units[-1]:
            if u == "B":
                return f"{int(size)} {u}"
            return f"{size:.2f} {u}"
        size /= 1024.0
    return f"{num_bytes} B"

def list_files_with_sizes(tool_use: ToolUse, **kwargs: Any) -> ToolResult:
    tool_use_id = tool_use["toolUseId"]
    inp = tool_use.get("input", {}) or {}
    path_str = inp.get("path", ".")
    include_dirs = bool(inp.get("include_dirs", False))

    try:
        base = Path(path_str).expanduser().resolve()
        if not base.exists():
            return {"toolUseId": tool_use_id, "status": "error", "content": [{"text": f"Path does not exist: {base}"}]}
        if not base.is_dir():
            return {"toolUseId": tool_use_id, "status": "error", "content": [{"text": f"Path is not a directory: {base}"}]}

        rows = []
        for p in sorted(base.iterdir(), key=lambda x: (x.is_file() == False, x.name.lower())):
            if p.is_dir() and not include_dirs:
                continue
            try:
                size_bytes = p.stat().st_size
                size_h = _human_size(size_bytes)
            except Exception:
                size_bytes = None
                size_h = "N/A"

            rows.append({"name": p.name + ("/" if p.is_dir() else ""), "size_bytes": size_bytes, "size": size_h})

        lines = [f"{r['name']}\t{r['size']}" for r in rows]
        text = "Files:\n" + "\n".join(lines) if lines else "No matching entries."

        return {"toolUseId": tool_use_id, "status": "success", "content": [{"text": text}]}

    except Exception as e:
        return {"toolUseId": tool_use_id, "status": "error", "content": [{"text": f"Error: {e}"}]}
'''


def bootstrap_known_good_tool() -> None:
    tool_abs = (GENERATED_DIR / KNOWN_GOOD_TOOL_NAME).resolve()
    if tool_abs.exists():
        print(f"✅ Known-good tool already exists: {tool_abs}")
        return
    write_file(tool_abs, KNOWN_GOOD_TOOL_CODE)
    print(f"✅ Bootstrapped known-good tool: {tool_abs}")
    list_tools()


def use_tool_best_effort(tool_name: str, path: str | None) -> None:
    # Best effort: ask agent to call the tool with JSON.
    # Works only if your Strands runtime exposes the loaded tool for invocation.
    payload = {"path": path} if path else {}
    msg = (
        f'Call the tool "{tool_name}" with this JSON input exactly: {payload}. '
        f"Return only the tool output."
    )
    print(str(agent(msg)))


# ---------- Main ----------
if __name__ == "__main__":
    print("\nMeta-Tooling Demonstration (Improved)")
    print("==================================")
    print("Commands:")
    print("  • create <description>   - Create a new tool")
    print("  • make a tool that <...> - Create a new tool (natural language)")
    print("  • list tools             - Show generated tool files")
    print("  • load <tool_file.py>    - Load a specific tool from generated_tools/")
    print("  • bootstrap              - Install a known-good list_files_with_sizes tool")
    print("  • use <tool_name> [path] - Best-effort invoke a loaded tool")
    print("  • exit                   - Exit the program")

    while True:
        try:
            user_input = input("\n> ").strip()

            if user_input.lower() == "exit":
                print("\nGoodbye!")
                break

            if user_input.lower() == "list tools":
                list_tools()
                continue

            if user_input.lower() == "bootstrap":
                bootstrap_known_good_tool()
                continue

            if user_input.lower().startswith("load "):
                manual_load(user_input.split(" ", 1)[1].strip())
                continue

            if user_input.lower().startswith("use "):
                parts = user_input.split(maxsplit=2)
                tool_name = parts[1] if len(parts) >= 2 else ""
                arg = parts[2] if len(parts) > 2 else "."

                arg = arg.strip()
                # Unwrap quotes if the user used them
                if (arg.startswith('"') and arg.endswith('"')) or (arg.startswith("'") and arg.endswith("'")):
                    arg = arg[1:-1]

                use_tool_direct(tool_name, arg)
                continue


            handle_create_or_generic(user_input)

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try a different request.")
