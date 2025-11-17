from django.shortcuts import render

def main(request):
    context = {'my_range': range(10)}
    # context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)