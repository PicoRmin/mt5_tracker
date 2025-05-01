from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from trading.models import MT5Account
from trading.serializers import MT5AccountSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_list_api(request):
    accounts = MT5Account.objects.filter(user=request.user)
    serializer = MT5AccountSerializer(accounts, many=True)
    return Response(serializer.data)