import streamlit as st
import requests
import json

# --- კონფიგურაცია ---
API_KEY = "AIzaSyCelk4Hij2vXuwJgbNDwrv1BVmk1kDqBo8"
# პირდაპირი ბმული v1 სტაბილურ ვერსიაზე
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="Gemo AI", page_icon="🤖")
st.title("🤖 Gemo AI (Stable Mode)")

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
            # პირდაპირი HTTP მოთხოვნა ბიბლიოთეკის გარეშე
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(URL, headers=headers, data=json.dumps(payload))
            res_json = response.json()
            
            # პასუხის ამოღება
            answer = res_json['candidates'][0]['content']['parts'][0]['text']
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"შეცდომა: {str(e)}")
            st.write("დეტალები:", res_json) # დაგვეხმარება გარკვევაში
