import streamlit as st
from typing import Generator, Optional, Dict, Union
from groq import Groq
import os

def _get_system_prompt() -> str:
    """Get system prompt from a file."""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "system_prompt.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

system_prompt = _get_system_prompt()
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

st.set_page_config(page_icon="📐", layout="wide", page_title="DigiDopps™")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

icon("🧬")
st.markdown('<a href="https://groqhealth.streamlit.app/" style="text-decoration:none; color: #ADD8E6;"><h2>Vers3Dynamics</h2></a>', unsafe_allow_html=True)
st.subheader("Meet Leonardo Da Vinci 🫀, Powered by Groq 🚀")

# Add a picture with a caption
st.image("images/Leonardo-legacy.png", caption="Buongiorno", width=200)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# Define model details
models = {
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
    "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

# Layout for model selection and max_tokens slider
col1, col2 = st.columns(2)

with col1:
    model_option = st.selectbox(
        "Connect with the perfect AI:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=2  # Default to LLaMA
    )

# Detect model change and clear chat history if model has changed
if st.session_state.selected_model != model_option:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]
    st.session_state.selected_model = model_option

max_tokens_range = models[model_option]["tokens"]

with col2:
    max_tokens = st.slider(
        "Max Tokens 🎨:",
        min_value=512,
        max_value=max_tokens_range,
        value=min(32768, max_tokens_range),
        step=512,
        help=f"Adjust the maximum number of tokens for the model's response. Max for selected model: {max_tokens_range}"
    )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = '🧬' if message["role"] == "assistant" else '🧑🏾‍💻'
    if message["role"] != "system":  # Do not display the system message
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if prompt := st.chat_input("Ciao", key="user_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='🧑🏾‍💻'):
        st.markdown(prompt)

    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=st.session_state.messages,
            max_tokens=max_tokens,
            stream=True
        )

        # Use the generator function with st.write_stream
        with st.chat_message("assistant", avatar="🧬"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(f"Oops! Something went wrong: {e}", icon="🐢🚨")

    # Append the full response to session_state.messages
    if isinstance(full_response, str):
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append({"role": "assistant", "content": combined_response})

# Add a video with custom size and loop
st.video("images/leo.mp4")
