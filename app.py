import streamlit as st
import tempfile
import os
from PIL import Image
from deepface import DeepFace

st.set_page_config(page_title="Taaranaa Mood Scanner", page_icon="🎭")

st.title("Taaranaa Mood Scanner: Passive Emotion Monitoring")

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
                
            dominant_emotion = result.get('dominant_emotion', 'Unknown')
            
            # Display the result with a clean UI
            st.success(f"### Detected Emotion: {dominant_emotion.capitalize()} 🎭")
            
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")
        finally:
            # Clean up the temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception:
                    pass
