import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, Radiobutton
from PIL import Image, ImageTk
import requests
from io import BytesIO

# API 伺服器 URL
API_BASE_URL = "http://35.238.154.158:5000"
#API_BASE_URL = "http://127.0.0.1:5000"


class Operation:
    def __init__(self):
        self.stock_number = None
        self.start_date = None
        self.end_date = None
        self.data = None
        self.selected_value = tk.IntVar(value=1)  

    def update_fields(self):
        self.stock_number = stock_entry.get().strip()
        self.start_date = start_date_entry.get().strip()
        self.end_date = end_date_entry.get().strip()


    def display_chart(self, image_path):
        try:
            image = Image.open(image_path)
            resized_image = image.resize((500,250))
            chart_image = ImageTk.PhotoImage(resized_image)
            chart_label.config(image=chart_image)
            chart_label.image = chart_image
            
        except Exception as e:
            messagebox.showerror("Error", f"無法顯示圖片：{e}")
    
    def display_strategy_chart(self, image_path):
        try:
            image = Image.open(image_path)
            resized_image = image.resize((700,210))
            chart_image = ImageTk.PhotoImage(resized_image)
            strategy_chart_label.config(image=chart_image)
            strategy_chart_label.image = chart_image
            
        except Exception as e:
            messagebox.showerror("Error", f"無法顯示圖片：{e}")


    def submit_form(self):
        self.update_fields()
        if self.stock_number and self.start_date and self.end_date:
            try:
                response = requests.post(
                    f'{API_BASE_URL}/api/analyze_data',
                    json={'stock': self.stock_number, 'start': self.start_date, 'end': self.end_date}
                )
                response.raise_for_status()
                self.data = response.json()
                
                if 'images' in self.data:
                    for widget in button_frame.winfo_children():
                        widget.destroy()  
                    Radiobutton(button_frame, text='Closing Prices History', variable=self.selected_value, value=1, command=self.update_image).pack(anchor=tk.W)
                    Radiobutton(button_frame, text='KD History', variable=self.selected_value, value=2, command=self.update_image).pack(anchor=tk.W)
                    Radiobutton(button_frame, text='MACD History', variable=self.selected_value, value=3, command=self.update_image).pack(anchor=tk.W)
                    Radiobutton(button_frame, text='RSI History', variable=self.selected_value, value=4, command=self.update_image).pack(anchor=tk.W)

                    self.update_image()
                messagebox.showinfo("Success", "分析完成，請選擇左側圖片顯示！")
            except Exception as e:
                messagebox.showerror("Error", f"請求失敗：{e}")
        else:
            messagebox.showwarning("Input Error", "請填寫所有欄位！")

    def update_image(self):
        selected_option = self.selected_value.get()
        self.show_images(selected_option)    
    
    def show_images(self, i):
        try:
            if 'images' in self.data:
                image_path = self.data['images'][i-1]
                image_response = requests.post(
                    f'{API_BASE_URL}/api/show_images',
                    json={"image_path": image_path}
                )
                image_response.raise_for_status()
                image_content = BytesIO(image_response.content)

                self.display_chart(image_content) 
        except Exception as e:
                messagebox.showerror("Error", f"請求失敗：{e}")
   
    
    def strategy_comparison(self):
        self.update_fields()
        if self.stock_number and self.start_date and self.end_date and self.data:
            try:
                if 'images' in self.data:
                    image_path = self.data['images'][-1]
                    image_response_strategy = requests.post(
                        f'{API_BASE_URL}/api/show_images',
                        json={"image_path": image_path}
                    )
                    image_response_strategy.raise_for_status()
                    image_content = BytesIO(image_response_strategy.content)
                    print(image_content)
                    
                    self.display_strategy_chart(image_content)  
            except Exception as e:
                messagebox.showerror("Error", f"請求失敗：{e}")
        else:
            messagebox.showwarning("Input Error", "請輸入股票編號、起始時間和結束時間並查詢才能進行策略比較！")


    def gpt_response(self):
        self.update_fields()
        if self.stock_number and self.start_date and self.end_date and self.data:
            
            user_question = gpt_entry.get().strip()
            if not user_question:
                messagebox.showwarning("Input Error", "請輸入您的問題！")
                return
        
            try:
                response = requests.post(
                f'{API_BASE_URL}/api/send_to_gpt',
                json={'image_paths': [i for i in self.data['images']], "question": user_question}
                )
                response.raise_for_status()
                data = response.json()
                gpt_reply_text.delete(1.0, tk.END)  # 清空之前的內容
                gpt_reply_text.insert(tk.END, data.get('gpt_reply', 'AI 顧問無法提供回答'))
            except Exception as e:
                messagebox.showerror("Error", f"請求失敗：{e}")
        else:
            messagebox.showwarning("Input Error", "請輸入股票編號、起始時間和結束時間並查詢才能進行AI諮詢！")

    def download_excel(self):
        self.update_fields()
        if self.stock_number and self.start_date and self.end_date and self.data:
            try:
                excel_path = self.data.get('excel_path')
                if excel_path:
                    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel Files", "*.xlsx")])
                    if file_path:
                        response = requests.get(f'{API_BASE_URL}/api/download_excel', params={'file_path': excel_path})
                        response.raise_for_status()
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                        messagebox.showinfo("Success", "分析報告已成功下載！")
            except Exception as e:
                messagebox.showerror("Error", f"請求失敗：{e}")
        else:
            messagebox.showwarning("Input Error", "請輸入股票編號、起始時間和結束時間並查詢才能下載分析報告！")

# GUI 介面設定
root = tk.Tk()
root.title("股票分析與AI諮詢應用程式")
width = root.winfo_screenwidth()
height = root.winfo_screenwidth()
root.geometry(f"{width}x{height}+0+0")

header_label = tk.Label(root, text="股票分析與AI諮詢應用程式", font=("標楷體", 20))
header_label.pack(pady=10)

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

stock_label = tk.Label(form_frame, text="股票編號：")
stock_label.grid(row=0, column=0, padx=5)

stock_entry = tk.Entry(form_frame)
stock_entry.grid(row=0, column=1, padx=5)

start_date_label = tk.Label(form_frame, text="起始日期：")
start_date_label.grid(row=1, column=0, padx=5)

start_date_entry = tk.Entry(form_frame)
start_date_entry.grid(row=1, column=1, padx=5)

end_date_label = tk.Label(form_frame, text="結束日期：")
end_date_label.grid(row=2, column=0, padx=5)

end_date_entry = tk.Entry(form_frame)
end_date_entry.grid(row=2, column=1, padx=5)

op = Operation()

submit_button = tk.Button(form_frame, text="開始查詢", command=op.submit_form)
submit_button.grid(row=3, column=0, columnspan=3, pady=10)

content_frame = tk.Frame(root)
content_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

image_frame = tk.LabelFrame(content_frame, text="分析類型", width=400, height=250)
image_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)

button_frame = tk.Frame(image_frame)
button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

chart_frame = tk.Frame(image_frame)
chart_frame.pack(side=tk.RIGHT, expand=False, fill=tk.BOTH, padx=5, pady=5)

chart_label = tk.Label(image_frame)  
chart_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

ai_frame = tk.LabelFrame(content_frame, text="AI 顧問區", width=400, height=250)
ai_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)

gpt_label = tk.Label(ai_frame, text="請輸入您的問題：")
gpt_label.pack(pady=5)

gpt_entry = tk.Entry(ai_frame, width=50)
gpt_entry.pack(pady=5)

gpt_button = tk.Button(ai_frame, text="發送問題至AI顧問", command=op.gpt_response)
gpt_button.pack(pady=5)

gpt_reply_label = tk.Label(ai_frame, text="（AI顧問回應將顯示在此處）")
gpt_reply_label.pack(pady=10)
gpt_reply_label.destroy()  # 刪除原有的 gpt_reply_label
gpt_reply_text = scrolledtext.ScrolledText(ai_frame, width=70, height=10, wrap=tk.WORD)
gpt_reply_text.pack(pady=10)

strategy_frame = tk.Frame(root)
strategy_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
strategy_button = tk.Button(root, text="進行策略比較", command=op.strategy_comparison)
strategy_button.pack(pady=10)
strategy_chart_label = tk.Label(strategy_frame)
strategy_chart_label.pack()

excel_button = tk.Button(root, text="下載分析結果", command=op.download_excel)
excel_button.pack(pady=10)

root.mainloop()