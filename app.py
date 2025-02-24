import streamlit as st
import whisper
from googletrans import Translator
import tempfile
import os
import numpy as np
import av

def main():
    st.title("Audio Transcription & Translation")
    st.write("Upload an English audio file to get Portuguese translation")

    # File uploader
    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg", "m4a"])

    if uploaded_file is not None:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        try:
            with st.spinner("Processing audio..."):
                # Load audio with PyAV
                container = av.open(tmp_path)
                audio = container.decode(audio=0)
                frames = [frame.to_ndarray() for frame in audio]
                audio_array = np.concatenate(frames)
                
                # Handle stereo audio
                if audio_array.ndim == 2:
                    audio_array = np.mean(audio_array, axis=1)
                
                # Load Whisper model
                model = whisper.load_model("base")
                result = model.transcribe(audio_array.astype(np.float32))
                transcription = result["text"]

            # Display transcription
            st.subheader("English Transcription:")
            st.write(transcription)

            # Translate to Portuguese
            with st.spinner("Translating..."):
                translator = Translator()
                translation = translator.translate(transcription, src='en', dest='pt').text

            # Display translation
            st.subheader("Portuguese Translation:")
            st.write(translation)

        except Exception as e:
            st.error(f"Error processing audio: {str(e)}")
            
        finally:
            # Clean up temporary files
            os.unlink(tmp_path)

if __name__ == "__main__":
    main()