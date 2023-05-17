from django.shortcuts import render
from .models import ICICIB22_investment,ICICIB22_profit,SBC_profit,SBC_investment,SBC_highest_price,ICICIB22_highest_price
from rest_framework.decorators import api_view
from .serializers import IISerializer,IPSerializer,SISerializer,SPSerializer,SBC_High_price_serializer,ICICIB22_High_price_serializer
from math import ceil,floor
import yfinance as yf

def calculate(serialized,cmp,total_stocks_sold,profit_margin_percentage,flag):
    net_investment = serialized['net_investment']
    # this is fixed. minimum return on profit should be 1% excluding deduction.
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
    if flag=='sbc':
        SBC_high_price_data = SBC_highest_price.objects.get(id=1)
        serialized_data = SBC_High_price_serializer(SBC_high_price_data)
        sbc_info = yf.Ticker('SBC.NS')
        high_day_price = sbc_info.info['dayHigh']
        high_price_db = serialized_data.data['high_share_price']
        if high_price_db < high_day_price:
            SBC_highest_price.objects.filter(id=1).update(high_share_price = high_day_price)
            percentage_deviation_from_high = 0
        else:
            percentage_deviation_from_high = f"{float(round((current_avg_share_price-high_price_db)*100/high_price_db,2))}"
    elif flag == 'icicib22':
        SBC_high_price_data = ICICIB22_highest_price.objects.get(id=1)
        serialized_data = ICICIB22_High_price_serializer(SBC_high_price_data)
        icicib22_info = yf.Ticker('ICICIB22.NS')
        high_day_price = icicib22_info.info['dayHigh']
        high_price_db = serialized_data.data['high_share_price']
        if high_price_db < high_day_price:
            ICICIB22_highest_price.objects.filter(id=1).update(high_share_price = high_day_price)
            percentage_deviation_from_high = 0
        else:
            percentage_deviation_from_high = f"{float(round((current_avg_share_price-high_price_db)*100/high_price_db,2))}"
    else:
        high_price_db='-'
        percentage_deviation_from_high = '-'

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
        return {'current_scenerio':f"{current_diff} RS with {round(current_percent_diff,2)}% loss,current avg share price is {current_avg_share_price} with {percentage_deviation_from_high}% deviation from high {high_price_db}",
                "target_scenerio": f" target profit is {target_profit_expectation_price} at {profit_margin_percentage}% :: {target_shares_to_sell} shares are required to sell at {target_avg_share_price}RS per share"}

    return {"current_scenerio": f"current profit is {current_diff} RS with {current_percent_diff}% profit :: {current_no_of_shares_to_sell} shares are required to sell. current avg share price is {current_avg_share_price} RS per share with {percentage_deviation_from_high}% deviation from high {high_price_db}",
            "target_scenerio": f" target profit is {target_profit_expectation_price} at {round(profit_margin_percentage,2)}% :: {target_shares_to_sell} shares are required to sell at {target_avg_share_price} RS per share",
    }

def calculate_profit(serialized):
    net_profit=0
    for d1 in serialized.data:
        net_profit += d1['profit_amount']
    return {"net_profit": f"{net_profit} RS"}

def Buy(investment_to_add,serialized,cmp,total_stocks_sold):
    net_investment = serialized['net_investment']
    present_number_of_stocks =int(serialized['stocks_added']) -  total_stocks_sold
    current_avg_share_price = round(float(cmp/ present_number_of_stocks),2)

    stocks_can_be_purchased_at_cmp = floor(investment_to_add/current_avg_share_price)

    effective_apparant_share_price_at_cmp = round((net_investment+investment_to_add)/(present_number_of_stocks+stocks_can_be_purchased_at_cmp),2)

    return {'stocks_can_be_purchased_at_cmp':stocks_can_be_purchased_at_cmp,'effective_apparant_share_price_at_cmp':effective_apparant_share_price_at_cmp}
    

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
    '''
    strategy:
    assuming it has lower risk of loss as it covers avg of 22 stox 
    treating ICICIB as a mutual fund 
    remove profit if market remains down consecutively for 3 days and invest money as decided if 2 day fall and 1 day raise 
    else add money monthly based on graph.
    '''

    serialized={}
    investment_to_add= 6000
    cmp = int(request.GET['cmp'])
    profit_margin_percentage = 1.2 # dont consider this for icicb 

    data= ICICIB22_investment.objects.all()
    serialized_data = IISerializer(data,many=True)

    net_investment= sum([dict['investment_amount_added'] for dict in serialized_data.data])
    stocks_added = sum([dict['stocks_added'] for dict in serialized_data.data])

    serialized['net_investment']= net_investment
    serialized['stocks_added']= stocks_added

    data1=ICICIB22_profit.objects.all()
    serialized1 = IPSerializer(data1,many=True)
    total_stocks_sold = sum([dict['stocks_sold'] for dict in serialized1.data])

    result= calculate(serialized,cmp,total_stocks_sold,profit_margin_percentage,'icicib22')
    result1=calculate_profit(serialized1)

    result['net_profit']= result1['net_profit']
    result['total_stocks']= stocks_added -total_stocks_sold
    result['net_investment']= net_investment
    result['apparant_share_price'] = round(result['net_investment']/result['total_stocks'],2)

    buying_condition = Buy(investment_to_add,serialized,cmp,total_stocks_sold)

    result['effective_apparant_share_price_at_cmp']=buying_condition['effective_apparant_share_price_at_cmp']
    result['stocks_can_be_purchased_at_cmp']= buying_condition['stocks_can_be_purchased_at_cmp']
    result['investment_to_add']=investment_to_add
    return render(request, 'profit_or_loss.html', result)

@api_view(['GET'])
def get_profit_or_loss_sbc(request):
    """
    if profit then get the profit amount and get the number of shares 
    required to sell to get the profit amount
    else if loss then only get loss amount
    """
    '''
    strategy:
    -- as risk involves while trading a particular stock. so economical approach would be.
    for SBC it is decided to apply stop loss at 15% of highest value.
    -- invest based on graph pattern at low or defined interval basis
    '''
    serialized={}
    investment_to_add = 9000
    cmp = int(request.GET['cmp'])
    recommended_stop_loss= 15
    profit_margin_percentage= 1.2

    data= SBC_investment.objects.all()
    serialized_data= SISerializer(data,many=True)

    net_investment= sum([dict['investment_amount_added'] for dict in serialized_data.data])
    stocks_added = sum([dict['stocks_added'] for dict in serialized_data.data])

    serialized['net_investment']= net_investment
    serialized['stocks_added']= stocks_added
    
    data1=SBC_profit.objects.all()
    serialized1 = SPSerializer(data1,many=True)
    total_stocks_sold = sum([dict['stocks_sold'] for dict in serialized1.data])

    result= calculate(serialized,cmp,total_stocks_sold,profit_margin_percentage,'sbc')
    result1=calculate_profit(serialized1)
    result['net_profit']= result1['net_profit']
    result['total_stocks']= stocks_added -total_stocks_sold
    result['net_investment']= net_investment
    result['apparant_share_price'] = round(result['net_investment']/result['total_stocks'],2)

    buying_condition = Buy(investment_to_add,serialized,cmp,total_stocks_sold)

    result['effective_apparant_share_price_at_cmp']=buying_condition['effective_apparant_share_price_at_cmp']
    result['stocks_can_be_purchased_at_cmp']= buying_condition['stocks_can_be_purchased_at_cmp']
    result['investment_to_add']=investment_to_add
    return render(request, 'profit_or_loss.html', result)