
import streamlit as st
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from gtts import gTTS
import numpy as np
from PIL import Image
import io
import re
from datetime import datetime

# --- გვერდის კონფიგურაცია ---
st.set_page_config(page_title="Gemo AI Mobile", page_icon="🤖")

# --- სტილი (CSS) აპლიკაციის იერისთვის ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #7FFFD4; color: black; }
    .gemo-text { font-size: 20px; font-weight: bold; text-align: center; }
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

# --- Gemo-ს ლოგიკა ---
def gemo_logic(input_text):
    lang = detect_language(input_text)
    text = input_text.lower()
    
    if "გამარჯობა" in text or "hello" in text:
        return ("გამარჯობა! მე გემო ვარ, შენი ასისტენტი.", "Hello! I am Gemo, your assistant.")[lang=='en'], "😊"
    elif "დრო" in text or "time" in text:
        now = datetime.now().strftime("%H:%M")
        return f"ახლა არის {now}" if lang=='ka' else f"It is {now}", "🕒"
    return ("ვერ გავიგე, სცადე სხვა რამ.", "I didn't understand, try something else.")[lang=='en'], "🤔"

# --- ინტერფეისი ---
st.title("🤖 Gemo AI")

# Gemo-ს სტატუსი/სახე
status_placeholder = st.empty()
status_placeholder.markdown("<div class='gemo-text'>👋 გამარჯობა, მე გემო ვარ!</div>", unsafe_allow_html=True)

# ჩატის ფუნქცია
user_input = st.text_input("მიწერე Gemo-ს:", placeholder="გამარჯობა / Hello")
if st.button("კითხვა"):
    if user_input:
        res, emoji = gemo_logic(user_input)
        st.write(f"{emoji} **Gemo:** {res}")
        audio_fp = speak(res, detect_language(res))
        st.audio(audio_fp, format='audio/mp3')

st.divider()

# მხედველობის ფუნქცია (Object Detection)
st.subheader("🖼️ მხედველობა")
uploaded_file = st.file_uploader("ატვირთე სურათი ან გადაიღე ფოტო", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # სურათის დამუშავება
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    
    with st.spinner('Gemo აანალიზებს...'):
        # ობიექტების ამოცნობა
        bbox, label, conf = cv.detect_common_objects(opencv_image)
        output_image = draw_bbox(opencv_image, bbox, label, conf)
        
        # RGB-ში გადაყვანა Streamlit-ისთვის
        output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
        
        st.image(output_image, caption="Gemo-ს დანახული სამყარო", use_column_width=True)
        
        # შედეგის თქმა
        objects = ", ".join(list(set(label)))
        if objects:
            msg = f"მე აქ ვხედავ: {objects}" if detect_language(objects) == 'ka' else f"I see here: {objects}"
            st.success(msg)
            st.audio(speak(msg, detect_language(msg)), format='audio/mp3')
        else:
            st.warning("ვერაფერი ამოვიცანი.")
