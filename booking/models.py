from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class Shift(models.Model):
    shift_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    booked = models.BooleanField(default=False)


    def __str__(self):
        return self.shift_name

class Node(models.Model):
    node_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.node_name

class Booking(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shift} - {self.node} - {self.status}"


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('employee', 'Employee'),
        ]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)    
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Add phone number field

    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Add a unique related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
'granted to each of their groups.'),
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Add a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )


class ShiftSwapRequest(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    from_employee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='swap_requests_sent')
    to_employee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='swap_requests_received')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.from_employee} to {self.to_employee} for {self.shift}"