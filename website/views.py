from django.shortcuts import redirect, render

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):

    records = Record.objects.all()

    if request.method != "POST":
        return render(request, 'home.html', {'records': records})
    username = request.POST['username']
    password = request.POST['password']

    # Authenticate
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, "You Have Been Logged In!")
    else:
        messages.success(request, "There was An Error Logging In, Please Try Again...")
    return redirect('home')


def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out!!")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            return _extracted_from_register_user_5(form, request)
    else:
        form =SignUpForm()

        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


# TODO Rename this here and in `register_user`
def _extracted_from_register_user_5(form, request):
    form.save()
    # Authenticate and Login
    username = form.cleaned_data['username']
    password = form.cleaned_data['password1']
    user = authenticate(username=username, password=password)
    login(request, user)
    messages.success(request, "You Have Successfully Registered! Welcome!")
    return redirect('home')


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be Logged In to View This Page...")
        return redirect('home')
    

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
    else:
        messages.success(request, "You must be Logged In to DO that!!")

    return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST" and form.is_valid():
            add_record = form.save()
            messages.success(request, "Record Added...")
            return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You Must be Logged In...")
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been Updated...")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You Must be Logged In...")
        return redirect('home')