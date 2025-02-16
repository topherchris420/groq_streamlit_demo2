# Quantum Supercomputing & Teleportation Explorer🐶

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://woodyard.streamlit.app/)


This [Streamlit](https://woodyard.streamlit.app/) app integrates with [Vers3Dynamics](https://vers3dynamics.io/) to provide an engaging interface where users can interact with quantum experiments.

It is blazing FUN; try it and see! 🏎️ 💨 💨 💨

## Features

- **Dynamic Response Generation**: Utilizes a generator function to stream responses from the Groq API, providing a seamless chat experience.
- **Error Handling**: Implements try-except blocks to handle potential errors gracefully during API calls.

## Requirements

- Streamlit
- Groq Python SDK
- Python 3.7+

## Setup and Installation

- **Install Dependencies**:

  ```bash
  pip install streamlit groq
  ```

- **Set Up Groq API Key**:

  Ensure you have an API key from Groq. This key should be stored securely using Streamlit's secrets management:

  ```toml
  # .streamlit/secrets.toml
  GROQ_API_KEY="your_api_key_here"
  ```

- **Run the App**:
  Navigate to the app's directory and run:

```bash
streamlit run streamlit_app.py
```

## Usage

Upon launching the app, you are greeted with the experiment. Just have fun.

## Contributing

Contributions are welcome to enhance the app, fix bugs, or improve documentation.

Please feel free to fork the repository, make changes, and submit a pull request.
