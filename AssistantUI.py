import customtkinter as ctk
from model import Assistant

class AssistantUI(object):
    def __init__(self):
        self.assistant = Assistant()
        
    def create_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Chat Assistant")
        self.root.geometry("900x700")

        #rigla stanga pentru parametrii
        self.left_frame = ctk.CTkFrame(self.root, width=250)
        self.left_frame.pack(side="left", fill='y')

        self.create_parameters_controls()

        #interfata dreapta pentru chat 
        self.right_frame = ctk.CTkFrame(self.root)
        self.right_frame.pack(side='right', expand=True, fill='both')

        self.create_chat_interface()

        self.root.mainloop()

    def create_parameters_controls(self):
        ctk.CTkLabel(self.left_frame, text='Numele Modelului: Gpt-2', font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(self.left_frame, text='Parametrii Modelului', font=("Arial", 18, "bold")).pack(pady=10)

        self.max_new_tokens = self.create_slider('Numarul maxim de token-uri', 50, 300, 70)
        self.num_return_sequences = self.create_slider("Numarul de propozitii", 1, 5, 3)
        self.top_k = self.create_slider("Top K", 0, 100, 50)
        self.top_p = self.create_slider("Top P (gradul de randomizare)", 0.0, 1.0, 0.30, 0.01)
        self.temperature = self.create_slider("Temperatura", 0.1, 1.5, 0.4, 0.1)

    def create_slider(self, label_text, min_value, max_value, default_value, step=1):
        ctk.CTkLabel(self.left_frame, text=label_text).pack(pady=5)
        slider = ctk.CTkSlider(self.left_frame, from_=min_value, to=max_value, number_of_steps=int((max_value - min_value) / step))
        slider.set(default_value)
        slider.pack(pady=5)
        return slider

    def create_chat_interface(self):
        self.chat_display = ctk.CTkTextbox(self.right_frame, height=20, width=60)
        self.chat_display.pack(pady=10, padx= 10, fill='both', expand=True)

        self.input_frame = ctk.CTkFrame(self.right_frame)
        self.input_frame.pack(fill='x')

        self.chat_input = ctk.CTkEntry(self.input_frame, placeholder_text='Scrie intrebarea aici...')
        self.chat_input.pack(side='left', fill='x', expand='True', padx=10)

        self.send_button = ctk.CTkButton(self.input_frame, text='Send', command=self.send_message)
        self.send_button.pack(side='right', padx=10)

    def send_message(self):
        user_input = self.chat_input.get()
        if user_input:
            max_new_tokens = int(self.max_new_tokens.get())
            num_return_sequences = int(self.num_return_sequences.get())
            top_k = int(self.top_k.get())
            top_p = self.top_p.get()
            temperature = self.temperature.get()
            
            self.chat_display.insert('end', f"Eu: {user_input}\n")
            response = self.assistant.chat_with_assistant(
                user_input,
                max_new_tokens=max_new_tokens,
                num_return_sequences=num_return_sequences,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature)

            self.chat_display.insert("end", f"Asistent: {response}\n\n")
            self.chat_input.delete(0,'end')
    




