from typing import Any
from strands.types.tools import ToolUse, ToolResult
from pathlib import Path

TOOL_SPEC = {
    "name": "list_files_with_sizes",
    "description": "List files in a directory with human-readable sizes (B, KB, MB, GB).",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory to list. Defaults to current directory."
                },
                "include_dirs": {
                    "type": "boolean",
                    "description": "Include directories too (size may be OS-dependent). Defaults to false."
                }
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
            return {
                "toolUseId": tool_use_id,
                "status": "error",
                "content": [{"text": f"Path does not exist: {base}"}],
            }
        if not base.is_dir():
            return {
                "toolUseId": tool_use_id,
                "status": "error",
                "content": [{"text": f"Path is not a directory: {base}"}],
            }

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

            rows.append({
                "name": p.name + ("/" if p.is_dir() else ""),
                "size_bytes": size_bytes,
                "size": size_h,
            })

        # Compact readable output (also includes structured info)
        lines = [f"{r['name']}\t{r['size']}" for r in rows]
        text = "Files:\n" + "\n".join(lines) if lines else "No matching entries."

        return {
            "toolUseId": tool_use_id,
            "status": "success",
            "content": [{"text": text}],
        }

    except Exception as e:
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": f"Error: {e}"}],
        }
