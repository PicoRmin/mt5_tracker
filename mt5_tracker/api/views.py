import json
from datetime import datetime
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from trading.models import MT5Account, Trade
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def test_connection(request):
    token = request.data.get('token')
    try:
        user = User.objects.get(auth_token__key=token)
        return Response({'status': 'success', 'message': 'Connection successful'})
    except User.DoesNotExist:
        return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def register_account(request):
    token = request.data.get('token')
    account_id = request.data.get('account_id')
    broker = request.data.get('broker')
    
    try:
        user = User.objects.get(auth_token__key=token)
    except User.DoesNotExist:
        return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    account, created = MT5Account.objects.get_or_create(
        account_id=account_id,
        defaults={
            'user': user,
            'broker': broker,
            'token': token
        }
    )
    
    return Response({
        'status': 'success',
        'account_id': account.account_id,
        'is_new': created
    })
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def upload_trade(request):
    try:
        # Parse JSON data directly from request.data (DRF handles this automatically)
        data = request.data
        
        # Verify token
        if not request.auth or data.get('token') != request.auth.key:
            return Response({'error': 'Invalid token'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get or create MT5 account
        account, created = MT5Account.objects.get_or_create(
            account_id=data.get('account_id'),
            defaults={
                'user': request.user,
                'broker': data.get('broker', 'Unknown'),
                'token': data.get('token')
            }
        )
        
        # Parse datetime strings
        entry_time = datetime.strptime(data['entry_time'], '%Y-%m-%d %H:%M:%S')
        exit_time = datetime.strptime(data['exit_time'], '%Y-%m-%d %H:%M:%S')
        
        # Create trade record
        trade = Trade.objects.create(
            account=account,
            ticket_id=data['ticket_id'],
            symbol=data['symbol'],
            type=data['type'],
            volume=data['volume'],
            entry_price=data['entry_price'],
            exit_price=data['exit_price'],
            profit=data['profit'],
            swap=data['swap'],
            commission=data['commission'],
            entry_time=entry_time,
            exit_time=exit_time,
            duration=data['duration'],
            magic_number=data.get('magic_number', 0),
            comment=data.get('comment', '')
        )
        
        return Response({
            'status': 'success',
            'trade_id': trade.id,
            'account_id': account.account_id
        })
        
    except Exception as e:
        return Response({
            'error': str(e),
            'received_data': data if 'data' in locals() else None
        }, status=status.HTTP_400_BAD_REQUEST)