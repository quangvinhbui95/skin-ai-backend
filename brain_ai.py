from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import random

app = FastAPI()

# 1. Cấu hình CORS - Rất quan trọng để gọi trực tiếp từ trình duyệt
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_skin(file: UploadFile = File(...)):
    # Đọc file ảnh từ giao diện gửi lên
    request_object_content = await file.read()
    img_array = np.frombuffer(request_object_content, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Lấy kích thước ảnh để tạo tọa độ markers chính xác
    height, width, _ = img.shape

    # 2. MÔ PHỎNG LOGIC PHÂN TÍCH (Vinh sẽ thay bằng Model AI thật sau này)
    # Ở đây mình giả lập các chỉ số điểm số từ 0-10
    scores = {
        "acne": random.randint(6, 9),      # Mụn viêm
        "non_acne": random.randint(3, 5),  # Mụn không viêm
        "sebum": random.randint(7, 9),     # Sợi bã nhờn
        "scar": random.randint(1, 4),      # Sẹo
        "pigment": random.randint(2, 5),   # Sắc tố
        "pore": random.randint(6, 8)       # Lỗ chân lông
    }

    # Giả lập tọa độ các đốm mụn/vấn đề da để vẽ vòng tròn trên giao diện
    # Tọa độ x, y tính theo pixel thực tế của ảnh
    markers = [
        {"x": random.randint(100, width-100), "y": random.randint(100, height-100)} 
        for _ in range(5)
    ]

    # 3. KẾT QUẢ TRẢ VỀ KHỚP VỚI SCRIPT.JS
    result = {
        "label": "Tăng tiết bã nhờn & Mụn viêm",
        "advice": "AI phát hiện da bạn đang đổ dầu nhiều và có nốt viêm. Hãy sử dụng Giấm lựu Daesang để cân bằng độ pH và hỗ trợ giảm viêm từ bên trong.",
        "cashback": "15.000đ",
        "shopee_link": "https://fashion.quangvinh.website",
        "scores": scores,
        "markers": markers
    }
    
    return result

@app.get("/")
async def root():
    return {"status": "AI Server is running"}

if __name__ == "__main__":
    import uvicorn
    # Render sẽ tự cấp Port, nhưng chạy local thì dùng 10000
    uvicorn.run(app, host="0.0.0.0", port=10000)
