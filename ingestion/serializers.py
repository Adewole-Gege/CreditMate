from rest_framework import serializers
from .models import BankStatement


class BankStatementSerializer(serializers.ModelSerializer):
    """
    Serializer for the BankStatement model.
    Handles validation, serialization, and
    custom representation of statement data,
    including base64-encoded PDF content and
    structured transaction data.
    """

    class Meta:
        model = BankStatement
        fields = [
            'id',
            'business',
            'reference',
            'statement_file',
            'encoded_data',
            'start_date',
            'end_date',
            'total_income',
            'total_expenditure',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_reference(self, value):
        """
        Ensure the reference value is unique across
        all BankStatement records.
        This complements the database constraint with
        early serializer-level validation.
        """
        if BankStatement.objects.filter(reference=value).exists():
            raise serializers.ValidationError("Reference must be unique.")
        return value

    def to_representation(self, instance):
        """
        Override the default representation to avoid exposing
        full base64-encoded PDF content in API response.
        This keeps the response payload smaller and more readable.
        """
        data = super().to_representation(instance)
        file_string = f"[BASE64 ENCODED PDF of {instance.reference}]"
        data['statement_file'] = file_string
        return data
