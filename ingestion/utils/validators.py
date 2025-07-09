from rest_framework.exceptions import ValidationError
from datetime import datetime

REQUIRED_FIELDS = ['date',
                   'description',
                   'amount',
                   'transaction_type',
                   'reference']


def validate_transaction_payload(data):
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in [None, '']:
            raise ValidationError(f"'{field}' is required")

    transaction_types = ['credit', 'debit']

    if data['transaction_type'].lower() not in transaction_types:
        raise ValidationError(
            f"transaction_type must be one of: {', '.join(transaction_types)}"
        )

    try:
        float(data['amount'])
    except (ValueError, TypeError):
        raise ValidationError(
            "amount must be a valid number"
        )

    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
    except (ValueError, TypeError):
        raise ValidationError(
            "date must be in YYYY-MM-DD format"
        )

    if len(data['reference']) > 100:
        raise ValidationError(
            "reference must not exceed 100 characters"
        )
