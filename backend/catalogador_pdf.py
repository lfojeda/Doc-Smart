class CatalogadorPDF:
    """
    Clase para buscar documentos en ChromaDB y catalogarlos con etiquetas disponibles.
    """

    def __init__(self, vector_store_documentos, vector_store_etiquetas):
        """
        Inicializa la clase con las bases de datos vectoriales precargadas.

        Args:
            vector_store_documentos (Chroma): Base de datos Chroma precargada para documentos.
            vector_store_etiquetas (Chroma): Base de datos Chroma precargada para etiquetas.
        """
        self.vector_store_documentos = vector_store_documentos
        self.vector_store_etiquetas = vector_store_etiquetas

    def asignar_etiquetas_a_documento(self, texto, etiquetas):
        """
        Asigna etiquetas a un documento basado en su contenido.

        Args:
            texto (str): Contenido textual del documento.
            etiquetas (list): Lista de etiquetas disponibles.

        Returns:
            list: Lista de nombres de etiquetas asignadas al documento.
        """
        asignadas = []
        for etiqueta in etiquetas:
            if etiqueta['nombre'].lower() in texto.lower():
                asignadas.append(etiqueta['nombre'])
        return asignadas

    def buscar_documento(self, query, k=1):
        """
        Busca un documento en ChromaDB.

        Args:
            query (str): Consulta para buscar en los documentos.
            k (int): Número de documentos a recuperar.

        Returns:
            list: Lista de documentos recuperados.
        """
        return self.vector_store_documentos.similarity_search(query=query, k=k)

    def recuperar_etiquetas(self):
        """
        Recupera todas las etiquetas almacenadas en ChromaDB.

        Returns:
            list: Lista de etiquetas disponibles.
        """
        results = self.vector_store_etiquetas.similarity_search(query="", k=1000)
        return [res.metadata for res in results]

    def catalogar_documento(self, query):
        """
        Busca un documento en ChromaDB y lo cataloga con las etiquetas disponibles.

        Args:
            query (str): Consulta para buscar el documento.

        Returns:
            dict: Documento catalogado con etiquetas asignadas.
        """
        # Recuperar documento
        documentos = self.buscar_documento(query=query, k=1)
        if not documentos:
            raise ValueError("No se encontraron documentos para la consulta proporcionada.")

        documento = documentos[0]
        texto = documento.page_content

        # Recuperar etiquetas
        etiquetas = self.recuperar_etiquetas()

        # Asignar etiquetas al documento
        etiquetas_asignadas = self.asignar_etiquetas_a_documento(texto, etiquetas)

        # Actualizar metadatos del documento
        documento.metadata['etiquetas'] = etiquetas_asignadas
        return documento.metadata
