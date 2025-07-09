import base64
import os
import tempfile
import pandas as pd

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now

from business.models import Business
from .models import BankStatement
from .utils.ai_utility import ask_ai_to_structure
from .utils.data_extract import extract_text_from_pdf, safe_decimal
from .serializers import BankStatementSerializer


class UploadBankStatementView(APIView):
    """
    POST: Uploads a bank statement PDF, extracts
    and structures transaction data using AI,
    then computes start/end dates, totals, and
    stores both file and structured data.
    """
    parser_classes = [MultiPartParser]

    def post(self, request, business_id):
        file = request.FILES.get('file')

        # Basic request validation
        if not file or not business_id:
            return Response(
                {'error': 'bank statement file and business_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            business = Business.objects.get(id=business_id)
        except Business.DoesNotExist:
            return Response(
                {'error': 'Business not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate reference string
        today_str = now().strftime('%Y%m%d%H%M%S')
        reference = f"ref-{business.id}_{today_str}"

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        # Extract raw text and structure with AI
        try:
            raw_text = extract_text_from_pdf(tmp_path)
            df = ask_ai_to_structure(raw_text)
        except Exception as e:
            os.unlink(tmp_path)
            return Response(
                {'error': f'AI extraction failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        os.unlink(tmp_path)

        # Data cleanup and computation
        try:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            df['balance'] = pd.to_numeric(df['balance'], errors='coerce')
            df.dropna(subset=['date', 'amount', 'balance'], inplace=True)

            start_date = df['date'].min().date()
            end_date = df['date'].max().date()

            total_income = safe_decimal(
                df[df['amount'] > 0]['amount'].sum()
            )
            total_expenditure = safe_decimal(
                df[df['amount'] < 0]['amount'].sum()
            )

        except Exception as e:
            return Response(
                {'error': f"DataFrame processing failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Encode original PDF and structured data
        try:
            file.seek(0)
            encoded_pdf = base64.b64encode(file.read()).decode()
            encoded_data = df.to_json(orient='records')
        except Exception as e:
            return Response(
                {'error': f'Encoding failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save everything to the DB
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

                return Response({
                    'message': 'Bank statement uploaded successfully',
                    'statement_id': str(statement.id),
                    'start_date': str(start_date),
                    'end_date': str(end_date),
                    'income': float(total_income),
                    'expenditure': float(total_expenditure),
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=400)

        except Exception as e:
            return Response(
                {'error': f'Database save failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DownloadBankStatementView(APIView):
    """
    GET: Downloads the original PDF of a bank
    statement from its base64-encoded field.
    """
    def get(self, request, statement_id):
        try:
            stmt = BankStatement.objects.get(pk=statement_id)
        except BankStatement.DoesNotExist:
            return Response(
                {'error': 'Statement not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # If ?meta=true is passed, return serialized metadata
        if request.query_params.get('meta') == 'true':
            serializer = BankStatementSerializer(stmt)
            return Response(serializer.data, status=200)

        # Otherwise, return the PDF as a file
        try:
            pdf_data = base64.b64decode(stmt.statement_file)
        except Exception:
            return Response(
                {'error': 'Invalid base64-encoded PDF data.'},
                status=500
            )

        response = HttpResponse(
            pdf_data,
            content_type='application/pdf'
        )
        attachment = f'attachment; filename="{stmt.reference}.pdf"'
        response['Content-Disposition'] = attachment
        return response
