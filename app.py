import streamlit as st
from huggingface_hub import InferenceClient

# --- ახალი "ტვინის" კონფიგურაცია ---
# ვიყენებთ Mistral-ს, რომელიც სტაბილურია და ყოველთვის პასუხობს
client = InferenceClient(api_key="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") # დროებითი გასაღები

st.set_page_config(page_title="Gemo AI v2", page_icon="🚀")
st.title("🚀 Gemo AI: ახალი ერა")
st.info("Gemo ახლა Hugging Face-ის ძრავზე მუშაობს!")

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
            # Gemo აგენერირებს პასუხს
            response = ""
            for message in client.chat_completion(
                model="mistralai/Mistral-7B-Instruct-v0.3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                stream=True,
            ):
                token = message.choices[0].delta.content
                response += token

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"ოპერაცია ვერ შესრულდა: {e}")
