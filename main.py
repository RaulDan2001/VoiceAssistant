import customtkinter as ctk
from AssistantUI import AssistantUI
from stt import SpeechLogic

root = ctk.CTk()
root.title("Welcome to ClosedAI")
root.geometry('640*480')

def stttts_runtime():
    speech = SpeechLogic()
    speech.speech_run()

def assistant_runtime():
    asist = AssistantUI()
    asist.create_ui()

def makewindow():
    root = ctk.CTk()
    root.title("Welcome")
    root.geometry('640*480')

    buttonassistant = ctk.CTkButton(root, text='Assistant', command=assistant_runtime)
    buttonassistant.pack()

    buttonsstts = ctk.CTkButton(root, text='STT and TTS', command=stttts_runtime)
    buttonsstts.pack()

    root.mainloop()

# Rulez aplicația
def main():
    makewindow()

if __name__ == "__main__":
    main()






