from rest_framework import serializers

from business.models import Business
from ingestion.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    business_id = serializers.PrimaryKeyRelatedField(
        source='business',
        queryset=Business.objects.all(),
        write_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            'business_id',
            'date',
            'description',
            'amount',
            'transaction_type',
            'balance',
            'reference'
        ]

    def validate_transaction_type(self, value):
        value = value.lower()
        if value not in ('credit', 'debit'):
            raise serializers.ValidationError(
                "Transaction type must be 'credit' or 'debit'."
            )
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )
        return value

    def validate(self, attrs):
        business = attrs.get('business')
        reference = attrs.get('reference')

        if business and reference:
            if Transaction.objects.filter(
                business=business,
                reference=reference
            ).exists():
                raise serializers.ValidationError(
                    {"reference": f"Reference '{reference}' \
                     already exists for this business."}
                )
        return super().validate(attrs)


class BulkTransactionSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        created_count = 0
        instances = []

        for item in validated_data:
            instance = Transaction.objects.create(**item)
            instances.append(instance)
            created_count += 1

        # Save count on the serializer instance so the view can access it
        self.created_count = created_count
        return instances

    def validate(self, attrs):
        seen_signatures = set()
        seen_refs = set()

        try:
            business_ids = {item['business'].id for item in attrs}
        except KeyError:
            raise serializers.ValidationError(
                {"business": "Each transaction must \
                 include a valid business."}
            )

        if len(business_ids) > 1:
            raise serializers.ValidationError(
                {"business": "All transactions must \
                 belong to the same business."}
            )

        business_id = next(iter(business_ids))

        try:
            references = [item['reference'] for item in attrs]
        except KeyError:
            raise serializers.ValidationError(
                {"reference": "Each transaction must include a reference."}
            )

        # Batch check for duplicates in DB
        existing_refs = set(
            Transaction.objects.filter(
                business__id=business_id,
                reference__in=references
            ).values_list('reference', flat=True)
        )

        for idx, item in enumerate(attrs):
            ref = item.get('reference')
            if not ref:
                raise serializers.ValidationError(
                    {f"item_{idx}": "Missing 'reference' in transaction."}
                )

            if ref in seen_refs:
                raise serializers.ValidationError(
                    {f"reference": f"Duplicate reference '{ref}' \
                     in uploaded file."}
                )
            seen_refs.add(ref)

            if ref in existing_refs:
                raise serializers.ValidationError(
                    {f"reference": f"Reference '{ref}' \
                     already exists for this business."}
                )

            try:
                signature = (
                    item['business'].id,
                    item['date'],
                    item['description'].strip().lower(),
                    float(item['amount']),
                    item['transaction_type'].lower(),
                    ref,
                )
            except KeyError as e:
                raise serializers.ValidationError(
                    {str(e): f"Missing required field \
                     '{str(e)}' in one of the transactions."}
                )

            if signature in seen_signatures:
                raise serializers.ValidationError(
                    {f"transaction": f"Duplicate transaction: \
                     '{item['description']}' on {item['date']}"}
                )
            seen_signatures.add(signature)

        return attrs


class TransactionBulkSerializer(TransactionSerializer):
    class Meta(TransactionSerializer.Meta):
        list_serializer_class = BulkTransactionSerializer
