import os
import re
import json
import pandas as pd
import requests
from django.conf import settings

# Load API key from Django settings or environment
OPENROUTER_API_KEY = getattr(settings, "OPENROUTER_API_KEY", None)
OPENROUTER_URL = getattr(settings, "OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")


def ask_ai_to_structure(text):
    """
    Send unstructured bank statement text to OpenRouter for AI-assisted parsing
    into a structured JSON array of transactions.

    Each transaction should include:
    - date: ISO 8601 string (e.g., "2025-07-09")
    - description: transaction description
    - amount: positive (credit) or negative (debit)
    - balance: account balance after the transaction
    - transaction_type: credit or debit
    - channel: e.g., POS, TRANSFER, USSD, ATM
    - counterparty: if available

    Parameters:
    - text (str): Raw bank statement text extracted from PDF

    Returns:
    - pd.DataFrame: A DataFrame containing structured transaction data

    Raises:
    - Exception: If OpenRouter API call fails or returns invalid format
    """
    if not OPENROUTER_API_KEY:
        raise Exception("OpenRouter API key not set in settings.")

    prompt = f"""
Extract the bank statement table from the following text. Each row must contain:
- date
- amount
- balance
- description (narration)
- transaction_type (credit/debit)
- channel (POS, TRANSFER, USSD, CASH, ATM, etc.)
- counterparty (if available)

Return only a **valid JSON array of objects** — no explanation, no markdown, no headings.

Bank statement text:
{text}
""".strip()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "BankStatementExtractor"
    }

    payload = {
        "model": "tngtech/deepseek-r1t2-chimera:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)

    if response.status_code != 200:
        try:
            error = response.json()
        except Exception:
            error = response.text
        raise Exception(f"OpenRouter API Error: {error}")

    try:
        content = response.json()['choices'][0]['message']['content']
        # Extract only the JSON array from the content
        match = re.search(r"\[\s*{.*?}\s*\]", content, re.DOTALL)
        if not match:
            raise ValueError("No JSON array found in AI response.")

        json_data = match.group(0)
        data = json.loads(json_data)
        return pd.DataFrame(data)

    except Exception as e:
        raise ValueError(f"Failed to convert AI response to DataFrame: {e}")
