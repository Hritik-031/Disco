from django.shortcuts import render
from .models import ICICIB22_investment,ICICIB22_profit,SBC_profit,SBC_investment
from rest_framework.decorators import api_view
from .serializers import IISerializer,IPSerializer,SISerializer,SPSerializer
from math import ceil

def calculate(serialized,cmp,total_stocks_sold):
    net_investment = serialized['net_investment']
    profit_margin_percentage = 1 # this is fixed. minimum return on profit should be 1% excluding deduction.
    present_number_of_stocks =int(serialized['stocks_added']) -  total_stocks_sold

    ####current
    ''' this represents the current scenerio based on current cmp. it answers 
        1)like how many shares are required to sell to gain the instantaneous profit.
        2) how much is the loss with percentage with current avg price
    '''
    current_avg_share_price = round(float(cmp/ present_number_of_stocks),2)
    current_diff= int(cmp)-net_investment
    current_percent_diff = round(float((cmp - net_investment) * 100/ net_investment),2)
    current_no_of_shares_to_sell= round(float(current_diff / current_avg_share_price),2)
    
    ###economic selling shares condition at current condition
    economic_shares_to_sell = ceil(current_no_of_shares_to_sell)
    economic_avg_share_price = current_avg_share_price
    economic_diff = current_diff

    while economic_diff < economic_shares_to_sell*economic_avg_share_price:
        economic_diff= int(cmp)-net_investment
        economic_percent_diff = round(float((cmp - net_investment) * 100/ net_investment),2)
        economic_avg_share_price += 0.01
        cmp+=1

    ####target
    '''
    this gives the target condition to sell the shares to gain the defined percentage of profit.
    provides no of shares would require to sell to gain percentage of profit with expected future avg share price
    '''
    target_profit_expectation_price= round(float(profit_margin_percentage/100)*net_investment,2)
    target_avg_share_price= round(float(net_investment+ target_profit_expectation_price)/present_number_of_stocks,2)
    target_no_of_shares_to_sell = round(float(target_profit_expectation_price/target_avg_share_price),2)
    ###optimal selling shares condition to achieve target
    '''
    as the above mentioned conditions are not always ideal to sell the shares as 1.24 shares can't be sold. 
    so this gives provides the ideal sell condition for shares to gain optimal profit.
    '''
    target_shares_to_sell =ceil(target_no_of_shares_to_sell)

    while target_profit_expectation_price < target_shares_to_sell * target_avg_share_price:
        target_profit_expectation_price= round(float(profit_margin_percentage/100)*net_investment,2)
        target_avg_share_price= round(float(net_investment+ target_profit_expectation_price)/present_number_of_stocks,2)
        profit_margin_percentage += 0.01

    
    if current_diff < 0:
        return {'current_scenerio':f"{current_diff} RS with {round(current_percent_diff,2)}% loss,current avg share price is {current_avg_share_price}",
                "target_scenerio": f" target profit is {target_profit_expectation_price} at {profit_margin_percentage}% :: {target_shares_to_sell} shares are required to sell at {target_avg_share_price}RS per share"}

    return {"current_scenerio": f"current profit is {current_diff} RS with {current_percent_diff}% profit :: {current_no_of_shares_to_sell} shares are required to sell. current avg share price is {current_avg_share_price} RS per share",
            "target_scenerio": f" target profit is {target_profit_expectation_price} at {round(profit_margin_percentage,2)}% :: {target_shares_to_sell} shares are required to sell at {target_avg_share_price} RS per share",
            "economic_scenerio": f"econmic profit is {economic_diff} RS with {economic_percent_diff}% :: shares to sell {economic_shares_to_sell}. economic avg share price : {round(economic_avg_share_price,2)} RS per share"}

def calculate_profit(serialized):
    net_profit=0
    for d1 in serialized.data:
        net_profit += d1['profit_amount']
    return {"net_profit": f"{net_profit} RS"}

@api_view(['GET'])
def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def get_profit_or_loss_icicib(request):
    """
    if profit then get the profit amount and get the number of shares 
    required to sell to get the profit amount
    else if loss then only get loss amount
    """
    serialized={}
    data= ICICIB22_investment.objects.all()
    serialized_data = IISerializer(data,many=True)

    net_investment= sum([dict['investment_amount_added'] for dict in serialized_data.data])
    stocks_added = sum([dict['stocks_added'] for dict in serialized_data.data])

    serialized['net_investment']= net_investment
    serialized['stocks_added']= stocks_added
    cmp = int(request.GET['cmp'])

    data1=ICICIB22_profit.objects.all()
    serialized1 = IPSerializer(data1,many=True)
    total_stocks_sold = sum([dict['stocks_sold'] for dict in serialized1.data])

    result= calculate(serialized,cmp,total_stocks_sold)
    result1=calculate_profit(serialized1)
    result['net_profit']= result1['net_profit']
    result['total_stocks']= stocks_added -total_stocks_sold
    result['net_investment']= net_investment
    return render(request, 'profit_or_loss.html', result)

@api_view(['GET'])
def get_profit_or_loss_sbc(request):
    """
    if profit then get the profit amount and get the number of shares 
    required to sell to get the profit amount
    else if loss then only get loss amount
    """
    serialized={}
    data= SBC_investment.objects.all()
    serialized_data= SISerializer(data,many=True)

    net_investment= sum([dict['investment_amount_added'] for dict in serialized_data.data])
    stocks_added = sum([dict['stocks_added'] for dict in serialized_data.data])

    serialized['net_investment']= net_investment
    serialized['stocks_added']= stocks_added
    cmp = int(request.GET['cmp'])
    
    data1=SBC_profit.objects.all()
    serialized1 = SPSerializer(data1,many=True)
    total_stocks_sold = sum([dict['stocks_sold'] for dict in serialized1.data])

    result= calculate(serialized,cmp,total_stocks_sold)
    result1=calculate_profit(serialized1)
    result['net_profit']= result1['net_profit']
    result['total_stocks']= stocks_added -total_stocks_sold
    result['net_investment']= net_investment
    return render(request, 'profit_or_loss.html', result)




 