from pathlib import Path
from docling.document_converter import DocumentConverter
from app.core.logger import logger

class ParserService:
    def __init__(self):
        self.converter = DocumentConverter()

    def parse_pdf(self, file_path: Path) -> str:
        """
        Converts a PDF file to Markdown text using Docling.
        """
        logger.log("ParserService.parse_pdf", "START", {"file": str(file_path)})
        try:
            result = self.converter.convert(file_path)
            markdown_text = result.document.export_to_markdown()
            logger.log("ParserService.parse_pdf", "SUCCESS", {"char_count": len(markdown_text)})
            return markdown_text
        except Exception as e:
            logger.log("ParserService.parse_pdf", "FAILED", {"error": str(e)})
            raise ValueError(f"Failed to parse PDF: {str(e)}")

parser_service = ParserService()
