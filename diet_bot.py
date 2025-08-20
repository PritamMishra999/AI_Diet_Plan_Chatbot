import streamlit as st
import requests
import os
from dotenv import load_dotenv
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Diet Chatbot", layout="centered")
st.title("🥗 AI Diet Plan Chatbot")
st.markdown("Chat with an AI to get your **personalized diet plan!**")

MODEL = "mistralai/mistral-7b-instruct"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}
openrouter_url = "https://openrouter.ai/api/v1/chat/completions"

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": (
                "You are a certified nutritionist and diet-focused chatbot. "
                "Only answer questions related to food, nutrition, dietary preferences, allergies, meal planning, and diet-related goals. "
                "Do NOT answer questions unrelated to diet, such as fitness, mental health, or general wellness. "
                "If a user asks an unrelated question, politely respond that you only provide help with diet and nutrition."
            )
        },
        {
            "role": "assistant",
            "content": (
                "Hi! 👋 I'm your personal AI dietitian. "
                "To begin, could you tell me your age, gender, height, weight, dietary preferences or restrictions, and your goal (like weight loss, muscle gain, etc)?"
            )
        }
    ]

# ---------------- DISPLAY CHAT HISTORY ----------------
for msg in st.session_state.chat_history[1:]:  # skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Type here...")

if user_input:
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to OpenRouter
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            payload = {
                "model": MODEL,
                "messages": st.session_state.chat_history
            }
            response = requests.post(openrouter_url, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                ai_reply = result["choices"][0]["message"]["content"]
            else:
                error_details = response.json()
                ai_reply = f"❌ API Error {response.status_code}: {error_details.get('error', {}).get('message', 'Unknown error')}"

            st.markdown(ai_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🤖 Powered by Mistral-7B via OpenRouter | Built with ❤️ using Streamlit")
