import streamlit as st

st.set_page_config(
    page_title="AI Vision Self-Chatbot",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .feature-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

from google import genai
from google.genai import types
import smtplib
from email.mime.text import MIMEText
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE

st.markdown(
    '<div class="main-title">AI Vision Self-Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your intelligent study assistant for text, images, and interactive learning.</div>',
    unsafe_allow_html=True
)

st.info(WELCOME_MESSAGE)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Clear Conversation", use_container_width=True):
    st.session_state.chat_history = []
    if "summary" in st.session_state:
        del st.session_state.summary
    st.rerun()


# =========================
# YOUR DETAILS
# =========================

st.markdown(
    '<div class="section-title">👤 Your Details</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "Your Name",
        placeholder="Enter your name"
    )

with col2:
    email = st.text_input(
        "📧 Email Address",
        placeholder="Enter your email to receive study summaries"
    )


# =========================
# ASK YOUR QUESTION
# =========================

st.markdown(
    '<div class="section-title">💬 Ask Your Question</div>',
    unsafe_allow_html=True
)

question = st.text_area(
    "Your Question",
    placeholder="Ask anything about your studies...",
    height=100
)


# =========================
# UPLOAD IMAGE
# =========================

st.markdown(
    '<div class="section-title">🖼️ Upload Study Image</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<p>Upload a textbook page, diagram, handwritten note, screenshot, or study image.</p>',
    unsafe_allow_html=True
)

uploaded_image = st.file_uploader(
    "Choose a study image",
    type=["jpg", "jpeg", "png"],
    help="Supported formats: JPG, JPEG and PNG"
)

if uploaded_image:
    st.success("✅ Image uploaded successfully!")

    st.image(
        uploaded_image,
        caption="Your Study Image",
        width=500
    )

# =========================
# CONVERSATION
# =========================

if st.session_state.chat_history:
    st.markdown(
        '<div class="section-title">💬 Conversation</div>',
        unsafe_allow_html=True
    )

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.chat_message("user").write(message)
        else:
            st.chat_message("assistant").write(message)


# =========================
# ASK AI
# =========================

if st.button("Ask AI", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question before asking AI.")

    else:
        contents = [SYSTEM_PROMPT]

        for message in st.session_state.chat_history:
            contents.append(message)

        if uploaded_image:
            image_bytes = uploaded_image.getvalue()

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=uploaded_image.type
                )
            )

        contents.append(question)

        try:
            with st.spinner("AI is analyzing your question..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=contents
                )

            st.session_state.chat_history.append(question)
            st.session_state.chat_history.append(response.text)

            st.chat_message("user").write(question)
            st.chat_message("assistant").write(response.text)

        except Exception:
            st.error(
                "Gemini API quota is temporarily exhausted. "
                "Please try again after the quota resets."
            )


# =========================
# GENERATE SUMMARY
# =========================

if st.session_state.chat_history and st.button(
    "Generate Summary",
    type="secondary",
    use_container_width=True
):
    summary_prompt = """
Create a short study summary from our conversation.

Include:
- Main topic
- Important points
- Key concepts
- Important code or examples if present

Use simple beginner-friendly language.
Keep the summary concise.
"""

    try:
        summary_response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=summary_prompt + "\n" + "\n".join(
                st.session_state.chat_history
            )
        )

        st.session_state.summary = summary_response.text

    except Exception:
        st.error(
            "Gemini API quota is temporarily exhausted. "
            "Please try again after the quota resets."
        )


# =========================
# STUDY SUMMARY + EMAIL
# =========================

if "summary" in st.session_state:
    st.markdown(
        '<div class="section-title">📝 Study Summary</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="feature-card">
            {st.session_state.summary}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("📧 Send Summary to Email"):
        if not email:
            st.warning("Please enter your email address first.")
        else:
            msg = MIMEText(
                f"Hello {name},\n\n"
                f"Here is your AI Study Assistant summary:\n\n"
                f"{st.session_state.summary}\n\n"
                f"Thank you for using AI Vision Self-Chatbot!"
            )

            msg["Subject"] = "AI Study Assistant - Study Summary"
            msg["From"] = st.secrets["GMAIL_ADDRESS"]
            msg["To"] = email

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(
                        st.secrets["GMAIL_ADDRESS"],
                        st.secrets["GMAIL_APP_PASSWORD"]
                    )

                    server.send_message(msg)

                st.success("✅ Summary sent successfully to your email!")

            except Exception:
                st.error(
                    "❌ Unable to send the email. "
                    "Please check your email address or Gmail settings."
                )