# core/score_engine.py
from datetime import timedelta
from collections import defaultdict
from django.utils import timezone
from ingestion.models import FinancialRecord
from business.models import SME
from decimal import Decimal
import statistics


class CreditScoringEngine:
    def __init__(self, sme: SME):
        self.sme = sme
        self.records = FinancialRecord.objects.filter(sme=sme).order_by('date')

    def calculate_score(self):
        if not self.records.exists():
            return 0, 'High', 'v1-no-data'

        revenue_score = self._score_revenue_trend()
        frequency_score = self._score_transaction_frequency()
        stability_score = self._score_cash_flow_stability()

        final_score = int((revenue_score + frequency_score + stability_score) / 3)
        risk_level = self._classify_risk(final_score)
        version = "v1-basic-rules"

        return final_score, risk_level, version

    def _score_revenue_trend(self):
        monthly_credits = defaultdict(Decimal)
        for record in self.records:
            if record.transaction_type == 'credit':
                key = record.date.strftime('%Y-%m')
                monthly_credits[key] += record.amount

        months = sorted(monthly_credits.keys())
        if len(months) < 2:
            return 500  # insufficient data

        growth_rates = []
        for i in range(1, len(months)):
            prev = monthly_credits[months[i - 1]]
            curr = monthly_credits[months[i]]
            if prev > 0:
                growth_rates.append(float((curr - prev) / prev))

        avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0
        if avg_growth >= 0.2:
            return 850
        elif avg_growth >= 0:
            return 650
        else:
            return 400

    def _score_transaction_frequency(self):
        recent_start = timezone.now().date() - timedelta(days=90)
        count = self.records.filter(date__gte=recent_start).count()

        if count >= 90:
            return 850
        elif count >= 30:
            return 650
        elif count > 0:
            return 400
        return 250

    def _score_cash_flow_stability(self):
        balances = [float(r.balance_after) for r in self.records if r.balance_after is not None]
        if len(balances) < 5:
            return 500

        avg = statistics.mean(balances)
        stddev = statistics.stdev(balances)
        if avg == 0:
            return 300

        volatility = stddev / avg
        if volatility < 0.2:
            return 900
        elif volatility < 0.5:
            return 700
        else:
            return 450

    def _classify_risk(self, score: int):
        if score <= 400:
            return 'High'
        elif score <= 700:
            return 'Medium'
        return 'Low'
