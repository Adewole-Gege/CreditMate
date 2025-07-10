# core/serializers.py
from rest_framework import serializers
from .models import CreditScore
from audit.models import ScoreAuditLog  # Ensure this path is correct


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
        read_only_fields = ['business_id', 'business_name', 'sector', 'state', 'calculated_at']

    def validate_score(self, value):
        if value < 0 or value > 1000:
            raise serializers.ValidationError("Score must be between 0 and 1000.")
        return value

    def validate_risk_level(self, value):
        valid_levels = ["Low", "Medium", "High"]
        if value not in valid_levels:
            raise serializers.ValidationError(f"Risk level must be one of {valid_levels}.")
        return value


class RiskLevelSerializer(serializers.ModelSerializer):
    business_id = serializers.UUIDField(source='sme.id', read_only=True)
    business_name = serializers.CharField(source='sme.business_name', read_only=True)

    class Meta:
        model = CreditScore
        fields = ['business_id', 'business_name', 'risk_level']

    def validate_risk_level(self, value):
        valid_levels = ["Low", "Medium", "High"]
        if value not in valid_levels:
            raise serializers.ValidationError(f"Risk level must be one of {valid_levels}.")
        return value


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
