from flask import Flask, Response
import cv2

app = Flask(__name__)

# Update the camera index here
camera_index = 4
video_capture = cv2.VideoCapture(camera_index)

if not video_capture.isOpened():
    raise RuntimeError(f"Failed to open camera {camera_index}. Please check the camera connection.")


def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Simulate YOLO bounding box (draw a rectangle)
            height, width, _ = frame.shape
            cv2.rectangle(frame, (50, 50), (width - 50, height - 50), (0, 255, 0), 2)  # Green rectangle

            # Encode the frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame as part of the MJPEG stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
