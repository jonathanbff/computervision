# README for Python Experiments: Interactive Pose and Expression Detection

This repository contains two Python-based experiments utilizing OpenCV and MediaPipe for real-time video processing and interaction. The projects are aimed at demonstrating the capabilities of computer vision and pose detection in creating engaging, interactive applications.

## Experiment 1: Ball Catching Game

### Overview
This experiment creates an interactive game where players use their body movements to catch a virtual ball on the screen. It uses OpenCV for image processing and MediaPipe for pose detection.

### How to Run
1. Ensure you have Python installed on your system.
2. Install the required libraries: OpenCV and MediaPipe.
3. Run the script `ball_catching_game.py`.

### Features
- **Pose Detection:** Utilizes MediaPipe's pose detection to track the player's movements.
- **Interactive Gameplay:** Players use their body part (e.g., hand) to catch a virtual ball.
- **Customizable Settings:** Options to select the body part for interaction and toggle mirror mode.
- **Real-time Feedback:** Displays current score and updates the game in real-time.

### Key Components
- **Video Capture & Processing:** Captures video frames and processes them for pose detection.
- **Dynamic Object Interaction:** Generates a virtual ball with random positions and colors.
- **Collision Detection:** Checks if the selected body part touches the virtual ball.
- **User Interface:** Displays a simple menu for game controls and shows the player's score.

## Experiment 2: Sit/Stand & Smile Detection

### Overview
This application detects and tracks whether a person is sitting or standing and recognizes facial expressions (specifically, smiling). It leverages both pose and facial landmark detection using MediaPipe.

### How to Run
1. Ensure Python is installed on your system.
2. Install OpenCV and MediaPipe libraries.
3. Execute the script `sit_stand_smile_detection.py`.

### Features
- **Pose Analysis:** Detects and analyzes the body posture (sitting or standing).
- **Facial Expression Recognition:** Identifies if the person is smiling using facial landmarks.
- **State Change Counter:** Counts and displays the number of times the person changes from sitting to standing and vice versa.
- **Real-time Display:** Shows the current state, smile status, and shoulder movement.

### Key Components
- **Video Capture & Pose Detection:** Processes video frames for body pose analysis.
- **Facial Landmark Detection:** Identifies and processes facial landmarks to detect smiling.
- **Posture Analysis:** Differentiates between sitting and standing by comparing the relative positions of hips and knees.
- **Interactive Feedback:** Provides instant feedback on the screen about the person's posture and facial expression.

## Installation

To run these experiments, you need to install certain Python libraries. You can install these using pip:

```bash
pip install opencv-python
pip install mediapipe
```

## Usage

After installing the required libraries, you can run each script from the command line:

```bash
python ball_catching_game.py
```

or

```bash
python sit_stand_smile_detection.py
```

Ensure your webcam is functional, as the experiments rely on real-time video input.

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request for any enhancements.

## License
This project is open-sourced under the MIT License. See the LICENSE file for more details.
