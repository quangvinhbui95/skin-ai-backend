from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import random
import io

app = FastAPI()

# Cấu hình CORS để web shopbang.quangvinh.website truy cập được
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

    # Lấy kích thước ảnh để tạo tọa độ markers giả lập
    height, width, _ = img.shape

    # --- LOGIC MÔ PHỎNG CHẨN ĐOÁN KHẮT KHE (Để BOT không hoàn hảo) ---
    # Điểm càng thấp = Tình trạng da càng tệ (Cần được cải thiện)
    # Ta ưu tiên các khoảng điểm từ 3 đến 6 để luôn có khuyết điểm

    # 1. Giả lập điểm số các vấn đề da (0-10)
    scores = {
        "acne": random.randint(2, 6),      # Mụn viêm đỏ (Tệ -> Trung bình)
        "non_acne": random.randint(4, 7),  # Mụn không viêm
        "sebum": random.randint(2, 5),     # Sợi bã nhờn (Tệ)
        "scar": random.randint(3, 8),      # Sẹo
        "pigment": random.randint(1, 5),   # Sắc tố da (Rất tệ -> Tệ)
        "pore": random.randint(2, 6)       # Lỗ chân lông (Tệ)
    }

    # 2. Giả lập tọa độ các vấn đề da (Vẽ markers tím)
    # Tọa độ x, y tính theo pixel thực tế của ảnh
    markers = [
        {"x": random.randint(100, width-100), "y": random.randint(100, height-100)} 
        for _ in range(5) # Luôn tạo 5 điểm nhận diện khuyết điểm
    ]

    # 3. KẾT QUẢ TRẢ VỀ KHỚP VỚI SCRIPT.JS (Bao gồm điểm số và Markers)
    result = {
        "label": "Tăng tiết bã nhờn & Sắc tố",
        "advice": "AI phát hiện da bạn đang có vấn đề nghiêm trọng về sắc tố và đổ dầu. Hãy sử dụng Niacinamide hoặc Serum Giấm lựu để kiểm soát dầu và làm sáng da.",
        "cashback": "15.000đ",
        "shopee_link": "https://fashion.quangvinh.website",
        "scores": scores, # Object chứa các con số điểm đã random khắt khe
        "markers": markers # Object chứa tọa độ vẽ markers
    }
    
    return result

if __name__ == "__main__":
    import uvicorn
    # Render sẽ tự cấp Port, nhưng chạy local thì dùng 10000
    uvicorn.run(app, host="0.0.0.0", port=10000)
