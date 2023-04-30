from .models import ICICIB22_investment,ICICIB22_profit,SBC_investment,SBC_profit,SBC_highest_price
from rest_framework.serializers import ModelSerializer

    
class IISerializer(ModelSerializer):
    class Meta:
        model= ICICIB22_investment
        fields='__all__'

class IPSerializer(ModelSerializer):
    class Meta:
        model= ICICIB22_profit
        fields='__all__'

class SISerializer(ModelSerializer):
    class Meta:
        model= SBC_investment
        fields='__all__'

class SPSerializer(ModelSerializer):
    class Meta:
        model= SBC_profit
        fields='__all__'

class SBC_High_price_serializer(ModelSerializer):
    class Meta:
        model = SBC_highest_price
        fields='__all__'
