import os
from groq import Groq
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 2. History for Memory
if "chat_history" not in globals():
    chat_history = []

print("\n" + "="*40)
print("⚡ GROQ AI AGENT STARTED (Super Fast)")
print("Type 'exit' to stop")
print("="*40)

while True:
    user_input = input("\nYou: ").strip()
    
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("AI: Goodbye!")
        break
    
    if not user_input:
        continue

    try:
        # Chat messages with System Instruction
        messages = [
            {"role": "system", "content": "You are a professional AI. Respond ONLY in English language."},
            *chat_history,
            {"role": "user", "content": user_input}
        ]

        # Request to Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
        )

        response_text = completion.choices[0].message.content
        print(f"\nAI: {response_text}")

        # Save to history for memory
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response_text})

    except Exception as e:
        print(f"\n[Error]: {e}")