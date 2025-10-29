from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.documents import Document
import validators
import bs4


class FileReader:
    """Utility class for reading and loading content from various file types."""

    def __init__(self):
        print("FileReader initialized")

    # ------------------------------------------------------------
    # Method: file_loader
    # Description:
    #   Determines the file type (PDF, DOCX, CSV, TXT, or Web URL)
    #   and loads the content using the appropriate loader.
    #   - Supports both local and remote (URL) files.
    # ------------------------------------------------------------
    def file_loader(self, file: str) -> list[Document]:
        if file:
            if validators.url(file):
                return self.read_web_page(file)
            elif file.endswith(".docx"):
                return self.read_doc(file)
            elif file.endswith(".pdf"):
                return self.read_pdf(file)
            elif file.endswith(".csv"):
                return self.read_csv(file)
            else:
                return self.read_text(file)
        return []

    # ------------------------------------------------------------
    # Method: read_doc
    # Description:
    #   Loads and parses a DOCX file into LangChain Document objects.
    # ------------------------------------------------------------
    def read_doc(self, file: str) -> list[Document]:
        doc = Docx2txtLoader(file)
        return doc.load()

    # ------------------------------------------------------------
    # Method: read_csv
    # Description:
    #   Loads and parses a CSV file into LangChain Document objects.
    # ------------------------------------------------------------
    def read_csv(self, file: str) -> list[Document]:
        csv = CSVLoader(file)
        return csv.load()

    # ------------------------------------------------------------
    # Method: read_pdf
    # Description:
    #   Loads and extracts text from a PDF file into LangChain Documents.
    # ------------------------------------------------------------
    def read_pdf(self, file: str) -> list[Document]:
        pdf = PyPDFLoader(file)
        return pdf.load()

    # ------------------------------------------------------------
    # Method: read_web_page
    # Description:
    #   Fetches and parses a web page (URL) into LangChain Document objects.
    # ------------------------------------------------------------
    def read_web_page(self, path: str) -> list[Document]:
        web_page = WebBaseLoader(web_path=[path])
        return web_page.load()

    # ------------------------------------------------------------
    # Method: read_text
    # Description:
    #   Loads and parses a plain text file into LangChain Document objects.
    # ------------------------------------------------------------
    def read_text(self, file: str) -> list[Document]:
        text = TextLoader(file_path=file)
        return text.load()
