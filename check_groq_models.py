#!/usr/bin/env python3
"""Check available Groq models."""

from groq import Groq
from src.roleradar.config import config

try:
    client = Groq(api_key=config.GROQ_API_KEY)
    models = client.models.list()

    print("Available Groq Models:")
    print("=" * 80)
    for model in models.data:
        print(f"  {model.id}")
    print("=" * 80)
except Exception as e:
    print(f"Error: {e}")
