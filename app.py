import streamlit as st
from agents.chat_agent import ChatAgent

st.set_page_config(page_title="SpectreBot", layout="wide")

if "chat" not in st.session_state:
    st.session_state.chat = ChatAgent()

st.title("SpectreBot: Opinion Assistant")

# Sidebar: Show current structure and evidence
structure = st.session_state.chat.structure
if structure:
    st.sidebar.markdown("## Current Structure")
    for point in structure["points"]:
        st.sidebar.markdown(f"- {point}")
        ev = structure["evidence"].get(point, {})
        if ev:
            st.sidebar.markdown(f"  - **{ev.get('title')}**")
            st.sidebar.markdown(f"    [{ev.get('link')}]({ev.get('link')})")
            st.sidebar.caption(ev.get("description"))

# Chat Input
user_input = st.chat_input("Share your thoughts or give instructions")

if user_input:
    reply = st.session_state.chat.handle(user_input)
    st.markdown(f"**You:** {user_input}")
    st.markdown(f"**SpectreBot:** {reply}")
