import streamlit as st
import tempfile
import whisper
import ffmpeg
import torch
from googletrans import Translator
import subprocess

# Verifica se ffmpeg está instalado
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Função para converter áudio usando ffmpeg
def convert_audio_ffmpeg(input_path: str, output_path: str):
    """
    Converte um arquivo de áudio para formato WAV com 16kHz usando ffmpeg.
    """
    command = [
        "ffmpeg", "-i", input_path,  # Entrada
        "-ac", "1", "-ar", "16000",  # Mono e 16kHz
        "-y", output_path  # Sobrescreve o arquivo de saída
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Função para transcrição com Whisper
def transcribe_audio(model, audio_path: str, language: str = "en") -> str:
    """
    Transcreve o áudio usando Whisper.
    """
    result = model.transcribe(audio_path, language=language)
    return result["text"].strip()

def main():
    st.title("🎙️ Transcrição e Tradução de Áudio")
    st.write("Faça upload de um áudio em inglês para transcrição e tradução para português.")

    audio_file = st.file_uploader("📂 Arraste e solte ou selecione um arquivo", type=["wav", "mp3", "m4a"])

    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
            tmp_audio.write(audio_file.read())
            tmp_path = tmp_audio.name

        with st.spinner("🔄 Convertendo áudio..."):
            converted_path = tmp_path.replace(".wav", "_converted.wav")
            convert_audio_ffmpeg(tmp_path, converted_path)

        with st.spinner("📝 Transcrevendo áudio..."):
            model = whisper.load_model("base")
            transcription = transcribe_audio(model, converted_path, language="en")

        with st.spinner("🌍 Traduzindo para português..."):
            translator = Translator()
            translation = translator.translate(transcription, dest='pt').text

        st.subheader("🇧🇷 Tradução (Português):")
        st.write(translation)

        st.subheader("📝 Transcrição (Inglês):")
        st.write(transcription)


if __name__ == "__main__":
    if not check_ffmpeg():
        st.error("🚨 FFmpeg não está instalado corretamente!")
    else:
        main()
