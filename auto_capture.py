import os
import time

try:
    import pydirectinput
    import pyautogui
    import keyboard
except ImportError:
    print("Thiếu thư viện. Vui lòng mở Terminal/CMD và chạy lệnh sau:")
    print("pip install pydirectinput pyautogui keyboard pillow")
    exit()

# Thư mục lưu ảnh
SAVE_DIR = r"E:\CwAI\CwAI_Screen\IMG"
os.makedirs(SAVE_DIR, exist_ok=True)

# Đã tăng chiều cao (Height) từ 305 lên 360 để lấy hết phần dưới của thẻ bài
# Tọa độ X, Y cũng được chỉnh lại để bao trọn viền
CARD_REGION = (1655, 120, 240, 360)

# --- Cấu hình lưới tọa độ phần Thẻ Vàng (3阶) ---
START_X = 75 
# Tọa độ Y tâm ban đầu là 238. Đã cộng thêm 15 pixel để chuột bấm sâu xuống nửa dưới của hình tròn!
START_Y = 253 

# Khoảng cách giữa các nút (Đã đo đạc lại cực kỳ chính xác)
SPACING_X = 101.5 
SPACING_Y = 95.85 # Tăng từ 95.0 lên 95.85 để chống lệch khi xuống các hàng dưới cùng

# Bắt đầu chạy tiếp từ vị trí bạn đang chọn: Hàng 6, Cột 1
START_ROW_INDEX = 5 # (0-indexed)
START_COL_INDEX = 0 # (0-indexed)

print("======================================================")
print(" CHƯƠNG TRÌNH AUTO CLICK - CHỤP THẺ VÀNG (TIẾP TỤC)")
print(f" Ảnh sẽ được lưu tại: {SAVE_DIR}")
print("======================================================")
print("HƯỚNG DẪN:")
print("1. KHÔNG CUỘN CHUỘT, mở màn hình game y như ảnh.")
print("2. Sau khi chạy, bạn có 5 GIÂY để mở game lên toàn màn hình.")
print("3. Nhấn giữ phím ESC (hoặc F9) để DỪNG khẩn cấp.")
print("======================================================")

print("\nChuẩn bị chạy tiếp tục. Hãy chuyển sang màn hình game NGAY LẬP TỨC!")
for i in range(5, 0, -1):
    print(f"Bắt đầu sau {i} giây...")
    time.sleep(1)

print("\nĐang chạy...")

count = 0
# 7 hàng đầu tiên mỗi hàng 16 nút, hàng cuối cùng có 6 nút
cols_per_row_list = [16, 16, 16, 16, 16, 16, 16, 6]

for row in range(len(cols_per_row_list)):
    if row < START_ROW_INDEX:
        continue # Bỏ qua các hàng đã chụp
        
    y = START_Y + row * SPACING_Y
    
    for col in range(cols_per_row_list[row]):
        if row == START_ROW_INDEX and col < START_COL_INDEX:
            continue # Bỏ qua các cột đã chụp ở hàng hiện tại
            
        if keyboard.is_pressed('esc') or keyboard.is_pressed('f9'):
            print("Đã dừng chương trình!")
            exit()
            
        x = START_X + col * SPACING_X
        
        pydirectinput.moveTo(int(x), int(y))
        time.sleep(0.1) 
        pydirectinput.click()
        
        time.sleep(0.7)
        
        img = pyautogui.screenshot(region=CARD_REGION)
        
        count += 1
        # Lưu file với đúng hàng/cột tương ứng
        filename = os.path.join(SAVE_DIR, f"card_gold_row{row+1}_col{col+1}.png")
        img.save(filename)
        print(f"[{count}] Đã click ({x}, {y}) -> Đã lưu ảnh: {filename}")

print(f"HOÀN THÀNH! Đã chụp tiếp {count} ảnh thẻ vàng.")
