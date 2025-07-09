import pdfplumber
from decimal import Decimal


def extract_text_from_pdf(file_path):
    """
    Extract all text content from a PDF file using pdfplumber.

    Parameters:
    - file_path (str): Path to the PDF file.

    Returns:
    - str: A single string containing the concatenated text from all pages.
           Returns an empty string for pages without extractable text.
    """
    with pdfplumber.open(file_path) as pdf:
        return "\n".join([
            page.extract_text() or ""
            for page in pdf.pages
        ])


def safe_decimal(value):
    """
    Safely convert a numeric value (e.g., string, float)
    to a Decimal with 2 decimal places,
    ensuring it is always positive (absolute value).

    Parameters:
    - value (str or float or int): Numeric value to convert.

    Returns:
    - Decimal: A Decimal rounded to 2 places, using absolute value.

    Raises:
    - ValueError: If the input value cannot be converted to float.
    - decimal.InvalidOperation: If the value is invalid for Decimal.
    """
    return Decimal(str(abs(float(value)))).quantize(Decimal('0.01'))
