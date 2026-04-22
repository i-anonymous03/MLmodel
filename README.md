# Taaranaa Mood Scanner

Taaranaa Mood Scanner is a passive emotion monitoring tool built using FastAPI and a premium HTML/CSS/JS frontend.

## Technology Stack

This project utilizes **Transfer Learning via DeepFace**, leveraging powerful CNN (Convolutional Neural Network) architectures. These models have been specifically trained on the **Kaggle FER-2013 (Facial Expression Recognition) Dataset**, enabling robust and accurate emotion detection from facial images.

## How to Run

1. **Install Dependencies**:
   Open your terminal and run the following command in the project directory to install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the FastAPI Server**:
   Start the application backend by running:
   ```bash
   uvicorn main:app --reload
   ```

3. **Open in Browser**:
   The application should be available on your localhost. Open your browser and navigate to `http://127.0.0.1:8000`.
