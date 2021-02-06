from django.shortcuts import redirect, render
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect ('login')

    else: 
        form = UserRegisterForm() 
    return render(request, 'users/register.html',{'form':form})

def login(request):
    
    return render(request,'users/login.html')