from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.schemas.resume_schema import ResumeSchema
from app.core.config import settings
from app.core.logger import logger

class LLMService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=settings.google_api_key,
            temperature=0,
            max_retries=3
        )
        self.parser = PydanticOutputParser(pydantic_object=ResumeSchema)

    def extract_structured_data(self, markdown_text: str) -> ResumeSchema:
        """
        Uses Gemini 1.5 Flash to extract structured JSON from Markdown resume text.
        """
        logger.log("LLMService.extract_structured_data", "START", {"char_count": len(markdown_text)})
        
        prompt = ChatPromptTemplate.from_template(
            "Extract the following information from the resume text provided in Markdown format.\n"
            "{format_instructions}\n"
            "Resume Text:\n{resume_text}"
        )
        
        chain = prompt | self.llm | self.parser
        
        try:
            result = chain.invoke({
                "resume_text": markdown_text,
                "format_instructions": self.parser.get_format_instructions()
            })
            logger.log("LLMService.extract_structured_data", "SUCCESS", {"name": result.name})
            return result
        except Exception as e:
            logger.log("LLMService.extract_structured_data", "FAILED", {"error": str(e)})
            raise ValueError(f"Failed to extract structured data: {str(e)}")

llm_service = LLMService()
