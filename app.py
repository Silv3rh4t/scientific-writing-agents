import streamlit as st
from agent import SimpleChatAgent

with open("prompts/chat.txt") as f:
    system_prompt = f.read()

if "chat" not in st.session_state:
    st.session_state.chat = SimpleChatAgent(system_prompt)

st.set_page_config(page_title="SpectreBot", layout="wide")
st.title("SpectreBot (Nano)")

user_input = st.chat_input("Type here...")

if user_input:
    reply = st.session_state.chat.chat(user_input)
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(reply)

st.sidebar.markdown("### Working Draft / Structure")
st.sidebar.markdown(st.session_state.chat.sidebar or "_Nothing yet_")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Tokens used:** {st.session_state.chat.token_count}")
st.sidebar.markdown(f"**Estimated cost:** ${st.session_state.chat.cost_usd:.4f}")

if st.sidebar.button("💾 Save Session"):
    st.session_state.chat.export_session()
    st.sidebar.success("Session saved.")
