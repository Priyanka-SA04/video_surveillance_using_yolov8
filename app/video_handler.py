

# import cv2
# from yt_dlp import YoutubeDL

# def get_youtube_capture(url):
#     ydl_opts = {
#         'format': 'best[ext=mp4]',
#         'quiet': True,
#         'noplaylist': True,
#     }
#     try:
#         with YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=False)
#             video_url = info_dict.get("url")
#             if video_url:
#                 print(f"✅ YouTube video stream found: {video_url}")
#                 return cv2.VideoCapture(video_url)
#             else:
#                 print("❌ No video URL found in info dict")
#                 return None
#     except Exception as e:
#         print(f"❌ yt_dlp failed to extract video: {e}")
#         return None

# def get_video_capture(source_type, source_path=None):
#     if source_type == 'webcam':
#         print("🎥 Starting webcam...")
#         return cv2.VideoCapture(0)

#     elif source_type == 'youtube':
#         if not source_path:
#             print("❌ No YouTube URL provided")
#             return None
#         return get_youtube_capture(source_path)

#     elif source_type == 'file':
#         if not source_path:
#             print("❌ No file path provided")
#             return None
#         print(f"📁 Loading video file: {source_path}")
#         return cv2.VideoCapture(source_path)

#     else:
#         raise ValueError(f"Invalid source_type: {source_type}")


import cv2
from yt_dlp import YoutubeDL
import os

def get_direct_youtube_stream(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get("url")
            if video_url:
                print(f"✅ YouTube video stream URL obtained")
                return video_url
            else:
                print("❌ No video URL found in info dict")
                return None
    except Exception as e:
        print(f"❌ yt_dlp failed to extract video URL: {e}")
        return None

def get_video_capture(source_type, source_path=None):
    if source_type == 'webcam':
        print("🎥 Starting webcam...")
        return cv2.VideoCapture(0)

    elif source_type == 'youtube':
        if not source_path:
            print("❌ No YouTube URL provided")
            return None
        print(f"🔗 Streaming YouTube video from: {source_path}")
        stream_url = get_direct_youtube_stream(source_path)
        if not stream_url:
            return None
        # Open direct stream URL with OpenCV VideoCapture
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            print("❌ Failed to open YouTube stream URL with OpenCV")
            return None
        return cap

    elif source_type == 'file':
        if not source_path:
            print("❌ No file path provided")
            return None
        if not os.path.isfile(source_path):
            print(f"❌ File not found: {source_path}")
            return None
        print(f"📁 Loading video file: {source_path}")
        cap = cv2.VideoCapture(source_path)
        if not cap.isOpened():
            print("❌ Failed to open video file")
            return None
        return cap

    else:
        print(f"❌ Invalid source_type: {source_type}")
        return None
