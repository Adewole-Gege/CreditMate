# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from business.models import SME
from .models import CreditScore
from audit.models import ScoreAuditLog
from core.score_engine import CreditScoringEngine


class CreditScoreView(APIView):
    """
    GET /api/score/<business_id>/?refresh=true
    Calculates or returns cached credit score for an SME.
    """
    def get(self, request, business_id):
        sme = get_object_or_404(SME, id=business_id)
        refresh = request.query_params.get("refresh", "false").lower() == "true"

        try:
            credit_score = getattr(sme, 'credit_score', None)

            if not credit_score or refresh:
                engine = CreditScoringEngine(sme)
                score, risk_level, version = engine.calculate_score()
                credit_score, _ = CreditScore.objects.update_or_create(
                    sme=sme,
                    defaults={
                        'score': score,
                        'risk_level': risk_level,
                        'data_version': version
                    }
                )

                # Log audit
                ScoreAuditLog.objects.create(
                    sme=sme,
                    score=credit_score.score,
                    risk_level=credit_score.risk_level,
                    data_version=credit_score.data_version,
                    requested_by="api"  # Replace with authenticated user if applicable
                )

            data = {
                "business_id": str(sme.id),
                "business_name": sme.business_name,
                "score": credit_score.score,
                "risk_level": credit_score.risk_level,
                "data_version": credit_score.data_version,
                "calculated_at": credit_score.calculated_at
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": "Failed to calculate credit score.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RiskLevelView(APIView):
    """
    GET /api/risk/<business_id>/
    Returns risk level only for a given SME.
    """
    def get(self, request, business_id):
        sme = get_object_or_404(SME, id=business_id)

        try:
            credit_score = getattr(sme, 'credit_score', None)

            if not credit_score:
                engine = CreditScoringEngine(sme)
                score, risk_level, version = engine.calculate_score()
                credit_score, _ = CreditScore.objects.update_or_create(
                    sme=sme,
                    defaults={
                        'score': score,
                        'risk_level': risk_level,
                        'data_version': version
                    }
                )

                ScoreAuditLog.objects.create(
                    sme=sme,
                    score=credit_score.score,
                    risk_level=credit_score.risk_level,
                    data_version=credit_score.data_version,
                    requested_by="api"
                )

            return Response({
                "business_id": str(sme.id),
                "risk_level": credit_score.risk_level
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": "Failed to retrieve risk level.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
