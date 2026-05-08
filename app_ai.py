from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Haut.ai Style - AI Skin Analysis Server is running!"}

@app.post("/analyze")
async def analyze_skin(file: UploadFile = File(...)):
    request_object_content = await file.read()
    nparr = np.frombuffer(request_object_content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Lấy kích thước ảnh để đặt marker cho đúng vùng mặt
    height, width, _ = img.shape

    # Tạo các chỉ số ngẫu nhiên theo dải khoa học (Scale 1-10)
    # Giả định: 1-3 (Tốt), 4-7 (Trung bình), 8-10 (Cần chú ý/Nghiêm trọng)
    acne_score = round(random.uniform(1.0, 9.5), 1)
    sebum_score = round(random.uniform(2.0, 8.5), 1)
    
    # Logic liên đới: Nếu bã nhờn (sebum) cao, lỗ chân lông (pore) thường to theo
    pore_score = min(9.8, round(sebum_score + random.uniform(-1.0, 2.0), 1))
    
    pigment_score = round(random.uniform(1.5, 7.0), 1)
    non_acne = round(random.uniform(2.0, 6.0), 1)
    scar_score = round(random.uniform(1.0, 5.0), 1)

    # Tạo Marker ngẫu nhiên quanh khu vực trung tâm khuôn mặt
    num_markers = random.randint(5, 12)
    markers = []
    types = ["acne", "sebum", "pore", "pigment"]
    
    for _ in range(num_markers):
        markers.append({
            "x": random.randint(int(width*0.2), int(width*0.8)),
            "y": random.randint(int(height*0.2), int(height*0.8)),
            "type": random.choice(types)
        })

    results = {
        "status": "success",
        "scores": {
            "acne": acne_score,
            "non_acne": non_acne,
            "sebum": sebum_score,
            "scar": scar_score,
            "pigment": pigment_score,
            "pore": pore_score
        },
        "markers": markers
    }
    
    return results
