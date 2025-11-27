import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
import datetime
from agent.tools import resume_analysis_tool
from agent.agent_builder import generate_answer

load_dotenv()

st.set_page_config(page_title="AI Career Coach", layout="wide")
st.title("🌟 AI Career Transition & Skill-Building Coach")
st.write("Your personal AI mentor for career change, skill-building & job readiness.")


st.sidebar.header("Actions")

mode = st.sidebar.radio(
    "Choose mode:",
    ["Chat (text)", "Resume Analyzer"],
    index=0,
    key="mode_select"
)

st.sidebar.markdown("---")


st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("processing", False)

def add_message(role, text):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chat_history.append({"role": role, "text": text, "time": ts})

def export_chat():
    msg = []
    for m in st.session_state.chat_history:
        who = "You" if m["role"] == "user" else "AI"
        msg.append(f"[{m['time']}] {who}: {m['text']}")
    return "\n\n".join(msg)


st.sidebar.subheader("Chat history")
if st.sidebar.button("Clear chat history"):
    st.session_state.chat_history = []
    st.sidebar.success("Chat cleared.")

st.sidebar.download_button(
    "Download chat (txt)",
    export_chat(),
    file_name="chat_history.txt",
    mime="text/plain"
)


st.markdown("""
<style>
.bubble {
    padding: 14px 18px; 
    border-radius: 18px; 
    margin: 8px 0;
    max-width: 80%;
    display: inline-block;
}
.user {
    background: #e0f2ff;
    float: right;
    border-bottom-right-radius: 4px;
}
.ai {
    background: #e6f7ea;
    float: left;
    border-bottom-left-radius: 4px;
}
.meta {
    font-size: 12px;
    color: #666;
}
.clearfix { clear: both; }
</style>
""", unsafe_allow_html=True)


if mode == "Chat (text)":
    st.subheader("Ask your career question")

    
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message...")
        submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        add_message("user", user_input.strip())

        with st.spinner("Thinking..."):
            try:
                prompt = (
                    "You are a career coach. Be concise and actionable.\n\n"
                    f"User: {user_input}\n\nResponse:"
                )
                ai_reply = generate_answer(prompt)
            except Exception as e:
                ai_reply = f"[Error] {e}"

        add_message("assistant", ai_reply)

    
    for msg in st.session_state.chat_history:
        role = msg["role"]
        bubble_class = "user" if role == "user" else "ai"
        align = "right" if role == "user" else "left"

        st.markdown(f"""
        <div style="text-align:{align}" class="meta">{msg['time']}</div>
        <div class="bubble {bubble_class}" style="float:{align}">
            {msg['text']}
        </div>
        <div class="clearfix"></div>
        """, unsafe_allow_html=True)


elif mode == "Resume Analyzer":
    st.subheader("Resume Analyzer")
    st.write("Upload a resume image (png/jpg).")

    uploaded = st.file_uploader("Upload resume", type=["png", "jpg", "jpeg"])

    if uploaded:
        st.image(uploaded, width=400)

        save_dir = Path("data/uploads")
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / uploaded.name
        save_path.write_bytes(uploaded.getbuffer())

        if st.button("Analyze Resume"):
            with st.spinner("Analyzing..."):
                try:
                    result = resume_analysis_tool(str(save_path))
                    st.success(result)
                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown("---")
