from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.documents import Document
import validators
import bs4


# ------------------------------------------------------------
# Module: document_reader
# Description:
#   Provides utilities to read and load content from multiple
#   file formats (PDF, DOCX, CSV, TXT) and web URLs into
#   standardized LangChain Document objects for further processing.
# ------------------------------------------------------------


class DocumentReader:
    # ------------------------------------------------------------
    # Initialize Class
    # ------------------------------------------------------------
    def __init__(self):
        print("DocumentReader initialized")

    # ------------------------------------------------------------
    # Method: file_loader
    # Description:
    #   Determines the file type (PDF, DOCX, CSV, TXT, or Web URL)
    #   and loads the content using the appropriate loader.
    #   - Automatically detects URLs using the validators package.
    #   - Returns a list of LangChain Document objects.
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
    #   Loads and parses a Microsoft Word (.docx) file into
    #   LangChain Document objects for downstream processing.
    # ------------------------------------------------------------
    def read_doc(self, file: str) -> list[Document]:
        doc = Docx2txtLoader(file)
        return doc.load()

    # ------------------------------------------------------------
    # Method: read_csv
    # Description:
    #   Loads and parses a CSV file into LangChain Document objects.
    #   Each row is typically treated as a separate Document.
    # ------------------------------------------------------------
    def read_csv(self, file: str) -> list[Document]:
        csv = CSVLoader(file)
        return csv.load()

    # ------------------------------------------------------------
    # Method: read_pdf
    # Description:
    #   Loads and extracts textual content from a PDF file into
    #   LangChain Document objects. Handles multi-page PDFs.
    # ------------------------------------------------------------
    def read_pdf(self, file: str) -> list[Document]:
        pdf = PyPDFLoader(file)
        return pdf.load()

    # ------------------------------------------------------------
    # Method: read_web_page
    # Description:
    #   Fetches and parses a web page (URL) into LangChain Document
    #   objects using BeautifulSoup for HTML parsing.
    # ------------------------------------------------------------
    def read_web_page(self, path: str) -> list[Document]:
        web_page = WebBaseLoader(web_path=[path])
        return web_page.load()

    # ------------------------------------------------------------
    # Method: read_text
    # Description:
    #   Loads and parses a plain text (.txt) file into LangChain
    #   Document objects for ingestion and vectorization.
    # ------------------------------------------------------------
    def read_text(self, file: str) -> list[Document]:
        text = TextLoader(file_path=file)
        return text.load()
