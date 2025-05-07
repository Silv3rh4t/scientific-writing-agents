import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from agents.structure import StructureAgent
from agents.searcher import SearcherAgent

st.set_page_config(page_title="Political Science Research Assistant", layout="wide")

# --- Session Initialization ---
if "chat" not in st.session_state:
    st.session_state.chat = []

if "agent" not in st.session_state:
    st.session_state.agent = StructureAgent()

if "points" not in st.session_state:
    st.session_state.points = []

if "evidence" not in st.session_state:
    st.session_state.evidence = {}

if "initialized" not in st.session_state:
    st.session_state.initialized = False

st.title("Political Science Research Assistant")

# --- Sidebar: Real-Time Structure + Evidence ---
st.sidebar.title("📌 Live Outline")

if st.session_state.points:
    for pt in st.session_state.points:
        st.sidebar.markdown(f"**• {pt}**")
        ev = st.session_state.evidence.get(pt, [])
        for e in ev:
            st.sidebar.markdown(f"  - [📄 {e['title']}]({e['url']})")

# --- Chat Submission ---
if prompt := st.chat_input("Type your thoughts or continue the conversation..."):
    st.session_state.chat.append(("🧍 You", prompt))

    # First input → structure + init
    if not st.session_state.initialized:
        response, points = st.session_state.agent.start(prompt)
        st.session_state.points = points
        st.session_state.chat.append(("🤖 Agent", response))
        st.session_state.initialized = True

        # Background: fetch evidence
        searcher = SearcherAgent()
        for pt in points:
            st.session_state.evidence[pt] = searcher.run(pt)

    # Later: continue refining structure
    else:
        response, points = st.session_state.agent.chat(prompt)
        st.session_state.points = points
        st.session_state.chat.append(("🤖 Agent", response))

        # Update evidence as needed
        searcher = SearcherAgent()
        for pt in points:
            if pt not in st.session_state.evidence:
                st.session_state.evidence[pt] = searcher.run(pt)

# --- Chat History Display ---
for sender, msg in st.session_state.chat:
    with st.chat_message("user" if "You" in sender else "assistant"):
        st.markdown(msg)

# --- Reset Button ---
if st.sidebar.button("🔄 Reset All"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
