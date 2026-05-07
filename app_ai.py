from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np

app = FastAPI()

# Cho phép CORS để PHP có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Skin Server is running!"}

@app.post("/analyze")
async def analyze_skin(file: UploadFile = File(...)):
    # Đọc ảnh từ request
    request_object_content = await file.read()
    nparr = np.frombuffer(request_object_content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Giả lập kết quả phân tích
    results = {
        "status": "success",
        "scores": {
            "acne": 9.0,
            "non_acne": 8.0,
            "sebum": 5.0,
            "scar": 6.0,
            "pigment": 3.0,
            "pore": 5.0
        },
        "markers": [
            {"x": 150, "y": 200, "type": "sebum"},
            {"x": 180, "y": 220, "type": "acne"},
            {"x": 160, "y": 250, "type": "pigment"}
        ]
    }
    
    return results
