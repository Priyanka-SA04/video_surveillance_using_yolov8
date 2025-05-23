# from flask import Flask, Response
# import cv2

# from app.fire_detection import detect_fire_combined
# from app.fall_detection import detect_fall
# from app.theft_detection import detect_theft
# from app.video_handler import get_video_capture
# # from app.alert import send_voicemail_alert  # Optional alert system

# app = Flask(__name__)

# @app.route('/video_feed/<source_type>/<path:source_path>')
# @app.route('/video_feed/<source_type>', defaults={'source_path': None})
# def video_feed(source_type, source_path):
#     cap = get_video_capture(source_type, source_path)

#     def generate_frames():
#         while cap.isOpened():
#             success, frame = cap.read()
#             if not success:
#                 break

#             # -------- Fire Detection (YOLO + CNN) --------
#             frame, fire_detected = detect_fire_combined(frame)

#             # -------- Fall Detection --------
#             fall_boxes = detect_fall(frame)
#             for x1, y1, x2, y2 in fall_boxes:
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
#                 cv2.putText(frame, "🧍 Fall Detected", (x1, y1 - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

#             # -------- Theft Detection --------
#             theft_boxes = detect_theft(frame)
#             for x1, y1, x2, y2 in theft_boxes:
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
#                 cv2.putText(frame, "🚨 Theft Detected", (x1, y1 - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

#                 # Optional: Trigger alert (voicemail/email)
#                 # send_voicemail_alert("🚨 Theft detected in surveillance feed.")

#             # -------- Encode & Stream --------
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#         cap.release()

#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run(debug=True)
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Intelligent Video Surveillance</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-r from-teal-700 to-sky-700 text-white font-sans min-h-screen">

  <!-- Header -->
  <header class="py-4 shadow-lg mb-10">
    <h1 class="text-5xl p-2 font-extrabold text-center text-transparent bg-clip-text bg-gradient-to-r from-cyan-200 to-lime-300 ">
      Intelligent Video Surveillance System
    </h1>
  </header>

  <!-- Main Layout -->
  <div class="container mx-auto my-auto px-6 py-10 grid grid-cols-1 lg:grid-cols-4 gap-8">
    
    <!-- Left Controls Panel -->
    <div class="lg:col-span-1 bg-gray-800 p-6 rounded-2xl shadow-md">
      <h2 class="text-xl p-1 font-bold text-teal-400 mb-4">📷 Select Video Source</h2>
      <form id="video-form" class="space-y-4" enctype="multipart/form-data">
        <label class="flex items-center">
          <input type="radio" name="video_source" value="device" onclick="toggleSource(this.value)" class="text-teal-400 mr-2">
          <span>Upload from Device</span>
        </label>
        <label class="flex items-center">
          <input type="radio" name="video_source" value="webcam" onclick="toggleSource(this.value)" class="text-teal-400 mr-2">
          <span>Webcam</span>
        </label>
        <label class="flex items-center">
          <input type="radio" name="video_source" value="youtube" onclick="toggleSource(this.value)" class="text-teal-400 mr-2">
          <span>YouTube Link</span>
        </label>

        <!-- File Upload -->
        <input type="file" id="file-input" name="video" accept=".mp4,.avi" class="mt-2 w-full bg-gray-700 text-white rounded-lg border border-gray-600 p-2 hidden" onchange="handleFileUpload(this)" />

        <!-- YouTube Link -->
        <input type="url" id="youtube-url" placeholder="Enter YouTube URL" class="mt-2 w-full bg-gray-700 text-white rounded-lg border border-gray-600 p-2 hidden"/>

        <!-- Buttons -->
        <div class="flex flex-col space-y-4 pt-6">
          <button type="button" id="start-btn" onclick="startDetection()" disabled class="bg-gradient-to-r from-green-500 to-lime-500 hover:bg-teal-600 text-white font-semibold py-2 rounded-lg transition duration-300 disabled:opacity-50">
            ▶ Start Detection
          </button>
          <button type="button" id="stop-btn" onclick="stopDetection()" disabled class="bg-gradient-to-r from-amber-700 to-red-600 hover:bg-red-600 text-white font-semibold py-2 rounded-lg transition duration-300 disabled:opacity-50">
            ⏹ Stop Detection
          </button>
        </div>
      </form>
    </div>

    <!-- Right Live Feed -->
    <div class="lg:col-span-3 bg-gray-800 p-6 rounded-2xl shadow-md flex flex-col items-center justify-center">
      <h2 class="text-xl font-semibold text-teal-400 mb-6">🎥 Live Feed</h2>
      <iframe id="live-feed" src="" class="w-full max-w-[700px] aspect-square border-4 border-teal-400 rounded-xl shadow-md hidden"></iframe>
      <p id="status-warning" class="mt-6 text-yellow-400 font-semibold hidden text-center">🛑 Detection Stopped — Refresh to reset.</p>
    </div>
  </div>

  <!-- Footer -->
  <footer class="py-4 mt-24 text-center text-gray-400">
    <p>&copy; 2025 Intelligent Surveillance. All Rights Reserved.</p>
  </footer>

  <!-- JavaScript -->
  <script>
    let streamUrl = "";

    function toggleSource(source) {
      document.getElementById("file-input").classList.add("hidden");
      document.getElementById("youtube-url").classList.add("hidden");
      document.getElementById("start-btn").disabled = true;
      streamUrl = "";

      if (source === "device") {
        document.getElementById("file-input").classList.remove("hidden");
      } else if (source === "youtube") {
        document.getElementById("youtube-url").classList.remove("hidden");
      } else if (source === "webcam") {
        streamUrl = "http://localhost:5000/video_feed/webcam";
        document.getElementById("start-btn").disabled = false;
      }
    }

    document.getElementById("youtube-url").addEventListener("input", function () {
      document.getElementById("start-btn").disabled = this.value.trim() === "";
    });

    function handleFileUpload(input) {
      const file = input.files[0];
      if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('http://localhost:5000/upload_video', {
          method: 'POST',
          body: formData
        })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              streamUrl = `http://localhost:5000/video_feed/file/${data.filename}`;
              document.getElementById("start-btn").disabled = false;
            } else {
              alert("Upload failed: " + data.message);
            }
          })
          .catch(err => {
            alert("Error uploading file");
            console.error(err);
          });
      }
    }

    function startDetection() {
      if (!streamUrl && !document.getElementById("youtube-url").classList.contains("hidden")) {
        const youtubeUrl = document.getElementById("youtube-url").value;
        if (!youtubeUrl) {
          alert("Please enter a valid YouTube URL.");
          return;
        }
        streamUrl = `http://localhost:5000/video_feed/youtube/${encodeURIComponent(youtubeUrl)}`;
      }

      if (streamUrl) {
        const iframe = document.getElementById("live-feed");
        iframe.src = streamUrl;
        iframe.classList.remove("hidden");

        document.getElementById("stop-btn").disabled = false;
        document.getElementById("start-btn").disabled = true;
        document.getElementById("status-warning").classList.add("hidden");
      }
    }

    function stopDetection() {
      const iframe = document.getElementById("live-feed");
      iframe.src = "";
      iframe.classList.add("hidden");

      document.getElementById("stop-btn").disabled = true;
      document.getElementById("start-btn").disabled = false;
      document.getElementById("status-warning").classList.remove("hidden");
    }
  </script>

</body>
</html>
