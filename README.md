# 🤖 AI Vision Self-Chatbot

An AI-powered study assistant that can understand **text, questions, study images, screenshots, diagrams, textbook pages, and handwritten notes**. The chatbot uses Gemini Vision and conversational AI to provide simple, beginner-friendly explanations and supports follow-up questions.

## 🌟 Features

* 💬 AI-powered conversational chatbot
* 🖼️ Upload and analyze study images
* 👁️ Vision-based understanding using Gemini
* 📖 Explain questions, notes, diagrams, and screenshots
* 🔄 Support for follow-up questions using conversation context
* 📝 Generate a short study summary
* 📧 Send the generated summary to email
* 👤 User name and email input
* 🗑️ Clear conversation history
* ☁️ Deployable using Streamlit Community Cloud

## 🧠 How It Works

The application follows this workflow:

```text
User Input
    ↓
Text Question / Study Image
    ↓
Gemini AI + Vision
    ↓
AI Explanation
    ↓
Follow-up Questions
    ↓
Study Summary
    ↓
Email Summary
```

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **Google Gemini API**
* **Gemini Vision**
* **Gmail SMTP**
* **Git & GitHub**
* **Streamlit Community Cloud**

## 📂 Project Structure

```text
AI-Vision-Self-Chatbot/
│
├── app.py
├── prompts.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml.example
```

## 📄 File Description

### `app.py`

Contains the main Streamlit application.

It handles:

* User interface
* Chat interaction
* Image upload
* Gemini API communication
* Conversation history
* Summary generation
* Email sending

### `prompts.py`

Contains the custom AI system prompt and welcome message.

The prompt instructs the AI to:

* Explain concepts in simple language
* Understand uploaded images
* Read clear text from images
* Explain content step by step
* Remember conversation context
* Avoid guessing when image content is unclear

### `requirements.txt`

Contains the Python packages required to run the project.

### `.streamlit/secrets.toml.example`

Provides an example of the required API keys and email configuration without exposing private credentials.

## 🔐 Environment Variables / Secrets

The application requires the following secrets:

```toml
GEMINI_API_KEY = "your-gemini-api-key"

GMAIL_ADDRESS = "your-gmail-address@gmail.com"

GMAIL_APP_PASSWORD = "your-gmail-app-password"
```

For local development, create:

```text
.streamlit/secrets.toml
```

**Do not upload the real `secrets.toml` file to GitHub.**

The `.gitignore` file is configured to prevent it from being committed.

## 🚀 Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/priyamvada2006/AI-Vision-Self-Chatbot.git
```

### 2. Open the project folder

```bash
cd AI-Vision-Self-Chatbot
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

On Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure secrets

Create:

```text
.streamlit/secrets.toml
```

Add your Gemini API key and Gmail App Password.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📧 Email Feature

The application uses Gmail SMTP to send the generated study summary to the user's email.

For security, a **Gmail App Password** should be used instead of the normal Gmail account password.

## ☁️ Deployment

The application can be deployed using **Streamlit Community Cloud**.

Deployment requires:

1. A GitHub repository
2. `app.py`
3. `requirements.txt`
4. Streamlit secrets configured in the deployment settings

## 🎯 Project Objective

The objective of this project is to create an interactive AI study assistant that combines **conversational AI and image understanding** to help students learn from different types of study material.

Instead of only answering text-based questions, the chatbot can also process visual learning material and provide explanations in simple language.

## 💡 Future Enhancements

Possible future improvements include:

* 🎤 Voice-based questions
* 📚 PDF and document analysis
* 🧮 Better mathematical problem solving
* 💻 Programming code explanation
* 📝 Quiz generation from uploaded material
* 📊 Personalized learning progress
* 🌐 Multi-language explanations

## 👩‍💻 Author

**Kankanala Priyamvada**

B.Tech Computer Science Engineering Student

Vignan's Institute of Management and Technology for Women

## 📌 Project

**AI Vision Self-Chatbot**

Built using Python, Streamlit, and Google Gemini AI.
