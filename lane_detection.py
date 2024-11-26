import cv2
import numpy as np
import os

def region_of_interest(image, vertices):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def draw_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
    return cv2.addWeighted(image, 0.8, line_image, 1, 0)

def detect_lane_lines(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)
    
    # Define region of interest (ROI)
    height, width = edges.shape
    roi_vertices = np.array([[
        (width * 0.1, height),
        (width * 0.4, height * 0.6),
        (width * 0.6, height * 0.6),
        (width * 0.9, height)
    ]], dtype=np.int32)
    cropped_edges = region_of_interest(edges, roi_vertices)
    
    # Detect lines using Hough Transform
    lines = cv2.HoughLinesP(cropped_edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=150)
    
    # Draw lines on the original frame
    return draw_lines(frame, lines)

def process_video(input_path, output_path):
    # Open input video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {input_path}")
        return

    # Get video properties
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define video writer
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    print("Processing video...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process each frame for lane detection
        processed_frame = detect_lane_lines(frame)

        # Write the frame to output video
        out.write(processed_frame)

    print(f"Processed video saved to {output_path}")

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    input_video_path = "input_videos/sample_video.mp4"
    output_video_path = "output_videos/lane_detected_video.avi"

    # Create output folder if it doesn't exist
    os.makedirs("output_videos", exist_ok=True)

    # Process the video for lane detection
    process_video(input_video_path, output_video_path)

