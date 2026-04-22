import os
import tempfile
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from deepface import DeepFace

app = FastAPI(title="Taaranaa Mood Scanner")

def derive_complex_emotion(emotion_dict):
    """
    Blends the top 2 emotions if the secondary emotion has a significant probability.
    Provides a richer set of 10+ emotions.
    """
    sorted_emotions = sorted(emotion_dict.items(), key=lambda item: item[1], reverse=True)
    primary_emotion, primary_score = sorted_emotions[0]
    secondary_emotion, secondary_score = sorted_emotions[1]
    
    if secondary_score < 10.0:
        return primary_emotion.capitalize()
        
    emotions_set = {primary_emotion, secondary_emotion}
    
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

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    temp_file_path = None
    try:
        # Save uploaded file to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Run DeepFace analysis
        results = DeepFace.analyze(temp_file_path, actions=['emotion'], enforce_detection=False)
        
        if isinstance(results, list):
            result = results[0]
        else:
            result = results
            
        emotions_dict = result.get('emotion', {})
        
        # DeepFace returns numpy float32 values which are not JSON serializable. 
        # Convert them to native python floats:
        emotions_dict = {k: float(v) for k, v in emotions_dict.items()}
        
        complex_emotion = derive_complex_emotion(emotions_dict)
        
        return JSONResponse(content={
            "success": True,
            "complex_emotion": complex_emotion,
            "breakdown": emotions_dict
        })
        
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        }, status_code=500)
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass

# Serve static files for the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
