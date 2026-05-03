import asyncio
from pathlib import Path
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from app.core.logger import logger
import sys
import os

class ParserService:
    async def parse_document(self, file_path: Path) -> str:
        """
        Converts a document to Markdown text by communicating with the MCP Server.
        """
        logger.log("ParserService.parse_document", "START", {"file": str(file_path)})
        
        # Determine the python executable to use (current python environment)
        # Or using uv run if preferred, but sys.executable is reliable within the venv
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "app.mcp.parser_server"],
            env={**os.environ} # pass current environment
        )
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Call the tool exposed by the MCP server
                    result = await session.call_tool(
                        "convert_document_to_markdown", 
                        {"file_path": str(file_path)}
                    )
                    
                    markdown_text = result.content[0].text
                    
                    if markdown_text.startswith("Error:"):
                        logger.log("ParserService.parse_document", "MCP_TOOL_ERROR", {"error": markdown_text})
                        raise ValueError(markdown_text)
                        
                    logger.log("ParserService.parse_document", "SUCCESS", {"char_count": len(markdown_text)})
                    return markdown_text
        except Exception as e:
            logger.log("ParserService.parse_document", "FAILED", {"error": str(e)})
            raise ValueError(f"Failed to parse document via MCP: {str(e)}")

parser_service = ParserService()
