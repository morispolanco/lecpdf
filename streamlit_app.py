import streamlit as st
import pdfplumber
import openai
import os

# Cargar la clave de la API de GPT-3 desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# Función para leer y extraer texto de un archivo PDF
def leer_pdf(archivo):
    with pdfplumber.open(archivo) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text()
    return texto

# Función para dividir el texto en fragmentos
def dividir_texto(texto, tamaño_fragmento):
    fragmentos = []
    for i in range(0, len(texto), tamaño_fragmento):
        fragmentos.append(texto[i:i+tamaño_fragmento])
    return fragmentos

# Función para formular la pregunta utilizando GPT-3
def formular_pregunta(pregunta, texto):
    entrada = pregunta + " [SEP] " + texto
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=entrada,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None
    )
    return respuesta.choices[0].text.strip()

# Aplicación principal
def main():
    st.title("Aplicación de Lectura de PDF y Preguntas y Respuestas")

    # Subir archivo
    archivo_subido = st.file_uploader("Subir PDF", type="pdf")

    if archivo_subido is not None:
        # Leer el PDF y extraer el texto
        texto = leer_pdf(archivo_subido)

        # Dividir el texto en fragmentos
        tamaño_fragmento = 1000
        fragmentos = dividir_texto(texto, tamaño_fragmento)

        # Entrada de la pregunta
        pregunta = st.text_input("Ingrese su pregunta")

        if st.button("Preguntar"):
            # Formular la pregunta utilizando GPT-3
            respuesta = formular_pregunta(pregunta, texto)

            st.write("Respuesta:", respuesta)

if __name__ == "__main__":
    main()
