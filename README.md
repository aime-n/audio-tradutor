# Audio Transcription & Translation App

## Overview
This Streamlit application allows users to upload an English audio file, transcribe it using OpenAI's Whisper model, and translate the transcription into Portuguese using Google Translate.

## Features
- **Audio Upload**: Supports WAV, MP3, and M4A files.
- **Transcription**: Uses Whisper for high-accuracy speech-to-text conversion.
- **Translation**: Automatically translates English transcriptions to Portuguese.
- **FFmpeg Support**: Ensures compatibility with various audio formats.

## Installation
Ensure you have Python installed (recommended: Python 3.8+). Then, install the required dependencies:

```sh
pip install -r requirements.txt
```

## Running the Application
Run the Streamlit app using:

```sh
streamlit run app.py
```

## Deployment Without Exposing API Keys
To keep your OpenAI API key secure, set it as an environment variable instead of hardcoding it:

```sh
export OPENAI_API_KEY='your_api_key_here'
```

Alternatively, use a secrets manager or `.env` file and load it with `python-dotenv`.

## Common Issues & Solutions
### 1. **Transcription Errors Due to Accent (Indian English)**
**Accuracy: ~70%**
- The Whisper model captures the general meaning but struggles with certain phrases.
- Common issues include:
  - Missing important words (e.g., "less" omitted in "100 square meters less").
  - Broken sentence structures leading to confusion.
  - Misinterpreted proper nouns or technical terms.

**Solution:**
- Use **Whisper large** for better accuracy.
- Apply **post-processing** to correct misheard words before translation.
- If recurring, consider training a custom model on Indian English accents.

### 2. **Translation Issues**
- Google Translate does well for general text but struggles with:
  - Business/technical terminology.
  - Grammatical structure preservation.
- Example error:
  - **Incorrect:** "não a citação será feita por scones."
  - **Correct:** "Não inclua na cotação o que será feito pelo [Scones (?)]."

**Solution:**
- Use **DeepL** for higher translation accuracy.
- Apply **manual post-editing** for critical documents.

### 3. **FFmpeg Not Found Error**
If you get:

```sh
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```
Install FFmpeg manually:

```sh
sudo apt update && sudo apt install ffmpeg
```
Or on Windows, install FFmpeg and add it to your system PATH.

### 4. **Whisper AttributeError**
If you encounter:

```sh
AttributeError: module 'whisper' has no attribute 'load_model'
```
Ensure you installed the correct package:

```sh
pip install openai-whisper
```

## Future Improvements
- **Improve accuracy for Indian accents** using fine-tuning.
- **Better translation quality** by switching to DeepL.
- **Add multi-language support** beyond English and Portuguese.

---
Developed by Aimê Nobrega.

