import os

import openai
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key=os.getenv("apiKey")

# 대화 로그를 OpenAI API에 전송하고 응답을 받아오는 함수입니다.
def send_message(message_log):
    # OpenAI의 ChatCompletion API를 사용하여 메시지를 생성합니다.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 사용할 모델을 지정합니다.
        messages=message_log,    # 대화 로그를 API에 전달합니다.
        temperature=0.5,         # 생성된 텍스트의 다양성을 조절하는 매개변수입니다.
    )

    # API 응답에서 생성된 선택지들을 반복합니다.
    for choice in response.choices:
        # 선택지에 "text"가 있으면 해당 텍스트를 반환합니다.
        if "text" in choice:
            return choice.text

    # 선택지에 "text"가 없는 경우, 첫 번째 선택지의 메시지 내용을 반환합니다.
    return response.choices[0].message.content

def main():
    # 초기 대화 로그 설정
    message_log = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    def on_send():
        # 사용자가 입력한 내용 가져오기
        user_input = user_entry.get()
        user_entry.delete(0, tk.END)  # 입력 필드 초기화

        # 사용자가 "quit"을 입력하면 창 종료
        if user_input.lower() == "quit":
            window.destroy()
            return

        # 사용자 입력을 대화 로그에 추가
        message_log.append({"role": "user", "content": user_input})

        # OpenAI API를 사용하여 응답 받아오기
        response = send_message(message_log)

        # 대화 로그에 AI 응답 추가
        message_log.append({"role": "assistant", "content": response})

        # 대화 화면에 사용자 입력과 AI 응답 추가
        conversation.insert(tk.END, f"You: {user_input}\n")
        conversation.insert(tk.END, f"AI assistant: {response}\n")
        conversation.see(tk.END)  # 스크롤을 맨 아래로 이동

    # Tkinter 창 생성
    window = tk.Tk()
    window.title("AI Assistant")

    # ScrolledText 위젯을 사용하여 대화 로그 표시
    conversation = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20)
    conversation.grid(row=0, column=0, padx=10, pady=10)

    # Entry 위젯을 사용하여 사용자 입력 받기
    user_entry = tk.Entry(window)
    user_entry.grid(row=1, column=0, padx=10, pady=10)

    # "Send" 버튼을 클릭하면 on_send 함수 호출
    send_button = tk.Button(window, text="Send", command=on_send)
    send_button.grid(row=1, column=1, padx=10, pady=10)

    # Return 키를 누르면 on_send 함수 호출
    window.bind('<Return>', lambda event: on_send())

    # Tkinter 메인 루프 실행
    window.mainloop()

if __name__ == "__main__":
    main()
