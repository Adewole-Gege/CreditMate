import csv
import io
import json
from rest_framework.exceptions import ValidationError

from .validators import validate_transaction_payload


def normalize_row(row):
    row['amount'] = float(row['amount'])
    row['transaction_type'] = row['transaction_type'].lower()
    row['description'] = row['description'].strip()
    return row


def parse_csv(file):
    decoded = file.read().decode('utf-8')
    io_string = io.StringIO(decoded)
    reader = csv.DictReader(io_string)
    transactions = []
    errors = []

    for index, row in enumerate(reader, start=1):
        try:
            validate_transaction_payload(row)
            transactions.append(normalize_row(row))
        except ValidationError as e:
            errors.append({'row': index, 'error': str(e.detail)})

    if errors:
        raise ValidationError(errors)

    return transactions


def parse_json(file):
    try:
        data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Expected a list of transaction objects")

        transactions = []
        errors = []

        for index, tx in enumerate(data, start=1):
            try:
                validate_transaction_payload(tx)
                transactions.append(normalize_row(tx))
            except ValidationError as e:
                errors.append({'index': index, 'error': str(e.detail)})

        if errors:
            raise ValidationError(errors)

        return transactions

    except json.JSONDecodeError:
        raise ValueError("Invalid JSON file")
