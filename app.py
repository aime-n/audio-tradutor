import streamlit as st
import tempfile
import whisper
import ffmpeg
import os
import subprocess
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

# Verifica dependências
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Carrega configurações do ambiente
load_dotenv()

# Cache do modelo Whisper
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

# Cache dos agentes
@st.cache_resource
def initialize_agents():
    config_list = [{
        "model": "deepseek/deepseek-r1-zero:free",
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        "base_url": "https://openrouter.ai/api/v1",
        "price": [0, 0]
    }]

    llm_config = {
        "config_list": config_list,
        "timeout": 600,
    }

    return {
        "transcriber": AssistantAgent(
            name="transcriber",
            system_message="Você é um especialista em transcrição de áudio. Transcreva o áudio com precisão.",
            llm_config=llm_config
        ),
        "language_detector": AssistantAgent(
            name="language_detector",
            system_message="Identifique o idioma do texto. Responda APENAS com o código ISO 639-1.",
            llm_config=llm_config
        ),
        "translator": AssistantAgent(
            name="translator",
            system_message="Traduza o texto para português. Preserve o significado e o tom. Responda APENAS com a tradução.",
            llm_config=llm_config
        ),
        "text_editor": AssistantAgent(
            name="text_editor",
            system_message="""Você é um editor profissional. Melhore a legibilidade do texto:
            1. Adicione pontuação correta
            2. Separe em parágrafos lógicos
            3. Corrija capitalização
            4. Mantenha o conteúdo original
            Responda APENAS com o texto limpo, sem nenhuma formatação extra (como markdown ou boxed)""",
            llm_config=llm_config
        ),
        "summarizer": AssistantAgent(
            name="summarizer",
            system_message="Gere um resumo conciso em português com os pontos principais. Responda APENAS com o resumo.",
            llm_config=llm_config
        ),
        "todo_extractor": AssistantAgent(
            name="todo_extractor",
            system_message="Extraia itens de ação como marcadores em português. Responda APENAS com a lista.",
            llm_config=llm_config
        ),
        "user_proxy": UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            code_execution_config=False,
            max_consecutive_auto_reply=1
        )
    }

# Função para processar áudio
def process_audio(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_audio.write(uploaded_file.read())
        converted_path = tmp_audio.name.replace(".wav", "_converted.wav")
        
        ffmpeg.input(tmp_audio.name).output(
            converted_path,
            ac=1, ar=16000
        ).overwrite_output().run(quiet=True)
        
        return converted_path

def main():
    st.title("🎙️ Assistente de Áudio Inteligente")
    st.write("Upload de áudio para análise completa com IA")
    
    audio_file = st.file_uploader("Carregar arquivo de áudio", type=["wav", "mp3", "m4a"])
    
    if audio_file:
        # Carrega o modelo Whisper e os agentes (usando cache)
        model = load_whisper_model()
        agents = initialize_agents()
        
        with st.status("Processando...", expanded=True) as status:
            # Conversão de áudio
            st.write("🔁 Convertendo áudio...")
            audio_path = process_audio(audio_file)
            
            # Transcrição
            st.write("📝 Transcrevendo...")
            transcription = model.transcribe(audio_path)
            text, detected_lang = transcription["text"], transcription["language"]
            
            # Tradução se necessário
            if detected_lang != 'pt':
                st.write("🌐 Traduzindo...")
                text = agents["user_proxy"].initiate_chat(
                    agents["translator"],
                    message=f"Traduza este texto para português: {text}"
                ).chat_history[-1]['content'].strip()
            
            # Melhorar fluidez do texto
            st.write("✒️ Melhorando fluidez do texto...")
            edited_text = agents["user_proxy"].initiate_chat(
                agents["text_editor"],
                message=f"Formate este texto para melhor legibilidade: {text}"
            ).chat_history[-1]['content'].strip()
            
            # Sumarização
            st.write("📌 Resumindo...")
            summary = agents["user_proxy"].initiate_chat(
                agents["summarizer"],
                message=f"Resuma este texto: {edited_text}"
            ).chat_history[-1]['content'].strip()
            
            # Extração de TODOs
            st.write("✅ Extraindo ações...")
            todos = agents["user_proxy"].initiate_chat(
                agents["todo_extractor"],
                message=f"Extraia itens de ação deste texto: {edited_text}"
            ).chat_history[-1]['content'].strip()

            status.update(label="Processamento completo!", state="complete")
        
        # Exibição dos resultados
        st.subheader("📄 Transcrição Original")
        st.write(text)

        st.subheader("📝 Texto Melhorado")
        st.write(edited_text)
        
        st.subheader("📌 Resumo Executivo")
        st.write(summary)
        
        st.subheader("✅ Itens de Ação")
        st.write(todos)

if __name__ == "__main__":
    if not check_ffmpeg():
        st.error("FFmpeg não está instalado!")
    elif not os.getenv("OPENROUTER_API_KEY"):
        st.error("Chave API não encontrada!")
    else:
        main()