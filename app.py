import streamlit as st
import tempfile
import os
from PIL import Image
from deepface import DeepFace

def derive_complex_emotion(emotion_dict):
    """
    Blends the top 2 emotions if the secondary emotion has a significant probability.
    Provides a richer set of 10+ emotions.
    """
    sorted_emotions = sorted(emotion_dict.items(), key=lambda item: item[1], reverse=True)
    primary_emotion, primary_score = sorted_emotions[0]
    secondary_emotion, secondary_score = sorted_emotions[1]
    
    # Threshold for considering the secondary emotion (e.g., > 10%)
    if secondary_score < 10.0:
        return primary_emotion.capitalize()
        
    emotions_set = {primary_emotion, secondary_emotion}
    
    # Blending Logic
    if {"happy", "surprise"}.issubset(emotions_set): return "Excited"
    elif {"angry", "sad"}.issubset(emotions_set): return "Frustrated"
    elif {"surprise", "neutral"}.issubset(emotions_set): return "Confused"
    elif {"fear", "surprise"}.issubset(emotions_set): return "Alarmed"
    elif {"disgust", "angry"}.issubset(emotions_set): return "Contemptuous"
    elif {"sad", "happy"}.issubset(emotions_set): return "Nostalgic / Bittersweet"
    elif {"fear", "sad"}.issubset(emotions_set): return "Anxious"
    elif {"fear", "angry"}.issubset(emotions_set): return "Hostile"
    elif {"happy", "neutral"}.issubset(emotions_set): return "Content"
    elif {"sad", "neutral"}.issubset(emotions_set): return "Melancholic"
    elif {"disgust", "sad"}.issubset(emotions_set): return "Bitter"
        
    return f"{primary_emotion.capitalize()} (with hints of {secondary_emotion})"

st.set_page_config(page_title="Taaranaa Mood Scanner", page_icon="🎭")

st.title("Taaranaa Mood Scanner: Passive Emotion Monitoring")
st.caption("Powered by Deep Learning CNNs trained on the Kaggle FER-2013 (Facial Expression Recognition) Dataset.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    with st.spinner('Analyzing emotion...'):
        temp_file_path = None
        try:
            # Save uploaded image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_file_path = temp_file.name

            # Run DeepFace analysis
            results = DeepFace.analyze(temp_file_path, actions=['emotion'], enforce_detection=False)
            
            # Extract the result
            if isinstance(results, list):
                result = results[0]
            else:
                result = results
                
            emotions_dict = result.get('emotion', {})
            complex_emotion = derive_complex_emotion(emotions_dict)
            
            # Display the result with a clean UI
            st.success(f"### Detected Emotion: **{complex_emotion}** 🎭")
            
            # Optionally show the raw breakdown
            with st.expander("Show Emotion Breakdown"):
                st.bar_chart(emotions_dict)
                
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")
        finally:
            # Clean up the temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception:
                    pass
