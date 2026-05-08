from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import io

app = FastAPI()

# Cấu hình CORS để web shopbang.quangvinh.website truy cập được
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_skin(file: UploadFile = File(...)):
    # 1. Đọc file ảnh từ giao diện gửi lên
    request_object_content = await file.read()
    img_array = np.frombuffer(request_object_content, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # 2. Logic xử lý giả lập (Vinh sẽ thay bằng AI model sau)
    # Ví dụ: Nếu phát hiện nhiều sắc tố đỏ -> chẩn đoán Mụn viêm
    
    result = {
        "label": "Mụn viêm đỏ",
        "advice": "AI phát hiện vùng da bị viêm. Bạn nên dùng Giấm lựu hoặc serum phục hồi.",
        "cashback": "15.000đ",
        "shopee_link": "https://fashion.quangvinh.website"
    }
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)