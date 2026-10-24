import os
import cv2
import pandas as pd
import sys
import io

# Sửa lỗi in tiếng Việt ra console trên Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import easyocr
    from deep_translator import GoogleTranslator
except ImportError:
    print("Vui lòng mở Terminal và chạy lệnh sau để cài đặt các thư viện cần thiết:")
    print("pip install easyocr pandas openpyxl deep-translator opencv-python")
    exit()

IMG_DIR = r"E:\CwAI\CwAI_Screen\IMG"
OUTPUT_EXCEL = r"E:\CwAI\CwAI_Screen\cards_data.xlsx"

print("Đang khởi tạo công cụ nhận diện chữ tiếng Trung (Lần đầu chạy có thể mất 1-2 phút để tải model)...")
# Khởi tạo bộ đọc tiếng Trung giản thể ('ch_sim') và tiếng Anh ('en' cho số/ký hiệu)
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
translator = GoogleTranslator(source='zh-CN', target='vi')

# Từ điển chuẩn hóa từ ngữ cho phù hợp với game Vương Giả Vạn Tượng Kỳ (Auto Chess)
# Google Dịch đôi khi dùng từ quá máy móc, ta sẽ sửa lại cho giống thuật ngữ game
GAME_TERMS = {
    "người chơi cờ": "kỳ thủ",
    "người chơi": "kỳ thủ",
    "giá trị sinh mệnh": "máu",
    "điểm sinh mệnh": "máu",
    "sức khỏe": "máu",
    "năng lượng": "năng lượng",
    "bạo kích": "chí mạng",
    "tỷ lệ bạo kích": "tỉ lệ chí mạng",
    "hút máu ma thuật": "hút máu phép",
    "hút máu vật lý": "hút máu vật lý",
    "sát thương ma thuật": "sát thương phép",
    "vật phẩm": "trang bị",
    "trận đấu": "vòng đấu",
    "anh hùng": "tướng",
    "thức tỉnh": "thức tỉnh",
    "cấp độ": "cấp",
}

def standardize_translation(text):
    text_lower = text.lower()
    for key, val in GAME_TERMS.items():
        text_lower = text_lower.replace(key, val)
    # Trả về text đã sửa (viết hoa chữ cái đầu cho đẹp)
    return text_lower.capitalize()

data = []
files = [f for f in os.listdir(IMG_DIR) if f.endswith(('.png', '.jpg'))]
print(f"Tìm thấy {len(files)} ảnh trong thư mục. Bắt đầu xử lý...")

for idx, filename in enumerate(files):
    filepath = os.path.join(IMG_DIR, filename)
    img = cv2.imread(filepath)
    
    if img is None:
        continue
    
    # Dựa vào khung ảnh (240x360), chia làm 2 vùng cần lấy chữ
    # Vùng 1 (Tên thẻ): Cắt y từ 180 đến 245, x từ 10 đến 230
    title_roi = img[180:245, 10:230]
    
    # Vùng 2 (Mô tả): Cắt y từ 245 đến 350, x từ 10 đến 230
    desc_roi = img[245:350, 10:230]
    
    # OCR Nhận diện chữ
    title_result = reader.readtext(title_roi, detail=0, paragraph=True)
    desc_result = reader.readtext(desc_roi, detail=0, paragraph=True)
    
    title_text = " ".join(title_result).strip()
    desc_text = " ".join(desc_result).strip()
    
    # Bỏ qua nếu ảnh chụp lỗi không có chữ
    if not title_text and not desc_text:
        continue
        
    # Dịch mô tả sang tiếng Việt
    translated_desc = ""
    if desc_text:
        try:
            translated_desc = translator.translate(desc_text)
            # Chuẩn hóa từ ngữ game
            translated_desc = standardize_translation(translated_desc)
        except Exception as e:
            translated_desc = f"[Lỗi dịch: {e}]"
            
    print(f"[{idx+1}/{len(files)}] {filename}")
    print(f"  + Tên: {title_text}")
    print(f"  + Mô tả: {translated_desc}")
    print("-" * 30)
    
    data.append({
        "Tên Thẻ (Tiếng Trung)": title_text,
        "Mô tả (Tiếng Việt)": translated_desc
    })

# Xuất ra file Excel
if data:
    df = pd.DataFrame(data)
    df.to_excel(OUTPUT_EXCEL, index=False)
    print(f"\n=> HOÀN THÀNH! Đã xuất {len(data)} thẻ ra file Excel thành công.")
    print(f"=> Đường dẫn file: {OUTPUT_EXCEL}")
else:
    print("Không trích xuất được chữ nào từ các ảnh.")
