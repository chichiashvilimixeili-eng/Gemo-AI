import streamlit as st
import google.generativeai as genai
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from gtts import gTTS
import numpy as np
import io
import re

# 
# --- Gemini კონფიგურაცია ---
GEMINI_API_KEY = "AIzaSyCelk4Hij2vXuwJgbNDwrv1BVmk1kDqBo8"
genai.configure(api_key=GEMINI_API_KEY)

# შეცვლილია gemini-pro-ზე სტაბილურობისთვის
model = genai.GenerativeModel('gemini-pro') 

# --- გვერდის კონფიგურაცია ---
st.set_page_config(page_title="Gemo AI Mobile", page_icon="🤖")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #7FFFD4; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- ფუნქციები ---
def detect_language(text):
    return 'ka' if re.search('[ა-ჰ]', text) else 'en'

def speak(text, lang):
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp

# --- მთავარი ინტერფეისი ---
st.title("🤖 Gemo AI (Powered by Gemini)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ჩატის ისტორიის ჩვენება
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# მომხმარებლის შეყვანა
if prompt := st.chat_input("ჰკითხე რამე Gemo-ს..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Gemo ფიქრობს..."):
            try:
                # Gemini-ს პასუხის გენერაცია
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
                
                # ხმოვანი პასუხი
                lang = detect_language(full_response)
                audio_fp = speak(full_response[:200], lang) # ვზღუდავთ ხმას დიდ ტექსტზე
                st.audio(audio_fp, format='audio/mp3')
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"შეცდომაა: {e}")

st.divider()

# მხედველობის ფუნქცია
st.subheader("🖼️ მხედველობა")
uploaded_file = st.file_uploader("ატვირთე ფოტო", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    bbox, label, conf = cv.detect_common_objects(img)
    output_image = draw_bbox(img, bbox, label, conf)
    output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
    
    st.image(output_image, use_column_width=True)
    
    if label:
        found_text = f"ვხედავ შემდეგ ობიექტებს: {', '.join(set(label))}"
        st.success(found_text)
        st.audio(speak(found_text, 'ka'), format='audio/mp3')
