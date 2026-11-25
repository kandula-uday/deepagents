import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-6-luna", use_responses_api=True)
strong_model = init_chat_model("openai:gpt-6.1-sol", use_responses_api=True)
