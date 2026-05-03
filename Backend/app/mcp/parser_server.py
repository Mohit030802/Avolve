from mcp.server.fastmcp import FastMCP
from docling.document_converter import DocumentConverter
from pathlib import Path
import logging

# Configure basic logging for the MCP server
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("parser_server")

# Initialize FastMCP Server
mcp = FastMCP("Resume Parser Server")

# Initialize Docling converter
# Note: Initializing here means it happens once when the server starts
converter = DocumentConverter()

@mcp.tool()
def convert_document_to_markdown(file_path: str) -> str:
    """
    Converts a document (PDF, DOCX, TXT, HTML, etc.) to Markdown text using Docling.
    """
    logger.info(f"Received request to convert document: {file_path}")
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        return f"Error: File not found at {file_path}"
    
    try:
        # Handle raw text files separately as Docling does not natively support .txt extension
        if path.suffix.lower() == '.txt':
            with open(path, 'r', encoding='utf-8') as f:
                markdown = f.read()
            logger.info(f"Successfully read text file: {file_path} ({len(markdown)} chars)")
            return markdown
            
        result = converter.convert(path)
        markdown = result.document.export_to_markdown()
        logger.info(f"Successfully converted document: {file_path} ({len(markdown)} chars)")
        return markdown
    except Exception as e:
        logger.error(f"Failed to convert document: {str(e)}")
        return f"Error converting document: {str(e)}"

if __name__ == "__main__":
    # Run the server with stdio transport
    mcp.run(transport='stdio')
