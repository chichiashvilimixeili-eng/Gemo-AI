import streamlit as st
import google.generativeai as genai
from google.generativeai import client

# --- Gemini-ს იძულებითი სტაბილური კონფიგურაცია ---
GEMINI_API_KEY = "AIzaSyCelk4Hij2vXuwJgbNDwrv1BVmk1kDqBo8"

# ჩვენ ხელით ვუთითებთ 'v1' ვერსიას, რომ v1beta-ს პრობლემა მოვხსნათ
client.DEFAULT_API_VERSION = 'v1' 
genai.configure(api_key=GEMINI_API_KEY, transport='rest')

# ვიყენებთ მოდელის სრულ და ზუსტ სახელს
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- ინტერფეისი და ლოგიკა ---
st.title("🤖 Gemo AI (Powered by Gemini)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ჰკითხე რამე Gemo-ს..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # აქ ხდება პასუხის გამოთხოვა
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # თუ მაინც შეცდომაა, ვცდილობთ ალტერნატიულ გზას
            st.error(f"შეცდომა: {str(e)}")
            st.info("სცადეთ გვერდის გადატვირთვა (Refresh)")
