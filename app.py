"""
    Streamlit App: Improved Audio Transcription & Translation

    This app uploads an English audio file, transcribes the entire audio using Whisper
    with adjusted decoding options (e.g., temperature=0.0 and beam search), performs simple
    post-processing to remove duplicate phrases, and then translates the transcription to
    Portuguese using googletrans.

    Key Adjustments:
    1. **Decoding Options**:
       - Set temperature=0.0 and use beam search (beam_size=5) to reduce randomness.
    2. **Post-Processing**:
       - Split the transcription into sentences and remove consecutive duplicates.
"""

import streamlit as st
import tempfile
import whisper
import librosa
import numpy as np
from googletrans import Translator

def load_audio_no_ffmpeg(file_path: str, sr: int = 16000) -> np.ndarray:
    """
    Loads an audio file using librosa without relying on ffmpeg.
    
    Args:
        file_path (str): Path to the audio file.
        sr (int): Target sample rate.
    
    Returns:
        np.ndarray: Mono audio time series.
    """
    audio, _ = librosa.load(file_path, sr=sr, mono=True)
    return audio

def transcribe_full_audio(model, audio_path: str, language: str = "en") -> str:
    """
    Transcribes the full audio by splitting it into 30-second chunks,
    decoding each with Whisper using stricter decoding options, and concatenating the results.
    
    Args:
        model: Loaded Whisper model.
        audio_path (str): Path to the audio file.
        language (str): Language code of the audio.
    
    Returns:
        str: Combined transcription.
    """
    # Load full audio
    audio = load_audio_no_ffmpeg(audio_path, sr=16000)
    
    # Define chunk size: 30 seconds of audio at 16kHz
    chunk_size = 30 * 16000
    chunks = [audio[i:i + chunk_size] for i in range(0, len(audio), chunk_size)]
    
    full_transcription = []
    for chunk in chunks:
        # Pad or trim the chunk to the required length
        chunk = whisper.pad_or_trim(chunk)
        # Compute the log-Mel spectrogram
        mel = whisper.log_mel_spectrogram(chunk).to(model.device)
        # Use stricter decoding parameters to reduce errors:
        options = whisper.DecodingOptions(
            language=language,
            fp16=False,
            temperature=0.0,  # less randomness
            beam_size=5      # beam search for better results
        )
        result = whisper.decode(model, mel, options)
        full_transcription.append(result.text.strip())
    
    # Concatenate all chunk transcriptions
    transcription = " ".join(full_transcription)
    
    # Post-processing: Remove consecutive duplicate sentences
    sentences = transcription.split('. ')
    filtered_sentences = []
    for s in sentences:
        s = s.strip()
        if not filtered_sentences or s.lower() != filtered_sentences[-1].lower():
            filtered_sentences.append(s)
    return '. '.join(filtered_sentences)

def main():
    st.title("Transcrição e tradução de áudio")
    # st.write("Carregue um arquivo de áudio em inglês para transcrever e traduzir para o português.")
    
    audio_file = st.file_uploader("Arraste e solte um arquivo de áudio ou clique para procurar", type=["wav", "mp3", "m4a"])


    if audio_file is not None:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        
        with st.spinner("Processing audio..."):
            # Load Whisper model
            model = whisper.load_model("base")
            # Transcribe the full audio with improved settings
            transcription = transcribe_full_audio(model, tmp_path, language="en")
            
            # Translate the transcription to Portuguese
            translator = Translator()
            translation = translator.translate(transcription, dest='pt').text

        st.subheader("Tradução (Português):")
        st.write(translation)

        st.subheader("Transcrição (Inglês):")
        st.write(transcription)
        


if __name__ == "__main__":
    main()
