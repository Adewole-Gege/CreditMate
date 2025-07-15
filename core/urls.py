from django.urls import path
from .views import RiskLevelView, ScoreFromStatementView

urlpatterns = [
    path('risk/<int:business_id>/', RiskLevelView.as_view(), name='risk-level'),
    path('score-from-statement/<uuid:statement_id>/', ScoreFromStatementView.as_view(), name='score-from-statement'),
]
