# core/validators.py
import re
from datetime import date
from decimal import Decimal
from rest_framework import serializers


def validate_nin(nin: str):
    """
    Validates that NIN is exactly 11 digits.
    """
    if not nin:
        raise serializers.ValidationError("NIN is required.")
    if not re.fullmatch(r'\d{11}', nin):
        raise serializers.ValidationError("NIN must be exactly 11 digits.")


def validate_phone(phone: str):
    """
    Validates Nigerian phone number format (starts with +234 or 0, 11 digits).
    """
    if not phone:
        raise serializers.ValidationError("Phone number is required.")
    if not re.fullmatch(r'^(\+234|0)[789]\d{9}$', phone):
        raise serializers.ValidationError("Invalid Nigerian phone number format.")


def validate_transaction_date(tx_date):
    """
    Validates that the transaction date is not in the future.
    """
    if tx_date > date.today():
        raise serializers.ValidationError("Transaction date cannot be in the future.")


def validate_amount(value):
    """
    Ensures transaction amount is a positive decimal.
    """
    if value <= 0:
        raise serializers.ValidationError("Transaction amount must be greater than zero.")


def validate_balance_after(value):
    """
    Optional but must not be negative if provided.
    """
    if value is not None and value < 0:
        raise serializers.ValidationError("Balance after transaction cannot be negative.")


def validate_transaction_type(value):
    """
    Accepts only 'credit' or 'debit'.
    """
    if value.lower() not in ['credit', 'debit']:
        raise serializers.ValidationError("Transaction type must be 'credit' or 'debit'.")


def validate_debit_vs_balance(transaction_type, amount, balance_after):
    """
    Ensures debit does not exceed balance (if balance provided).
    """
    if transaction_type == 'debit' and balance_after is not None and amount > balance_after:
        raise serializers.ValidationError("Debit amount cannot exceed resulting balance.")


def validate_csv_headers(headers: list, expected_headers: list):
    """
    Validates that uploaded CSV headers match the expected structure.
    """
    if headers != expected_headers:
        raise serializers.ValidationError(f"CSV headers must match: {expected_headers}")
