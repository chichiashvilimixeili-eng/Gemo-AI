import streamlit as st
import google.generativeai as genai

# კონფიგურაცია
GEMINI_API_KEY = "AIzaSyCelk4Hij2vXuwJgbNDwrv1BVmk1kDqBo8"
genai.configure(api_key=GEMINI_API_KEY, transport='rest')

# მოდელის იძულებითი შერჩევა v1 სტანდარტით
model = genai.GenerativeModel('gemini-1.5-flash')

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
            # მოთხოვნა v1 ვერსიის გამოყენებით
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"კავშირის პრობლემა: {str(e)}")
