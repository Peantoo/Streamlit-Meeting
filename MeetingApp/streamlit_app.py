import av
import streamlit as st
from io import BytesIO
import requests
from st_custom_components import st_audiorec

FLASK_APP_URL = "https://meeting-summarizer.herokuapp.com/upload"

def main():
    st.title('🎙️ Meeting Summarizer')
    st.write("Record a meeting and receive a summary of the discussion.")
    
    audio_data = st_audiorec()
    
    if audio_data is not None:
        audio_file = BytesIO(audio_data)
        audio_file.seek(0)
    
    start_button = st.button("Start Recording")
    stop_button = st.button("Stop")
    reset_button = st.button("Reset")
    download_button = st.button("Download")
    summarize_button = st.button("Summarize")

    if summarize_button:
        if audio_data is not None:
            # Send the recorded audio to the Flask API
            response = requests.post(
                FLASK_APP_URL,
                files={"file": ("audio.wav", audio_file, "audio/wav")},
            )

            if response.status_code == 200:
                result = response.json()
                transcription_text = result["transcription"]
                summary_text = result["summary"]

                st.write('**Transcription:**')
                st.write(transcription_text)

                st.write('**Summary:**')
                st.write(summary_text)

            else:
                st.error(f"Error processing the audio. Please try again. (Error: {response.status_code})")
        else:
            st.warning("Please record the audio before summarizing.")
            
if __name__ == "__main__":
    main()
