import cv2
import requests
import numpy as np

# URL of the video feed from the server
stream_url = "http://192.168.178.25:5000/video_feed"


def stream_video():
    # Open the video stream using requests
    video_stream = requests.get(stream_url, stream=True)

    if video_stream.status_code != 200:
        raise RuntimeError(f"Failed to connect to server at {stream_url}. HTTP status: {video_stream.status_code}")

    # Stream processing
    bytes_buffer = b""
    for chunk in video_stream.iter_content(chunk_size=1024):
        bytes_buffer += chunk
        # Look for the start and end of a frame in the MJPEG stream
        a = bytes_buffer.find(b'\xff\xd8')  # JPEG start
        b = bytes_buffer.find(b'\xff\xd9')  # JPEG end
        if a != -1 and b != -1:
            # Extract the JPEG frame
            jpg = bytes_buffer[a:b + 2]
            bytes_buffer = bytes_buffer[b + 2:]

            # Decode the JPEG frame to OpenCV format
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            if frame is not None:
                # Display the frame
                cv2.imshow("Video Stream", frame)

                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        stream_video()
    except Exception as e:
        print(f"Error: {e}")
