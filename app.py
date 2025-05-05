import streamlit as st
st.set_page_config(page_title="AI Political Research Agent", layout="wide")
from dotenv import load_dotenv
load_dotenv()

from agents.validator import ValidatorAgent
from agents.searcher import SearcherAgent
from agents.reviewer import ReviewerAgent
from agents.drafter import DrafterAgent
from agents.critic import CriticAgent

# ---- Set page config ----


# ---- Session init ----
if "step" not in st.session_state:
    st.session_state.step = "validator"

st.title("🧠 AI Political Research Assistant")

# ---- User inputs ----
with st.sidebar:
    st.header("📝 Article Inputs")
    scope = st.text_area("Scope", st.session_state.get("scope", ""), height=100)
    premise = st.text_area("Premise", st.session_state.get("premise", ""), height=100)
    hypothesis = st.text_area("Hypothesis", st.session_state.get("hypothesis", ""), height=100)

    if st.button("Save Inputs"):
        st.session_state.scope = scope
        st.session_state.premise = premise
        st.session_state.hypothesis = hypothesis
        st.success("Inputs saved.")

# ---- Validator Step ----
if st.session_state.step == "validator":
    st.header("🔎 Step 1: Validate Premise and Hypothesis")

    if st.button("Run Validator"):
        agent = ValidatorAgent()
        st.session_state.validated = agent.run(scope, premise, hypothesis)

    if "validated" in st.session_state:
        st.subheader("✅ Validator Output")
        st.write(st.session_state.validated)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Proceed to Literature Search"):
                st.session_state.step = "searcher"
        with col2:
            if st.button("Re-run Validator"):
                del st.session_state.validated

# ---- Searcher Step ----
elif st.session_state.step == "searcher":
    st.header("🔍 Step 2: Literature & Evidence Search")

    if st.button("Run Searcher"):
        agent = SearcherAgent()
        st.session_state.papers = agent.run(hypothesis)

    if "papers" in st.session_state:
        st.subheader("📚 Search Results")
        st.text_area("Edit search output (optional):", value=st.session_state.papers, key="edited_papers", height=300)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Proceed to Review"):
                st.session_state.step = "reviewer"
        with col2:
            if st.button("Re-run Search"):
                del st.session_state.papers

# ---- Reviewer Step ----
elif st.session_state.step == "reviewer":
    st.header("🧵 Step 3: Thematic Literature Review")

    if st.button("Run Reviewer"):
        agent = ReviewerAgent()
        st.session_state.reviewed = agent.run(st.session_state.edited_papers)

    if "reviewed" in st.session_state:
        st.subheader("📖 Literature Review Output")
        st.text_area("Edit review summary (optional):", value=st.session_state.reviewed, key="edited_review", height=400)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Proceed to Drafting"):
                st.session_state.step = "drafter"
        with col2:
            if st.button("Re-run Reviewer"):
                del st.session_state.reviewed

# ---- Drafter Step ----
elif st.session_state.step == "drafter":
    st.header("✍️ Step 4: Draft Article")

    if st.button("Run Drafter"):
        agent = DrafterAgent()
        st.session_state.draft = agent.run(scope, hypothesis, st.session_state.edited_review)

    if "draft" in st.session_state:
        st.subheader("📝 Draft Output")
        st.text_area("Edit draft (optional):", value=st.session_state.draft, key="edited_draft", height=600)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Proceed to Critique"):
                st.session_state.step = "critic"
        with col2:
            if st.button("Re-run Drafter"):
                del st.session_state.draft

# ---- Critic Step ----
elif st.session_state.step == "critic":
    st.header("🧐 Step 5: Critique and Feedback")

    if st.button("Run Critic"):
        agent = CriticAgent()
        st.session_state.critique = agent.run(st.session_state.edited_draft)

    if "critique" in st.session_state:
        st.subheader("📋 Critique")
        st.markdown(st.session_state.critique)

        st.success("✅ Done. You can now export, edit, or re-run any stage above.")
