import streamlit as st
import json
from agent import SpectreAgent

st.set_page_config(page_title="Writing Assistant", layout="wide")
st.title("Writing Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = SpectreAgent()
    st.session_state.display_history = []

agent = st.session_state.chat
user_input = st.chat_input("What are you thinking about?")

# Display stored messages
for role, msg in st.session_state.display_history:
    st.chat_message(role).write(msg)

# Handle new input
if user_input:
    result = agent.chat(user_input)

    # Save to display history only
    st.session_state.display_history.append(("user", user_input))
    st.session_state.display_history.append(("assistant", result["chat"]))

    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(result["chat"])

# Sidebar article
st.sidebar.markdown("### 📄 Draft in Progress")
if agent.article:
    for i in sorted(agent.article.keys(), key=lambda x: int(x)):
        st.sidebar.markdown(f"**{i}.** {agent.article[i]}")
else:
    st.sidebar.info("Nothing yet. Start by sharing your ideas.")

# Stats
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Tokens In:** {agent.token_in}")
st.sidebar.markdown(f"**Tokens Out:** {agent.token_out}")
st.sidebar.markdown(f"**Estimated Cost:** ${agent._estimate_cost():.4f}")

if st.sidebar.button("💾 Save Session"):
    agent.export_session()
    st.sidebar.success("Session saved.")

