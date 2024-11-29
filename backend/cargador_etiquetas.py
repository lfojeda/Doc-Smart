from dotenv import load_dotenv
import os
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import JSONLoader
import json
from pathlib import Path


class RegistrarEtiquetas:
    """
    Clase para gestionar etiquetas en ChromaDB utilizando embeddings de Cohere.
    Permite importar etiquetas desde un archivo JSON y recuperarlas mediante búsquedas de similitud.
    """

    def __init__(self, cohere_api_key, collection_name="etiquetas", model="embed-english-v3.0"):
        """
        Inicializa la clase, configurando Cohere embeddings y la base de datos ChromaDB.

        Args:
            cohere_api_key (str): Clave API para acceder a los servicios de Cohere.
            collection_name (str, optional): Nombre de la colección en ChromaDB. Por defecto, "etiquetas".
            model (str, optional): Modelo de embeddings de Cohere. Por defecto, "embed-english-v3.0".
        """
        # Inicializar embeddings y la base de datos
        self.embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key, model=model)
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings
        )

    def importar_etiquetas(self, file_path):
        """
        Importa etiquetas desde un archivo JSON y las almacena como documentos en ChromaDB.

        Args:
            file_path (str): Ruta del archivo JSON que contiene las etiquetas.

        Returns:
            None
        """
        data = json.loads(Path(file_path).read_text())
        etiquetas = data.get('etiquetas', [])

        # Crear documentos para cada etiqueta
        documentos = []
        for etiqueta in etiquetas:
            documento = Document(
                page_content=etiqueta['nombre'],  # Contenido textual principal de la etiqueta
                metadata={'nombre': etiqueta['nombre'], 'descripcion': etiqueta.get('descripcion', '')}
            )
            documentos.append(documento)

        # Agregar documentos a ChromaDB
        self.vector_store.add_documents(documents=documentos)
        print(f"{len(documentos)} etiquetas cargadas en ChromaDB.")

    def recuperar_etiquetas(self, query="", k=1):
        """
        Recupera etiquetas almacenadas en ChromaDB utilizando una consulta y búsquedas de similitud.

        Args:
            query (str, optional): Consulta textual para buscar etiquetas relacionadas. Por defecto, "" (vacío).
            k (int, optional): Número de etiquetas a recuperar. Por defecto, 1.

        Returns:
            list: Lista de metadatos de las etiquetas recuperadas.
        """
        results = self.vector_store.similarity_search(query=query, k=k)
        etiquetas_recuperadas = []

        for res in results:
            etiquetas_recuperadas.append(res.metadata['nombre'])

        return etiquetas_recuperadas


