# I have created this file. - Younus

from django.http import HttpResponse
from django.shortcuts import render



# # E-Commerce Website Code functions: ---------------
#                                                     |
#                                                     |
# # def index(request):                               |
# #     return render(request, 'index.html')          |
#                                                     |
# # def about(request):                               |
# #     return render(request, 'sample.html')         |
#                                                     |
# ----------------------------------------------------|      
#

# def new_website(request):
#     return render(request, 'new.html')

# def calculate(request):
#     return HttpResponse("Give me your name: ")


def calculator(request):
    result = ''
    try:
        if request.method == 'POST':
            n1 = eval(request.POST.get('num1'))
            n2 = eval(request.POST.get('num2'))
            opr = request.POST.get('opr')
            if opr == '+':
                result = n1 + n2
            elif opr == '-':
                result = n1 - n2
            elif opr == '*':
                result = n1 * n2
            elif opr == '/':
                result = n1 / n2
    except:
        result = 'Invalid Input!'
    print(result)
    return render(request, 'calculator.html', {'result':result}) 
            


