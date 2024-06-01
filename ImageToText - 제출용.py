import cv2
import pytesseract
import requests
import json
import openai
import os
import tkinter as tk
from tkinter import messagebox
import pyautogui
from PIL import Image
from PIL import ImageGrab  # ImageGrab 모듈 임포트
from tqdm import tqdm
import requests
import torch

class CaptureTool:
    def __init__(self, root):
        self.root = root
        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas = tk.Canvas(root, cursor="cross", bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        end_x, end_y = event.x, event.y
        self.capture_screen(self.start_x, self.start_y, end_x, end_y)
        self.root.quit()

    def capture_screen(self, start_x, start_y, end_x, end_y):
        self.root.withdraw()
        self.root.update_idletasks()  # 캡처 전에 모든 GUI 업데이트가 완료되도록 보장
        x1 = self.root.winfo_rootx() + min(start_x, end_x)
        y1 = self.root.winfo_rooty() + min(start_y, end_y)
        x2 = self.root.winfo_rootx() + max(start_x, end_x)
        y2 = self.root.winfo_rooty() + max(start_y, end_y)
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        screenshot.save("selected_screenshot.png")
        #print("선택한 영역이 캡처되었습니다. 'selected_screenshot.png' 파일을 확인하세요.")

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)  # 투명도 설정
    app = CaptureTool(root)
    root.mainloop()

# 다이얼로그 박스를 표시하는 함수
def show_message(message):
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우 숨기기
    messagebox.showinfo("Message", message)
    root.destroy()

# OpenAI API 키 설정
openai.api_key = "your_key"  # OpenAI API 키 입력

# Azure Translator API 설정
azure_endpoint = "https://api.cognitive.microsofttranslator.com/"
azure_key = "your_key"  # Azure Translator API 키 입력
location = "koreacentral"  # 리소스 위치 입력 (예: eastus)


# Tesseract 설치 경로 (Windows의 경우)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 이미지 읽기
image = cv2.imread('selected_screenshot.png')

# 이미지를 회색조로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 노이즈 제거를 위해 임계처리 적용
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# 이미지에서 텍스트 추출
text = pytesseract.image_to_string(gray, lang='eng') # 언어 설정: 영어 ('eng')

# 줄바꿈 처리: 연속된 줄바꿈을 하나로 줄이고 각 줄의 앞뒤 공백 제거
text = ' '.join(line.strip() for line in text.split('\n') if line.strip())

# Azure Translator API 호출 함수
def translate_azure(text, source_lang='en', target_lang='ko'):
    path = '/translate?api-version=3.0'
    params = f'&from={source_lang}&to={target_lang}'
    constructed_url = azure_endpoint + path + params
    
    headers = {
        'Ocp-Apim-Subscription-Key': azure_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json'
    }
    body = [{
        'text': text
    }]
    
    response = requests.post(constructed_url, headers=headers, json=body)
    
     # 응답 상태 코드 확인
    if response.status_code != 200:
        #print(f"Error: API request failed with status code {response.status_code}")
        #print(response.json())
        return None
    
    response_json = response.json()
    #print("API Response:")
    #print(json.dumps(response_json, indent=4, ensure_ascii=False))
    
    try:
        return response_json[0]['translations'][0]['text']
    except (KeyError, IndexError) as e:
        show_message(f"Error: Unexpected response structure: {e}")
        show_message(json.dumps(response_json, indent=4, ensure_ascii=False))
        return None


# 텍스트 번역 (Azure Translator)
translated_text = translate_azure(text)

#print(text)
#print("\nTranslated Text:")
if translated_text:
    # 마침표를 기준으로 줄바꿈 추가
    modified_text = translated_text.replace('.', '.\n')

    show_message(modified_text)

    text_to_save = modified_text

    # 텍스트 파일에 문자열 저장
    with open("translate.txt", "w", encoding="utf-8") as file:
        file.write(text_to_save)

    show_message("번역본이 텍스트 파일에 저장되었습니다.")

    #GPT-3.5 API 호출
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # 사용하고자 하는 모델 (예: gpt-3.5-turbo)
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content":modified_text}
            ],
            max_tokens=1000  # 응답의 최대 토큰 수 설정
        )
        
         # 응답 출력
        message = response.choices[0].message.content.strip()

        show_message(message)

        text_to_save = message

        # 텍스트 파일에 문자열 저장
        with open("Chat_response.txt", "w", encoding="utf-8") as file:
            file.write(text_to_save)

        show_message("Chat_GPT 답변이 텍스트 파일에 저장되었습니다.")

        
    except openai.OpenAIError as e:
        show_message(f"Error: {e}")
        show_message("현재 무료버전입니다. chat-gpt를 유료버전으로 업그레이드 해주세요")
    
else:
    show_message("Translation failed.")


