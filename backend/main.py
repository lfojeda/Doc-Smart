# Usamos la clase RegistrarEtiquetas
import json
import os
from dotenv import load_dotenv
from cargador_pdf import CargadorPDF
from cargador_etiquetas import RegistrarEtiquetas


load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
#Cargar etiquetas
registrar_etiquetas = RegistrarEtiquetas(cohere_api_key=api_key)

# Importar etiquetas desde un archivo JSON
file_path = './app/smart_doc/data/etiquetas.json'
registrar_etiquetas.importar_etiquetas(file_path)

# Recuperar etiquetas almacenadas
etiquetas = registrar_etiquetas.recuperar_etiquetas(query="", k=20)

# Imprimir las etiquetas recuperadas
formatted_json = json.dumps(etiquetas, indent=4, ensure_ascii=False)
print(formatted_json)

# Inicializar el catalogador
cargador = CargadorPDF(api_key=api_key)

# Ruta de la carpeta con PDFs - cargar pdfs y etiquetas para catalogar
pdf_folder_path = './app/smart_doc/data/pdf_docs'
cargador.cargar_documentos_pdf(pdf_folder_path)
