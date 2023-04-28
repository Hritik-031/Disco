from django.db import models

# Create your models here.
    
class ICICIB22_investment(models.Model):
    investment_amount_added= models.IntegerField()
    avg_share_price = models.FloatField(default=1.0)
    stocks_added = models.IntegerField(default=0)
    date= models.CharField(max_length=100)

    class Meta:
        db_table = "II"

    def __str__(self):
        return self.date

class ICICIB22_profit(models.Model):
    profit_amount = models.IntegerField()
    stocks_sold = models.IntegerField(default=0)
    date= models.CharField(max_length=100)

    class Meta:
        db_table = "IP"
    
    def __str__(self):
        return self.date + ' - ' +str(self.profit_amount)
    
class SBC_investment(models.Model):
    investment_amount_added= models.IntegerField()
    avg_share_price = models.FloatField(default=1.0)
    stocks_added = models.IntegerField(default=0)
    date= models.CharField(max_length=100)

    class Meta:
        db_table = "SI"

    def __str__(self):
        return self.date

class SBC_profit(models.Model):
    profit_amount = models.IntegerField()
    stocks_sold = models.IntegerField(default=0)
    date= models.CharField(max_length=100)

    class Meta:
        db_table = "SP"
    
    def __str__(self):
        return self.date + ' - ' +str(self.profit_amount)