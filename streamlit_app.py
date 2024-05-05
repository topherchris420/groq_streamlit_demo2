import streamlit as st
from typing import Generator
from groq import Groq
import openai
import claude

st.set_page_config(page_icon="💡", layout="wide", page_title="Vers3Dynamics")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("🦙")
st.write(f'[Vers3Dynamics](https://mitpress.vercel.app)', unsafe_allow_html=True)
st.subheader("Virtual Assistants, Powered by Groq, ChatGPT, and Claude", divider="rainbow", anchor=False)

# Initialize Groq client
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialize Claude client
claude_client = claude.Client(api_key=st.secrets["CLAUDE_API_KEY"])

# Layout for model selection and max_tokens slider
col1, col2 = st.columns(2)

# Define model details
models = {
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
    "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
    "claude": {"name": "Claude", "tokens": 4096, "developer": "Vers3Dynamics"},
    "chatgpt": {"name": "ChatGPT", "tokens": 2048, "developer": "OpenAI"},
}

with col1:
    model_option = st.selectbox(
        "Connect with the perfect AI:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=0  # Default to Gemma-7b-it
    )

# Detect model change and clear chat history if model has changed
if "selected_model" not in st.session_state or st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

max_tokens_range = models[model_option]["tokens"]

with col2:
    max_tokens = st.slider(
        "Max Tokens🪙:",
        min_value=512,  # Minimum value to allow some flexibility
        max_value=max_tokens_range,
        value=min(8192, max_tokens_range),  # Default value
        step=512,
        help=f"Adjust the maximum number of 🪙 (words) for the model's response. Max for selected model🚀: {max_tokens_range}"
    )

def generate_chat_responses(response) -> Generator[str, None, None]:
    """Yield chat response content."""
    yield response.text

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar='👨🏾‍💻'):
        st.markdown(prompt)

    try:
        if model_option in ["gemma-7b-it", "llama2-70b-4096", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"]:
            # Groq API call
            chat_completion_groq = groq_client.chat.completions.create(
                model=model_option,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                max_tokens=max_tokens,
                stream=True
            )

            with st.chat_message("assistant", avatar="😎"):
                chat_responses_generator_groq = generate_chat_responses(chat_completion_groq)
                st.write_stream(chat_responses_generator_groq)

        elif model_option == "claude":
            # Claude API call
            response_claude = claude_client.get_response(prompt)

            with st.chat_message("assistant", avatar="🐾"):
                st.write(response_claude.text)

        elif model_option == "chatgpt":
            # ChatGPT API call
            response_chatgpt = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=max_tokens
            )

            with st.chat_message("assistant", avatar="🤖"):
                st.write(response_chatgpt.choices[0].text.strip())

    except Exception as e:
        st.error(e, icon="🚨🐢")
