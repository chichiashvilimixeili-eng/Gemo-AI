import streamlit as st
from duckduckgo_search import DDGS

st.set_page_config(page_title="Gemo AI v3", page_icon="🌐")
st.title("🌐 Gemo AI: ინტერნეტ-ასისტენტი")
st.caption("ეს ვერსია მუშაობს ყოველგვარი API გასაღებების გარეშე!")

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
            with DDGS() as ddgs:
                # Gemo ეძებს პასუხს ინტერნეტში ქართულ ენაზე
                search_results = list(ddgs.text(prompt, region='ka-ge', max_results=3))
                
                if search_results:
                    # ვაერთიანებთ ნაპოვნ ინფორმაციას
                    response = "აი რა ვიპოვე შენთვის:\n\n"
                    for res in search_results:
                        response += f"🔹 {res['body']}\n\n"
                else:
                    response = "სამწუხაროდ, ამ თემაზე ინფორმაცია ვერ მოვიძიე."
                
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"ხარვეზი ძიებისას: {e}")
