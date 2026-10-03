import streamlit as st
from google import genai
from google.genai import types
import smtplib
from email.mime.text import MIMEText
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE

st.title("🤖 AI Vision Self-Chatbot")

st.info(WELCOME_MESSAGE)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    if "summary" in st.session_state:
        del st.session_state.summary
    st.rerun()

st.subheader("👤 Your Details")

name = st.text_input("👤 Enter your name:")

st.subheader("💬 Ask Your Question") 

question = st.text_input("Ask me anything:")

email = st.text_input("📧 Enter your email:")

st.subheader("🖼️ Upload Study Image")

uploaded_image = st.file_uploader(
    "🖼️ Upload a study image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image")

for i, message in enumerate(st.session_state.chat_history):
    if i % 2 == 0:
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)

if question:
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
            "Gemini is temporarily busy. Please try again in a few seconds."
        )

if st.button("📝 Generate Summary"):
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
            "Gemini quota is currently exhausted. "
            "Please try again after the quota resets."
        )

if "summary" in st.session_state:
    st.subheader("📝 Study Summary")
    st.write(st.session_state.summary)

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

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(
                    st.secrets["GMAIL_ADDRESS"],
                    st.secrets["GMAIL_APP_PASSWORD"]
                )

                server.send_message(msg)

            st.success("✅ Summary sent successfully to your email!")