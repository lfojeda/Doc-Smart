from io import BytesIO, StringIO
import os
import subprocess
import streamlit as st

# Estilo personalizado para el resultado
st.markdown(
    """
    <style>
    .result-box {
        background-color: #f0f0f0;  /* Fondo gris claro */
        border: 2px solid #4f4f4f; /* Borde gris oscuro */
        padding: 10px;
        color: black;             /* Texto negro */
        font-family: monospace;   /* Fuente monoespaciada */
        white-space: pre-wrap;    /* Mantener formato del texto */
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# Configuración de la aplicación
st.title("PASO 1 - Subida de Documentos PDF para catalogar")
st.write("Sube tus archivos PDF para almacenarlos en el servidor.")

# Directorio donde se guardarán los PDFs y json
UPLOAD_DIR = "./app/smart_doc/data/pdf_docs"
UPLOAD_DIR_ETIQUETAS = "./app/smart_doc/data"

# Crear el directorio si no existe
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Subir archivos PDF
uploaded_files = st.file_uploader("Selecciona archivos PDF", type=['pdf'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Ruta completa del archivo guardado
        save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        
        # Guardar el archivo en el directorio
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Archivo '{uploaded_file.name}' subido y guardado en: {save_path}")

# Configuración de la aplicación
st.title("PASO 2 - Subida de archivo JSON con las etiquetas para los documentos")
st.write("Sube tu archivo JSON con las etiquetas para almacenarlos en el servidor.")

# Crear el directorio si no existe
if not os.path.exists(UPLOAD_DIR_ETIQUETAS):
    os.makedirs(UPLOAD_DIR_ETIQUETAS)

# Subir archivos PDF
uploaded_file = st.file_uploader("Selecciona archivo JSON", type=['json'])

if uploaded_file:
        # Ruta completa del archivo guardado
        save_path = os.path.join(UPLOAD_DIR_ETIQUETAS, "etiquetas.json")
        
        # Guardar el archivo en el directorio
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        st.success(f"Archivo '{uploaded_file.name}' subido y guardado en: {save_path}")

# Botón para ejecutar el script main.py
st.title("PASO 3 - Guardar en ChromaDB los documentos PDF y las etiquetas")
if st.button("Procesar"):
    # Ejecutar el script main.py
    script_path = "smart_doc/backend/main.py"  # Ruta al archivo main.py
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        # Mostrar el resultado en un div con estilo personalizado
        st.markdown(
            f"""
            <div class="result-box">
                Salida del Script:
                {result.stdout if result.stdout else "Sin salida estándar."}
                Errores:
                {result.stderr if result.stderr else "Sin errores reportados."}
            """,
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"Error al ejecutar el script: {e}")