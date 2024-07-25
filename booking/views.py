from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .utils import *




def home(request):
    return render(request, 'home.html')

def add_shift(request):
    if request.method == 'POST':
        shift_name = request.POST['shift_name']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        # Convert string inputs to datetime objects
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

        Shift.objects.create(shift_name=shift_name, start_time=start_time, end_time=end_time)
        messages.success(request, 'Shift added successfully.')
        return redirect('shift_list')
    return render(request, 'add_shift.html')
# views.py
def shift_list(request):
    shifts = Shift.objects.filter(booked=False)  # Only show unbooked shifts
    return render(request, 'shift_list.html', {'shifts': shifts})


# booking/views.py


from .utils import *


@login_required
def book_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    nodes = Node.objects.all()
    if request.method == 'POST':
        node_id = request.POST.get('node_id')
        if node_id:
            node = get_object_or_404(Node, id=node_id)
            booking = Booking.objects.create(shift=shift, node=node, status='booked')
            shift.booked = True
            shift.save()

            # Send SMS notification
            message = f"Hey there, Shift '{shift.shift_name}' has been booked from {shift.start_time} to {shift.end_time}."
            send_sms(request.user.phone_number, message)

            # Send Email notification
            subject = "Shift Booking Confirmation"
            email_message = f"Dear {request.user.get_full_name()},\n\nYour shift '{shift.shift_name}' has been successfully booked from {shift.start_time} to {shift.end_time}.\n\nThank you."
            send_email(subject, email_message, request.user.email)

            messages.success(request, f'Successfully booked shift "{shift.shift_name}" for "{node.node_name}".')
            return redirect('shift_list')
        else:
            messages.error(request, 'Please select a node.')
    return render(request, 'book_shift.html', {'shift': shift, 'nodes': nodes})

def api_get_shifts(request):
    shifts = list(Shift.objects.values())
    return JsonResponse(shifts, safe=False)

def api_book_shift(request):
    if request.method == 'POST':
        shift_id = request.POST['shift_id']
        node_id = request.POST['node_id']
        shift = Shift.objects.get(id=shift_id)
        node = Node.objects.get(id=node_id)
        booking = Booking.objects.create(shift=shift, node=node, status='pending')
        return JsonResponse({'booking_id': booking.id, 'status': booking.status})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# booking/views.py
def booked_shifts(request):
    bookings = Booking.objects.all()
    return render(request, 'booked_shifts.html', {'bookings': bookings})


def booking_list(request):
    bookings = Booking.objects.select_related('shift', 'node').all()  # Retrieve all bookings with related shifts and nodes
    return render(request, 'bookings.html', {'bookings': bookings})


def login_view(request):
    if request.method == 'POST':
        print("POST request received")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("User authenticated")
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'manager':
                return redirect('manager_dashboard')
            elif user.role == 'employee':
                return redirect('employee_dashboard')
        else:
            print("Invalid credentials")
            return render(request, 'User/login.html', {'error': 'Invalid credentials'})
    print("Rendering login page")
    return render(request, 'User/login.html')



def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'User/register.html', {'form': form})



def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Change this to your desired profile page
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'User/profile.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'User/profile.html', {'form': form})

@login_required
def admin_dashboard(request):
    user = request.user
    shifts = Shift.objects.filter(booked=False)  # or any other logic to fetch shifts
    messages = []  # Fetch or create messages as needed

    context = {
        'user': user,
        'shifts': shifts,
        'messages': messages
    }
    return render(request, 'Dashboard/admin_dashboard.html', context)

@login_required
def manager_dashboard(request):
    return render(request, 'Dashboard/manager_dashboard.html')

@login_required
def employee_dashboard(request):
    return render(request, 'Dashboard/employee_dashboard.html')


@login_required
def request_shift_swap(request, shift_id, to_employee_id):
    shift = Shift.objects.get(id=shift_id)
    to_employee = CustomUser.objects.get(id=to_employee_id)
    ShiftSwapRequest.objects.create(shift=shift, from_employee=request.user, to_employee=to_employee)
    messages.success(request, 'Shift swap request sent successfully.')
    return redirect('shift_list')

@login_required
def manage_shift_swaps(request):
    if request.user.role == 'manager':
        swaps = ShiftSwapRequest.objects.filter(status='pending')
        return render(request, 'manage_shift_swaps.html', {'swaps': swaps})
    else:
        return redirect('home')

@login_required
def approve_swap(request, swap_id):
    swap = ShiftSwapRequest.objects.get(id=swap_id)
    swap.status = 'approved'
    swap.save()
    messages.success(request, 'Shift swap approved.')
    return redirect('manage_shift_swaps')

@login_required
def deny_swap(request, swap_id):
    swap = ShiftSwapRequest.objects.get(id=swap_id)
    swap.status = 'denied'
    swap.save()
    messages.success(request, 'Shift swap denied.')
    return redirect('manage_shift_swaps')