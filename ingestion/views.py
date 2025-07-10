import base64
import os
import tempfile
import pandas as pd

from django.http import HttpResponse
from django.utils.timezone import now

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from business.models import Business
from .models import BankStatement, BankTransaction
from .utils.ai_utility import ask_ai_to_structure
from .utils.data_extract import extract_text_from_pdf, safe_decimal
from .serializers import BankStatementSerializer


class UploadBankStatementView(APIView):
    """
    POST: Upload a PDF bank statement.
    Extracts + structures transactions via AI,
    stores summary in BankStatement,
    stores all entries in BankTransaction.
    """
    parser_classes = [MultiPartParser]

    def post(self, request, business_id):
        file = request.FILES.get('file')

        if not file or not business_id:
            return Response(
                {'error': 'Bank statement file and business_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            business = Business.objects.get(id=business_id)
        except Business.DoesNotExist:
            return Response(
                {'error': 'Business not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        today_str = now().strftime('%Y%m%d%H%M%S')
        reference = f"ref-{business.id}_{today_str}"

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            raw_text = extract_text_from_pdf(tmp_path)
            df = ask_ai_to_structure(raw_text)

            # Ensure expected columns
            expected_cols = ['date', 'amount', 'balance', 'description', 'transaction_type', 'channel', 'counterparty']
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = None

        except Exception as e:
            os.unlink(tmp_path)
            return Response({'error': f'AI extraction failed: {str(e)}'}, status=400)

        os.unlink(tmp_path)

        try:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            df['balance'] = pd.to_numeric(df['balance'], errors='coerce')
            df.dropna(subset=['date', 'amount', 'balance'], inplace=True)

            start_date = df['date'].min().date()
            end_date = df['date'].max().date()

            total_income = safe_decimal(df[df['amount'] > 0]['amount'].sum())
            total_expenditure = safe_decimal(df[df['amount'] < 0]['amount'].sum())

        except Exception as e:
            return Response({'error': f'DataFrame processing failed: {str(e)}'}, status=400)

        try:
            file.seek(0)
            encoded_pdf = base64.b64encode(file.read()).decode()
            encoded_data = df.to_json(orient='records')
        except Exception as e:
            return Response({'error': f'Encoding failed: {str(e)}'}, status=400)

        try:
            serializer = BankStatementSerializer(data={
                'business': business.id,
                'reference': reference,
                'statement_file': encoded_pdf,
                'encoded_data': encoded_data,
                'start_date': start_date,
                'end_date': end_date,
                'total_income': total_income,
                'total_expenditure': total_expenditure,
            })

            if serializer.is_valid():
                statement = serializer.save()

                # Save transactions
                for _, row in df.iterrows():
                    BankTransaction.objects.create(
                        statement=statement,
                        date=row['date'],
                        amount=row['amount'],
                        balance=row['balance'],
                        description=row.get('description') or '',
                        transaction_type=row.get('transaction_type') or 'credit',
                        channel=row.get('channel') or '',
                        counterparty=row.get('counterparty') or ''
                    )

                return Response({
                    'message': 'Bank statement uploaded successfully',
                    'statement_id': str(statement.id),
                    'start_date': str(start_date),
                    'end_date': str(end_date),
                    'income': float(total_income),
                    'expenditure': float(total_expenditure),
                }, status=201)
            else:
                return Response(serializer.errors, status=400)

        except Exception as e:
            return Response({'error': f'Database save failed: {str(e)}'}, status=500)


class DownloadBankStatementView(APIView):
    """
    GET: Download bank statement PDF or metadata.
    - ?meta=true returns metadata.
    - otherwise returns base64-decoded PDF file.
    """

    def get(self, request, statement_id):
        try:
            stmt = BankStatement.objects.get(pk=statement_id)
        except BankStatement.DoesNotExist:
            return Response({'error': 'Statement not found'}, status=404)

        if request.query_params.get('meta') == 'true':
            serializer = BankStatementSerializer(stmt)
            return Response(serializer.data, status=200)

        try:
            pdf_data = base64.b64decode(stmt.statement_file)
        except Exception:
            return Response({'error': 'Invalid PDF encoding'}, status=500)

        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{stmt.reference}.pdf"'
        return response
