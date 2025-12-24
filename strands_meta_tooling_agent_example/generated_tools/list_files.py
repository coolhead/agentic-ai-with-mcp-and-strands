from typing import Any
from strands.types.tools import ToolUse, ToolResult
import os

TOOL_SPEC = {
    "name": "list_files",
    "description": "Lists all files in a directory with their sizes in bytes.",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory to list (defaults to current directory)."
                }
            },
            "required": []
        }
    }
}

def list_files(tool_use: ToolUse, **kwargs: Any) -> ToolResult:
    tool_use_id = tool_use["toolUseId"]
    path = tool_use["input"].get("path", ".")
    try:
        entries = os.listdir(path)
        files = []
        for name in entries:
            full = os.path.join(path, name)
            try:
                size = os.path.getsize(full)
            except OSError:
                size = None
            files.append({"name": name, "size": size})
        return {
            "toolUseId": tool_use_id,
            "status": "success",
            "content": [{"text": str(files)}],
        }
    except Exception as e:
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": f"Error listing {path}: {e}"}],
        }
