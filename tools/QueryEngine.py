






import fitz  # PyMuPDF
import json
from langchain.tools import tool
import textwrap
from pathlib import Path

from typing import Dict, Any
from typing_extensions import TypeAlias  # For Python < 3.10

#Document: TypeAlias = fitz.Document
Document: TypeAlias = Any

class PDFExtractionTools:

    @tool("Extract unstructured data from PDF and index them for use.")
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from the provided PDF file.

        Args:
            pdf_path (str): Path to the PDF file from which text needs to be extracted.

        Returns:
            str: JSON string containing the status and extracted text from each page of the PDF.
        """
        try:
            # Explicitly annotate the document variable
            #doc: Document = fitz.open(pdf_path)
            doc: Any = fitz.open(pdf_path)

            
            # Now doc is properly typed
            text: Dict[int, str] = {
                page_num: page.get_text() 
                for page_num, page in enumerate(doc)
            }
            
            # Make sure to close the document
            doc.close()
            
            result: Dict[str, Any] = {
                "status": "success", 
                "data": text, 
                "summary": self._generate_summary(text)
            }
            
        except Exception as e:
            result = {
                "status": "error", 
                "message": f"An error occurred while extracting text: {str(e)}"
            }
        
        return json.dumps(result, indent=2)

    @tool("Index text extracted from PDF.")
    def index_text(self, texts: Dict[int, str]) -> str:
        """
        Index the extracted text.

        Args:
            texts (dict): Dictionary of extracted text from each page of the PDF.

        Returns:
            str: JSON string containing the status and indexed text with page numbers as keys.
        """
        try:
            # Here we return the same text, as it is already indexed by page numbers
            result = {"status": "success", "data": texts}
        except Exception as e:
            result = {"status": "error", "message": f"An error occurred while indexing text: {str(e)}"}
        
        return json.dumps(result, indent=2)

    @tool("Extract text from PDF and index it.")
    def extract_and_index(self, pdf_path: str) -> str:
        """
        Extract text from the PDF file and index it.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            str: JSON string containing the status and indexed text with page numbers as keys.
        """
        extraction_result = self.extract_text_from_pdf(pdf_path)
        extraction_result_dict = json.loads(extraction_result)

        if extraction_result_dict["status"] == "success":
            indexing_result = self.index_text(extraction_result_dict["data"])
            return indexing_result
        else:
            return extraction_result

    def _generate_summary(self, text: Dict[int, str]) -> Dict[str, Any]:
        """
        Generate a summary of the extracted text.

        Args:
            text (dict): Dictionary of extracted text from each page of the PDF.

        Returns:
            dict: Summary of the text including the number of pages and an overview of content.
        """
        num_pages = len(text)
        preview_texts = {
            page_num: content[:200] + '...' 
            for page_num, content in text.items()
        }
        return {
            "total_pages": num_pages,
            "page_previews": preview_texts
        }
