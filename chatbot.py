import tkinter as tk

try:
    from google import genai
except ImportError:
    genai = None

# ==========================
# GEMINI API KEY
# ==========================
API_KEY = "AQ.Ab8RN6IzCTZyHXYNqLEpP63ISjdjUzh69htLOIB4JS2s7hck6w"  # Put your Gemini API key here

client = None
if API_KEY and genai:
    try:
        client = genai.Client(api_key=API_KEY)
    except:
        client = None

# ==========================
# SYSTEM PROMPT
# ==========================
SYSTEM_PROMPT = """
You are HealthBot, a professional healthcare assistant.

Rules:
- Answer health-related questions politely.
- Provide general health information only.
- Do not prescribe medication.
- For serious symptoms advise consulting a doctor.
- Keep responses short and easy to understand.
"""

# ==========================
# DISEASE DATABASE
# ==========================
DISEASES = {
    "fever": "Fever is usually caused by infection. Drink plenty of fluids and get adequate rest.",
    "cold": "A common cold may cause sneezing, cough, and a runny nose.",
    "headache": "Headaches can result from stress, dehydration, lack of sleep, or illness.",
    "dengue": "Dengue symptoms include high fever, severe headache, muscle pain, and rash.",
    "diabetes": "Diabetes affects blood sugar levels and requires proper monitoring.",
    "asthma": "Asthma can cause wheezing, coughing, and breathing difficulties.",
    "malaria": "Malaria often causes fever, chills, sweating, and fatigue.",
    "typhoid": "Typhoid may cause prolonged fever, weakness, and stomach pain.",
    "covid": "COVID-19 symptoms may include fever, cough, sore throat, and fatigue.",
    "hypertension": "High blood pressure often has no symptoms but requires monitoring.",
    "anemia": "Anemia can cause tiredness, weakness, and dizziness.",
    "migraine": "Migraine often causes severe headaches and sensitivity to light.",
    "arthritis": "Arthritis causes joint pain, stiffness, and swelling.",
    "tuberculosis": "Tuberculosis may cause persistent cough, fever, and weight loss.",
    "pneumonia": "Pneumonia is a lung infection that may cause fever and breathing problems.",
    "cholera": "Cholera can cause severe diarrhea and dehydration.",
    "hepatitis": "Hepatitis is an inflammation of the liver.",
    "kidney stone": "Kidney stones may cause severe pain and difficulty urinating.",
    "heart disease": "Heart disease affects the heart and blood vessels.",
    "allergy": "Allergies may cause sneezing, itching, or skin rashes."
}

# ==========================
# MAIN WINDOW
# ==========================
root = tk.Tk()
root.title("💙 HealthBot")
root.geometry("850x700")
root.configure(bg="#25D366")

# ==========================
# HEADER
# ==========================
header = tk.Frame(root, bg="#128C7E", height=80)
header.pack(fill="x")

title = tk.Label(
    header,
    text="💙 HealthBot",
    font=("Arial", 22, "bold"),
    bg="#128C7E",
    fg="white"
)
title.pack(pady=20)

# ==========================
# CHAT AREA
# ==========================
chat_container = tk.Frame(root, bg="#ECE5DD")
chat_container.pack(fill="both", expand=True)

canvas = tk.Canvas(
    chat_container,
    bg="#ECE5DD",
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    chat_container,
    orient="vertical",
    command=canvas.yview
)

messages_frame = tk.Frame(canvas, bg="#ECE5DD")

messages_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window(
    (0, 0),
    window=messages_frame,
    anchor="nw"
)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ==========================
# MESSAGE BUBBLES
# ==========================
def add_message(message, sender):

    frame = tk.Frame(messages_frame, bg="#ECE5DD")

    if sender == "user":
        frame.pack(fill="x", padx=10, pady=5)

        bubble = tk.Label(
            frame,
            text=message,
            bg="#DCF8C6",
            fg="black",
            font=("Segoe UI", 11),
            wraplength=500,
            justify="left",
            padx=12,
            pady=8
        )
        bubble.pack(anchor="e")

    else:
        frame.pack(fill="x", padx=10, pady=5)

        bubble = tk.Label(
            frame,
            text=message,
            bg="white",
            fg="black",
            font=("Segoe UI", 11),
            wraplength=500,
            justify="left",
            padx=12,
            pady=8
        )
        bubble.pack(anchor="w")

    root.update_idletasks()
    canvas.yview_moveto(1.0)

# ==========================
# BOT RESPONSE
# ==========================
def get_bot_response(user_message):

    for disease, answer in DISEASES.items():
        if disease in user_message.lower():
            return answer

    if client:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
            )
            return response.text
        except Exception as e:
            return f"Error: {e}"

    return "Please enter a health-related question."

# ==========================
# SEND MESSAGE
# ==========================
def send_message():

    user_message = entry.get().strip()

    if not user_message:
        return

    add_message(user_message, "user")

    entry.delete(0, tk.END)

    bot_reply = get_bot_response(user_message)

    add_message(bot_reply, "bot")

# ==========================
# ENTER KEY
# ==========================
def enter_pressed(event):
    send_message()

# ==========================
# WELCOME MESSAGE
# ==========================
add_message(
    "👋 Welcome to HealthBot!\n\nI am your personal health assistant.\nHow can I help you today?",
    "bot"
)

# ==========================
# INPUT AREA
# ==========================
bottom_frame = tk.Frame(root, bg="#ECE5DD")
bottom_frame.pack(fill="x")

entry = tk.Entry(
    bottom_frame,
    font=("Segoe UI", 12)
)

entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=10,
    pady=10,
    ipady=8
)

entry.bind("<Return>", enter_pressed)

send_button = tk.Button(
    bottom_frame,
    text="➤",
    font=("Arial", 14, "bold"),
    bg="#128C7E",
    fg="white",
    command=send_message
)

send_button.pack(
    side="right",
    padx=10,
    pady=10
)

root.mainloop()
