import os
import pandas as pd
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load API key from environment or fallback to default
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter endpoint for chat completion
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_ai_to_structure(text):
    """
    Send unstructured bank statement text to OpenRouter for AI-assisted parsing
    into a structured JSON array of transactions.

    Each transaction should include:
    - date: ISO 8601 string (e.g., "2025-07-09")
    - description: transaction description
    - amount: positive (credit) or negative (debit)
    - balance: account balance after the transaction

    Parameters:
    - text (str): Raw bank statement text extracted from PDF

    Returns:
    - pd.DataFrame: A DataFrame containing structured transaction data

    Raises:
    - Exception: If OpenRouter API call fails or returns invalid format
    """

    # Prompt instructing the AI to format output in strict JSON
    prompt = f"""
    You are a data extraction assistant. From the following raw bank statement
    text, extract a structured JSON array of transactions.

    Each transaction must have:
    - date (ISO 8601 format)
    - description
    - amount (positive for credit, negative for debit)
    - balance

    Respond only with the array.

    TEXT:
    {text}
        """.strip()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "BankStatementExtractor"
    }

    data = {
        "model": "tngtech/deepseek-r1t2-chimera:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=data)

    # If request failed or invalid response
    if response.status_code != 200:
        try:
            error = response.json()
        except Exception:
            error = response.text
        raise Exception(f"OpenRouter API Error: {error}")

    # Extract JSON from response text
    content = response.json()['choices'][0]['message']['content']

    try:
        return pd.read_json(content)
    except Exception as e:
        raise ValueError(f"Failed to convert AI response to DataFrame: {e}")
