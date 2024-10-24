from crewai_tools import PDFSearchTool
from crewai_tools import CodeDocsSearchTool

# Inicializando la herramienta para leer PDF's
pdf_tool = PDFSearchTool(pdf='bucket/cp.pdf')

fastapi_tool = CodeDocsSearchTool(docs_url="https://fastapi.tiangolo.com/reference")

scipy_tool = CodeDocsSearchTool(docs_url="https://docs.scipy.org/doc/scipy/reference/index.html#scipy-api")