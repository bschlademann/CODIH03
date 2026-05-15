from django.shortcuts import render
from .models import Currency

def calculate_conversion(amount, from_rate, to_rate):
    if from_rate == 0: return 0
    return (amount / from_rate) * to_rate

def converter_home(request):
    currencies = Currency.objects.all()
    result = None
    from_id = None
    to_id = None
    amount = ""

    if request.method == "POST":
        amount_str = request.POST.get('amount')
        from_id_str = request.POST.get('from_currency_id')
        to_id_str = request.POST.get('to_currency_id')

        if amount_str and from_id_str and to_id_str:
            amount = amount_str
            from_id = int(from_id_str)
            to_id = int(to_id_str)
            
            from_curr = Currency.objects.get(id=from_id)
            to_curr = Currency.objects.get(id=to_id)
            
            result = calculate_conversion(amount, from_curr.exchange_rate, to_curr.exchange_rate)
            
    context = {
        'currencies': currencies, 
        'result': result,
        'from_id': from_id,
        'to_id': to_id,
        'amount': amount 
    }
    return render(request, 'converter/home.html', context)