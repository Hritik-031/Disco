from django.contrib import admin
from .models import ICICIB22_investment,ICICIB22_profit,SBC_investment,SBC_profit, SBC_highest_price,ICICIB22_highest_price

admin.site.register(ICICIB22_investment)
admin.site.register(ICICIB22_profit)
admin.site.register(SBC_investment)
admin.site.register(SBC_profit)
admin.site.register(SBC_highest_price)
admin.site.register(ICICIB22_highest_price)
