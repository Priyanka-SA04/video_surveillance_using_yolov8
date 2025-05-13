import streamlit as st


# Custom CSS styling
page_style = """
st.markdown(page_style, unsafe_allow_html=True)
<style>
/*Global body styling */
body, .stApp {
    background-color: #1a1a1a;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Header text */
h1, h2 {
    color: #00FFC6;
}

/* Buttons */
.stButton > button {
    background-color: #00b894;
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.6em 1.2em;
    transition: 0.3s ease;
}
.stButton > button:hover {
    background-color: #26de81;
    transform: scale(1.02);
}

/* File uploader and radio box styling */
.stRadio > div, .stFileUploader, .stTextInput {
    background-color: #2c2c2c;
    color: white;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
    border: 1px solid #444;
}

/* Iframe (live feed viewer) */
iframe {
    border: 3px solid #00FFC6;
    border-radius: 12px;
    box-shadow: 0 0 10px #00ffc688;
}

/* Sidebar or content containers */
.block-container {
    padding: 2rem 2rem;
}
</style>

"""

st.set_page_config(page_title="Intelligent Surveillance", layout="wide")
st.markdown(page_style, unsafe_allow_html=True)
st.title(" Intelligent Video Surveillance System")

# --- Layout ---
left_col, right_col = st.columns([1, 3])

stream_url = ""
stop_clicked = False

with left_col:
    st.markdown("## 📷 Select Video Source")
    option = st.radio("Choose source:", ["Upload from Device", "Webcam", "YouTube Link"])

    if option == "Upload from Device":
        video_file = st.file_uploader("Upload video", type=["mp4", "avi"])
        if video_file:
            with open("uploaded_video.mp4", "wb") as f:
                f.write(video_file.read())
            stream_url = "http://localhost:5000/video_feed/file/uploaded_video.mp4"

    elif option == "Webcam":
        stream_url = "http://localhost:5000/video_feed/webcam"

    elif option == "YouTube Link":
        youtube_url = st.text_input("Enter YouTube URL")
        if youtube_url:
            stream_url = f"http://localhost:5000/video_feed/youtube/{youtube_url}"

    start = st.button("▶ Start Detection")
    stop = st.button("⏹ Stop Detection")

with right_col:
    st.markdown("## 🎥 Live Feed")

    if start and stream_url:
        st.markdown(
            f'<iframe src="{stream_url}" width="100%" height="500"></iframe>',
            unsafe_allow_html=True
        )

    elif stop:
        st.warning("🛑 Detection Stopped — Refresh to reset.")

