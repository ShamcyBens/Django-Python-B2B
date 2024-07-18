from django.shortcuts import render, redirect, get_object_or_404
from .models import Shift, Booking, Node
from django.http import JsonResponse
from django.contrib import messages


def add_shift(request):
    if request.method == 'POST':
        shift_name = request.POST['shift_name']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        Shift.objects.create(shift_name=shift_name, start_time=start_time, end_time=end_time)
        return redirect('shift_list')
    return render(request, 'add_shift.html')

def shift_list(request):
    shifts = Shift.objects.all()
    return render(request, 'shift_list.html', {'shifts': shifts})


def book_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    nodes = Node.objects.all()
    if request.method == 'POST':
        node_id = request.POST.get('node_id')
        if node_id:
            node = get_object_or_404(Node, id=node_id)
            Booking.objects.create(shift=shift, node=node, status='pending')
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


def home(request):
    return render(request, 'home.html')



def booking_list(request):
    bookings = Booking.objects.select_related('shift', 'node').all()  # Retrieve all bookings with related shifts and nodes
    return render(request, 'bookings.html', {'bookings': bookings})

