from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from business.models import Business
from ingestion.utils.files_parser import parse_csv, parse_json
from ingestion.serializers import (
    TransactionBulkSerializer,
    TransactionSerializer,
    Transaction)


@api_view(['POST'])
@parser_classes([MultiPartParser, JSONParser])
def upload_transactions(request, business_id):
    business_id = business_id
    file = request.FILES.get('file')

    if not business_id or not file:
        return Response(
            {'error': 'Missing business_id or file'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        business = Business.objects.get(id=business_id)
    except Business.DoesNotExist:
        return Response(
            {'error': 'Business not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        if file.name.endswith('.csv'):
            transactions_data = parse_csv(file)
        elif file.name.endswith('.json'):
            transactions_data = parse_json(file)
        else:
            return Response(
                {'error': 'Unsupported file format'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

    for tx in transactions_data:
        tx['business_id'] = business.id

    serializer = TransactionBulkSerializer(
        data=transactions_data,
        many=True
    )

    try:
        if serializer.is_valid():
            serializer.save()
            count = serializer.created_count
            return Response(
                {'message': f"{count} transactions uploaded successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': serializer.errors[0]},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'errors': e},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_business_transactions(request, business_id):
    try:
        business = Business.objects.get(id=business_id)
    except Business.DoesNotExist:
        return Response(
            {'error': 'Business not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    transactions = Transaction.objects.filter(business=business
                                              ).order_by('-date')
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
