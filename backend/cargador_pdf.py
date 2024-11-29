import json
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
from langchain_core.documents import Document
from PyPDF2 import PdfReader



class CargadorPDF:
    """
    Clase para procesar documentos PDF, asignarles etiquetas y almacenarlos en una base de datos ChromaDB.
    """

    def __init__(self, api_key, collection_name="pdf_documents", model="embed-english-v3.0"):
        """
        Inicializa los embeddings, la base de datos Chroma y configura el catalogador.

        Args:
            api_key (str): Clave API de Cohere.
            collection_name (str, optional): Nombre de la colección en ChromaDB. Por defecto, "pdf_documents".
            model (str, optional): Modelo de embeddings de Cohere. Por defecto, "embed-english-v3.0".
        """
        self.embeddings = CohereEmbeddings(cohere_api_key=api_key, model=model)
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings
        )

    def extraer_texto_pdf(self, pdf_path):
        """
        Extrae el texto de un archivo PDF.

        Args:
            pdf_path (str): Ruta del archivo PDF.

        Returns:
            str: Texto extraído del PDF.
        """
        reader = PdfReader(pdf_path)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text()
        return texto

    
    def cargar_documentos_pdf(self, pdf_folder_path):
        """
        Procesa todos los archivos PDF en una carpeta, asigna etiquetas y los guarda en ChromaDB.

        Args:
            pdf_folder_path (str): Ruta de la carpeta que contiene los archivos PDF.
            etiquetas (list): Lista de etiquetas disponibles para asignar.

        Returns:
            None
        """
        pdf_files = [f for f in os.listdir(pdf_folder_path) if f.endswith('.pdf')]
        documents = []

        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_folder_path, pdf_file)
            texto = self.extraer_texto_pdf(pdf_path)

          
            # Crear un documento en ChromaDB
            document = Document(
                page_content=texto,
                metadata={'nombre': pdf_file}
            )
            documents.append(document)

        # Agregar los documentos a ChromaDB
        self.vector_store.add_documents(documents)
        print(f"{len(documents)} documentos PDF cargados en ChromaDB.")

        for document in documents:
            doc = document.metadata['nombre']
            print(f"Documento: {doc}")
