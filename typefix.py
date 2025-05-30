import keyboard
import pyautogui
import win32api,win32con,win32gui,win32process,win32clipboard
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw, ImageFont
import threading
import sys,os,datetime,time
#------------------------日誌------------------------------
# 找到使用者的文件資料夾
documents_path = os.path.join(os.environ['USERPROFILE'], 'Documents')
log_dir = os.path.join(documents_path, 'TypeFixLogs')
# 建立資料夾 如果不存在
os.makedirs(log_dir, exist_ok=True)
LOG_FILE = os.path.join(log_dir, 'conversion_log.txt')
MAX_LOG_LINES = 200 
def log(text):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > MAX_LOG_LINES:
            lines = lines[-MAX_LOG_LINES:]  # 保留最後幾行
        lines.append(f"{datetime.datetime.now()} - {text}\n")
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)
    else:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()} - {text}\n")
def show_log():
    if os.path.exists(LOG_FILE):
        os.startfile(LOG_FILE)
    else:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("（目前沒有日誌）")
        os.startfile(LOG_FILE)
#------------------------圖標------------------------------
def create_image():
    image = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(image)
    # 讀取字型（Windows 系統內建的字型路徑）
    font_path = "C:/Windows/Fonts/msjh.ttc"  # 微軟正黑體
    font_size = 60
    font = ImageFont.truetype(font_path, font_size)
    text = "轉"
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    position = ((64 - w) / 2, ((64-h)/2)-15)
    draw.text(position, text, fill='white', font=font)
    return image
def setup_tray():
    icon = pystray.Icon("輸入法修正工具")
    icon.icon = create_image()
    icon.menu = pystray.Menu(
        item('顯示日誌', lambda: show_log()),
        item('退出', quit_program)
    )
    icon.run()
#------------------------背景執行------------------------------
def listen_hotkey():
    keyboard.add_hotkey('ctrl+b', hotkey)
    keyboard.wait()
def quit_program(icon, item):# 退出程序
    icon.stop()
    os._exit(0)
#------------------------主程式--------------------------------
def copy_selected_text():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.05)
def get_current_input_method():
    hwnd = win32gui.GetForegroundWindow()
    thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
    layout_id = win32api.GetKeyboardLayout(thread_id)
    return layout_id
def switch_input_method():
    hwnd = win32gui.GetForegroundWindow()
    #win32api.SendMessage(hwnd, win32con.WM_INPUTLANGCHANGEREQUEST, 0, 0x0409)  # 切换到英文输入法
    win32api.SendMessage(hwnd, win32con.WM_INPUTLANGCHANGEREQUEST, 0, 0x0804)  # 切换到中文输入法
def get_clipboard_text():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData()
    except TypeError:
        data = ''
    win32clipboard.CloseClipboard()
    return data
def convert_text_to_keypress(text):
    for char in text:
        pyautogui.keyDown(char)
        pyautogui.keyUp(char)
def convert_wrong_input_to_correct_chinese():
    text = get_clipboard_text()
    if not text:
        print("剪貼簿內容為空或無效")
        log("剪貼簿內容為空或無效,執行失敗")
        return
    print(f"原始剪貼簿內容：{text}")
    log(f"原始剪貼簿內容：{text}")
    current_input_method = get_current_input_method()
    if current_input_method != 0xE0060804:  
        switch_input_method()  # 切换输入法
        time.sleep(0.1)
    convert_text_to_keypress(text)
    log("執行成功")
def hotkey():
    print("嘗試轉換錯誤輸入為中文...")
    copy_selected_text()
    convert_wrong_input_to_correct_chinese()
    
if __name__ == "__main__":
    print("程式已在背景啟動，選取錯字並按 Ctrl+b")
    threading.Thread(target=listen_hotkey, daemon=True).start()
    setup_tray()
