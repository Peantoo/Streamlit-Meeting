import av
import streamlit as st
from streamlit_webrtc import (
    AudioProcessorBase,
    ClientSettings,
    WebRtcMode,
    webrtc_streamer,
)
from io import BytesIO
import requests
from Meeting-App.st_custom_components import st_audiorec

# URL of your the Flask app
FLASK_APP_URL = "https://meeting-summarizer.herokuapp.com/upload"

# Any code needed for the Streamlit app.


def main():
    st.title('🎙️ Meeting Summarizer')
    st.write("Click 'Start Meeting' to begin recording. Click 'End Meeting' to stop recording and see the transcription and summary.")
    
    if "recording" not in st.session_state:
        st.session_state.recording = False

    audio_data = None
    start_button = st.button("Start Meeting")
    stop_button = st.button("End Meeting")
    
    if start_button and not st.session_state.recording:
        st.session_state.recording = True
        audio_data = st_audiorec()

    if stop_button:
        if st.session_state.recording:
            st.session_state.recording = False

            if audio_data is not None:
                # Send the recorded audio to the Flask API
                response = requests.post(
                    FLASK_APP_URL,
                    files={"file": ("audio.wav", audio_data, "audio/wav")},
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
            st.warning("Please start the meeting first before stopping it.")

    if st.session_state.recording:
        st.warning("Meeting is in progress...")

if __name__ == "__main__":
    main()
