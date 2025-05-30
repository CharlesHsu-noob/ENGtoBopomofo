Inspired by https://www.threads.com/@henning_0908/post/DKEmYZZz_cL?sort_order=recent&hl=zh-tw

open 'run_typefix_.vbs',change the path to which your 'typefix.py' is in

put the vbs file in C:\Users\"your user name"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

the log file will be in C:\Users\"your user name"\Documents\typefix\

TypeFix – 輸入法修正工具
TypeFix 是一個針對中文輸入錯誤（如切錯成英文模式）的修正工具。只需選取錯字並按下 `Ctrl + B`，程式會自動切換輸入法並輸出正確的中文。
快捷鍵修正（Ctrl + B）
有托盤圖示、背景常駐
日誌記錄轉換結果
可設定開機自動啟動

安裝方式
1. 安裝 Python（建議版本 3.10+）
2. 安裝依賴：
pip install pyautogui keyboard pystray pillow pywin32
3. 執行 `typefix.py` 即可開始使用

設定開機自動啟動
1. 打開'run_typefix_.vbs'，把路徑改成你放'typefix.py'的地方(e.g. C:\Users\username\Desktop\all\code\python\ENGtoBopomofo\typefix.py)
2. 按win+r 輸入 shell:startup 把.vbs丟到裡面

使用方式
1. 啟動程式後會在右下角系統托盤顯示圖示「轉」
2. 使用時遇到輸入錯誤的注音英文（如 "su3cl3" 本想輸「你好」）
3. 選取錯誤文字，切換到注音輸入法，按下 `Ctrl + B`
4. 程式會在光標位置輸出你剛剛打的中文
5. 右鍵點擊圖標可以開啟日誌

日誌位置
轉換記錄會儲存在：C:\Users\"your user name"\Documents\typefix\

ps:整個只有主程式是我寫的，生成log檔還有背景執行，圖標是chatgpt寫的


