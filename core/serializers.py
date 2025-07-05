from rest_framework import serializers
from .models import CreditScore
from audit.models import ScoreAuditLog #TODO- Ensure this import matches actual ScoreAuditLog model location


class CreditScoreSerializer(serializers.ModelSerializer):
    business_id = serializers.UUIDField(source='sme.id', read_only=True)
    business_name = serializers.CharField(source='sme.business_name', read_only=True)
    sector = serializers.CharField(source='sme.sector', read_only=True)
    state = serializers.CharField(source='sme.state', read_only=True)

    class Meta:
        model = CreditScore
        fields = [
            'business_id',
            'business_name',
            'sector',
            'state',
            'score',
            'risk_level',
            'data_version',
            'calculated_at',
        ]


class RiskLevelSerializer(serializers.ModelSerializer):
    business_id = serializers.UUIDField(source='sme.id', read_only=True)
    business_name = serializers.CharField(source='sme.business_name', read_only=True)

    class Meta:
        model = CreditScore
        fields = ['business_id', 'business_name', 'risk_level']


class ScoreAuditLogSerializer(serializers.ModelSerializer):
    business_id = serializers.UUIDField(source='sme.id', read_only=True)
    business_name = serializers.CharField(source='sme.business_name', read_only=True)

    class Meta:
        model = ScoreAuditLog
        fields = [
            'business_id',
            'business_name',
            'score',
            'risk_level',
            'data_version',
            'timestamp',
            'requested_by'
        ]
        read_only_fields = fields
