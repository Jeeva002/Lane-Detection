# Lane Detection

This project implements lane detection in road videos using OpenCV. The system identifies lane markings in each frame of a video, overlays them on the original frames, and saves the processed video.

---

## Features
- Converts frames to grayscale and applies Gaussian blur.
- Detects edges using the Canny Edge Detector.
- Isolates the region of interest (lanes) with a polygonal mask.
- Detects lane lines using the Hough Transform.
- Overlays the detected lanes on the original frames.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/lane_detection.git
   cd lane_detection
   
2. Install dependencies:
   ``` bash
   pip install -r requirements.txt

3. Place a driving video in the input_videos/ folder.
4. Run the script:
   ``` bash
   python lane_detection.py

   
