import streamlit as st
import requests
import json

# --- პარამეტრები ---
API_KEY = "AIzaSyCelk4Hij2vXuwJgbNDwrv1BVmk1kDqBo8"
# პირდაპირი ბმული სტაბილურ v1 ვერსიაზე - აქ შეცდომა გამორიცხულია
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="Gemo AI Stable", page_icon="🤖")

# სტილი მობილურისთვის
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTextInput>div>div>input { border-radius: 25px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Gemo AI")
st.caption("პირდაპირი კავშირი Gemini-სთან (v1)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ჩატის ისტორია
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# მომხმარებლის შეყვანა
if prompt := st.chat_input("ჰკითხე რამე Gemo-ს..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ვამზადებთ მონაცემებს Google-ისთვის გაგზავნამდე
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            headers = {'Content-Type': 'application/json'}
            
            # ვაგზავნით პირდაპირ მოთხოვნას
            response = requests.post(URL, headers=headers, data=json.dumps(payload))
            response_data = response.json()
            
            # პასუხის ამოღება JSON-იდან
            if 'candidates' in response_data:
                full_response = response_data['candidates'][0]['content']['parts'][0]['text']
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Google-მა პასუხი ვერ დააბრუნა. ნახეთ დეტალები.")
                st.json(response_data) # ეს გვაჩვენებს თუ რატომ არ იმუშავა

        except Exception as e:
            st.error(f"კავშირის შეცდომა: {str(e)}")
