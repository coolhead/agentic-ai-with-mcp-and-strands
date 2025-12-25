# generated_tools/count_chars.py

from strands.types.tools import ToolResult, ToolUse

TOOL_SPEC = {
    "name": "count_chars",
    "description": "Counts characters in a string",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Input text to count characters"
                }
            },
            "required": ["text"]
        }
    }
}

def count_chars(tool: ToolUse, **kwargs: Any) -> ToolResult:
    # Get the input text from the tool's data
    text = tool["data"]["text"]

    # Count the characters in the text
    char_count = len(text)

    return {
        "toolUseId": tool["toolUseId"],
        "status": "success",
        "content": [{"text": f"Character count: {char_count}"}]
    }