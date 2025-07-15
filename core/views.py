# core/views.py
from ingestion.models import BankStatement  # ensure this model exists
from .models import CreditScore, Business
from audit.models import ScoreAuditLog
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .score_engine import CreditScoringEngine  # Import the scoring engine
from django.shortcuts import render

class ScoreFromStatementView(APIView):
    def get(self, request, statement_id):
        statement = get_object_or_404(BankStatement, id=statement_id)
        business = statement.business  # assuming FK from statement to business

        refresh = request.query_params.get("refresh", "false").lower() == "true"
        try:
            credit_score = getattr(business, 'credit_score', None)

            if not credit_score or refresh:
                engine = CreditScoringEngine(business)
                score, risk_level, version = engine.calculate_score()
                credit_score, _ = CreditScore.objects.update_or_create(
                    sme=business,
                    defaults={
                        'score': score,
                        'risk_level': risk_level,
                        'data_version': version
                    }
                )
                ScoreAuditLog.objects.create(
                    sme=business,
                    score=credit_score.score,
                    risk_level=credit_score.risk_level,
                    data_version=credit_score.data_version,
                    requested_by="api"
                )

            return Response({
                "statement_id": str(statement.id),
                "business_id": str(business.id),
                "business_name": business.name,
                "score": credit_score.score,
                "risk_level": credit_score.risk_level,
                "data_version": credit_score.data_version,
                "calculated_at": credit_score.calculated_at
            }, status=200)

        except Exception as e:
            return Response({
                "error": "Failed to calculate score from statement",
                "details": str(e)
            }, status=500)



class RiskLevelView(APIView):
    """
    GET /api/risk/<business_id>/
    Returns risk level only for a given business.
    """

    def get(self, request, business_id):
        business = get_object_or_404(Business, id=business_id)

        try:
            credit_score = getattr(business, 'credit_score', None)

            if not credit_score:
                engine = CreditScoringEngine(business)
                score, risk_level, version = engine.calculate_score()

                credit_score, _ = CreditScore.objects.update_or_create(
                    sme=business,
                    defaults={
                        'score': score,
                        'risk_level': risk_level,
                        'data_version': version
                    }
                )

                ScoreAuditLog.objects.create(
                    sme=business,
                    score=credit_score.score,
                    risk_level=credit_score.risk_level,
                    data_version=credit_score.data_version,
                    requested_by="api"
                )

            return Response({
                "business_id": str(business.id),
                "risk_level": credit_score.risk_level
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": "Failed to retrieve risk level.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def home_view(request):
    """
    This view will serve the 'index.html' template located in the
    'templates' directory
    """
    return render(request, 'index.html')