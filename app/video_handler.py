import cv2
from yt_dlp import YoutubeDL

def get_youtube_capture(url):
    """
    Uses yt_dlp to extract a direct video stream URL from a YouTube link.
    """
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'quiet': True,
        'noplaylist': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get("url", None)
            if video_url:
                print(f"✅ YouTube video stream found: {video_url}")
                return cv2.VideoCapture(video_url)
            else:
                print("❌ No video URL found in info dict")
                return None
    except Exception as e:
        print(f"❌ yt_dlp failed to extract video: {e}")
        return None


def get_video_capture(source_type, source_path=None):
    """
    Unified video capture handler:
    - webcam: returns cv2.VideoCapture(0)
    - youtube: uses yt_dlp to stream
    - file: loads local video
    """
    if source_type == 'webcam':
        print("🎥 Starting webcam...")
        return cv2.VideoCapture(0)

    elif source_type == 'youtube':
        if not source_path:
            print("❌ No YouTube URL provided")
            return None
        return get_youtube_capture(source_path)

    elif source_type == 'file':
        if not source_path:
            print("❌ No file path provided")
            return None
        print(f"📁 Loading video file: {source_path}")
        return cv2.VideoCapture(source_path)

    else:
        raise ValueError(f"Invalid source_type: {source_type}")
