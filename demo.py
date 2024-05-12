import streamlit as st
import anthropic
import fitz  # Biblioteca PyMuPDF

with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")

st.title("Asistente Virtual UPIICSA - EQUIPO 5 - APLICACIONES DE REDES🗞️")
st.write("Empieza a chatear ...🚀")

uploaded_file = st.file_uploader("Sube un archivo.", type=("txt", "md", "pdf"))

question = st.text_input(
    "Pregúntame cualquier cosa sobre el contenido del archivo.",
    placeholder="Escribe tu pregunta.",
    disabled=not uploaded_file,
)

if uploaded_file and question and not anthropic_api_key:
    st.info("Añade tu API KEY.")

if uploaded_file and question and anthropic_api_key:
    if uploaded_file.type == "application/pdf":
        # Leer contenido del PDF
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        article = ""
        for page in pdf_doc:
            article += page.get_text()
    else:
        article = uploaded_file.read().decode()

    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\\n\\n<article>
    {article}\\n\\n</article>\\n\\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=anthropic_api_key)
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-2",
        max_tokens_to_sample=300,
    )

    st.write("### Respuesta")
    st.write(response.completion)
