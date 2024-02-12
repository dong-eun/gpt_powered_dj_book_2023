import openai
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("apiKey")

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
    message_log=[
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    def show_popup_message(window, message):
        popup=tk.Toplevel(window)
        popup.title("")
        
        # 팝업 창의 내용
        label=tk.Label(popup, text=message, font=("맑은 고딕", 12))
        label.pack(expand=True, fill=tk.BOTH)
        
        # 팝업 창의 크기 조절하기
        window.update_idletasks()
        popup_width=label.winfo_reqwidth() + 20
        popup_height=label.winfo_reqheight() + 20
        popup.geometry(f"{popup_width}x{popup_height}")
        
        # 팝업 창의 중앙에 위치하기
        window_x=window.winfo_x()
        window_y=window.winfo_y()
        window_width=window.winfo_width()
        window_height=window.winfo_height()

        popup_x=window_x + window_width // 2 - popup_width // 2
        popup_y=window_y + window_height // 2 - popup_height // 2
        popup.geometry(f"+{popup_x}+{popup_y}")
        
        popup.transient(window)
        popup.attributes('-topmost', True)
        
        popup.update()
        return popup

    def on_send():
        user_input=user_entry.get()
        user_entry.delete(0, tk.END)
        
        if user_input.lower() == "quit":
            window.destroy()
            return
    
        message_log.append({"role": "user", "content": user_input})
        thinking_popup=show_popup_message(window, "생각 중...")
        window.update_idletasks() 
        # '생각 중...' 팝업 창이 반드시 화면에 나타나도록 강제로 설정하기
        response=send_message(message_log)
        thinking_popup.destroy()

        message_log.append({"role": "assistant", "content": response})
        conversation.config(state=tk.NORMAL) 
        # conversation을 수정할 수 있게 설정하기
        conversation.insert(tk.END, f"You: {user_input}\n", "user")
        # 태그를 추가한 부분(1)
        conversation.insert(tk.END, f"AI assistant: {response}\n", "assistant")
        conversation.config(state=tk.DISABLED) 
        # conversation을 수정하지 못하게 설정하기
        conversation.see(tk.END)

    window=tk.Tk()
    window.title("AI Assistant")

    font=("맑은 고딕", 10)
    
    conversation=scrolledtext.ScrolledText(window, wrap=tk.WORD, bg='#f0f0f0', font=font)
    # width, height를 없애고 배경색 지정하기(2)
    conversation.tag_configure("user", background="#c9daf8")
    # 태그별로 다르게 배경색 지정하기(3)
    conversation.tag_configure("assistant", background="#e4e4e4")
    # 태그별로 다르게 배경색 지정하기(3)
    conversation.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    # 창의 폭에 맞추어 크기 조정하기(4)

    input_frame=tk.Frame(window) # user_entry와 send_button을 담는 frame(5)
    input_frame.pack(fill=tk.X, padx=10, pady=10) # 창의 크기에 맞추어 조절하기(5)
    
    user_entry=tk.Entry(input_frame)
    user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
    
    send_button=tk.Button(input_frame, text="Send", command=on_send)
    send_button.pack(side=tk.RIGHT)
    
    window.bind('<Return>', lambda event: on_send())
    window.mainloop()

if __name__ == "__main__":
    main()