import nltk
from nltk.chat.util import Chat, reflections
import tkinter as tk
import pyttsx3
import random
from tkinter import scrolledtext
import threading  # Import threading

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Define the chatbot responses
pairs = [
    [r"hi|hello|hey|wassup",
     ["Hey there!", "Hello!", "Hi!", "Hey! What's up?", "Hi! How can I help you today?"]],

    [r"my name is (.*)",
     ["Nice to meet you, %1!", "Hey %1! What can I do for you?", "Hi %1! How's it going?"]],

    [r"(.*)how are you ?",
     ["I'm doing well, thanks for asking!", "I'm good, how about you?", "I'm fine, and you?", "Doing great! What's on your mind?"]],

    [r"(.*) your name?",
     ["I'm Iris.", "You can call me Iris.", "My name is Iris!"]],

    [r"(.*) your age?",
     ["I'm a chatbot, so I don't really have an age!", "Age is just a number, and I'm digital!", "I'm ageless, just here to assist!"]],

    [r"(.*) do for me?",
     ["I can answer questions, chat, or provide info!", "I'm here to help with questions, or just chat!", "I can assist with info and conversation!"]],

    [r"(.*) can you do?",
     ["I can chat, answer questions, and provide info!", "I'm good at answering questions and having conversations.", "I can help with information and a friendly chat!"]],

    [r"(.*) (love|like) you",
     ["Aww, that's sweet!", "That's very kind of you!", "I appreciate that!"]],

    [r"what is the weather like in (.*)",
     ["The weather in %1 is pleasant.", "The weather in %1 seems to be lovely today!", "It's sunny in %1"]],

    [r"tell me a joke",
     ["Why don't scientists trust atoms? Because they make up everything!", "What do you call a lazy kangaroo? Pouch potato!",
      "Why did the scarecrow win an award? Because he was outstanding in his field!"]],

    [r"what is your favorite color?",
     ["I'm an AI, so I don't have preferences, but I think the color blue is visually appealing!",
      "Colors are fascinating! I like the way different shades can evoke emotions."] ],

    [r"what is your purpose?",
     ["My purpose is to assist you with information and conversation.",
      "I'm here to help answer questions and provide a friendly chat experience."]],

    [r"who created you?",
     ["I was created by my developer.", "I was developed using Python and NLTK."]],

    [r"do you like sports?",
     ["Sports can be exciting! I find the strategies and teamwork involved in many sports fascinating.",
      "While I don't 'like' sports in a personal sense, I recognize their popularity and cultural significance."]],

    [r"tell me something interesting",
     ["Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
      "Here's a mind-blowing fact: The average person walks the equivalent of five times around the world in their lifetime!"]],

    [r"what are your hobbies?",
     ["As a chatbot, I don't have hobbies in the traditional sense, but I enjoy learning new things and engaging in conversations with people.",
      "I like processing information and providing helpful responses."]],

    [r"what is the meaning of life?",
     ["That's a big question! Philosophers have pondered that for centuries. From my perspective, the meaning of life is to learn, grow, and make a positive impact on the world around you.",
      "The meaning of life is a very personal thing. What brings meaning to your life?" ]],

    [r"can you help me with (.*)",
     ["I can definitely try to help you with %1! What specifically are you looking for?",
      "I'll do my best to assist you with %1. Tell me more about what you need."]],

    [r"how does the internet work?",
     ["The internet is a vast network of interconnected computers that communicate using a standard set of protocols. Information is transmitted in packets, and routers help to direct these packets to their destination.",
      "That's a complex topic! In simple terms, it's a network of connected computers sharing information."]],

    [r"what are some good movies?",
     ["That depends on what you like! Some popular and critically acclaimed movies include 'The Shawshank Redemption,' 'The Godfather,' and 'Pulp Fiction.'",
      "Do you have any preferences? Perhaps a genre, an actor, or director?" ]],

    [r"what is artificial intelligence?",
     ["Artificial intelligence is the ability of a computer or machine to mimic human cognitive functions such as learning and problem-solving.",
      "It's about making computers 'think' like humans!" ]],

    [r"tell me a fun fact",
     ["Here's a fun fact: A group of flamingos is called a flamboyance!", "Bananas are berries, but strawberries aren't."]],

     [r"thank you",
      ["You're welcome!", "No problem. Glad I could help!", "Anytime!"]],

    [r"(.*)",
     ["Hmm, I'm not quite sure about that.", "Could you rephrase that?", "I'm still learning, can you ask something else?",
      "Interesting question! Let me think...", "I'm not sure I have the answer to that right now.",
      "Let's talk about something else!"]]
]

# Create the chatbot
chatbot = Chat(pairs, reflections)
# Initialize pyttsx3
engine = pyttsx3.init()

# Set voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Index 1 for female voice


def speak(text):
    engine.say(text)
    engine.runAndWait()


# GUI setup
class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Iris")
        master.geometry("400x500")  # Increased size
        master.configure(bg="#2E2E2E")  # Dark background #2E2E2E

        # Chat history display (using ScrolledText for easier scrollbar management)
        self.chat_history = scrolledtext.ScrolledText(master, width=45, height=18, bg="#333333", fg="#FFFFFF",
                                                      wrap=tk.WORD, state=tk.DISABLED)  # Adjusted width and height
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # User input field
        self.user_input = tk.Entry(master, bg="#444444", fg="#FFFFFF", insertbackground="#FFFFFF") #444444
        self.user_input.pack(padx=10, pady=5, fill=tk.X)
        self.user_input.bind("<Return>", self.send_message)  # Bind Enter key

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message, bg="#555555", fg="#FFFFFF") #555555
        self.send_button.pack(pady=5)
        self.send_button.config(width=6)

        # Configure grid layout to make widgets responsive
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)


    def send_message(self, event=None):
        user_message = self.user_input.get().strip()
        if not user_message:
            return  # Ignore empty messages

        self.user_input.delete(0, tk.END)  # Clear the input field

        # Disable input while processing
        self.user_input.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

        # Start a thread to handle chatbot response and UI update
        threading.Thread(target=self.process_message, args=(user_message,)).start()

    def process_message(self, user_message):
        # Display user message
        self.display_message("You: " + user_message)

        # Get chatbot's response
        chatbot_response = chatbot.respond(user_message)

        if chatbot_response:
            self.display_message("Iris: " + chatbot_response)
            speak(chatbot_response)  # Speak the response
        else:
            response = random.choice(["I'm not quite sure about that.", "Let me think about that."])
            self.display_message("Iris: " + response)
            speak(response)  # Speak the response

        # Re-enable input after processing
        self.master.after(0, self.enable_input)

    def enable_input(self):
        self.user_input.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)

    def display_message(self, message):
        self.chat_history.config(state=tk.NORMAL)  # Make it editable
        self.chat_history.insert(tk.END, message + "\n")

        self.chat_history.config(state=tk.DISABLED)  # Make it read-only
        self.chat_history.yview(tk.END)  # Scroll to the end


# Main function to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()