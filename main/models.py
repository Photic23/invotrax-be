from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from rolepermissions.roles import assign_role, clear_roles
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom user manager that handles soft delete functionality"""
    
    def get_queryset(self):
        """Return only active (not deleted) users by default"""
        return super().get_queryset().filter(is_deleted=False)
    
    def all_with_deleted(self):
        """Return all users including deleted ones"""
        return super().get_queryset()
    
    def deleted_only(self):
        """Return only deleted users"""
        return super().get_queryset().filter(is_deleted=True)
    
    def create_user(self, username, email, password=None, **extra_fields):
        """Create and save a normal user with the given details"""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and save a superuser with the given details"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model with additional fields and soft delete support"""
    email = models.EmailField(unique=True)  # Make email unique
    phone_number = models.CharField(max_length=15, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    
    # Role field for clear role identification
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('staff', 'Staff'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('owner', 'Owner'),  # Added owner role
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    
    # Soft delete fields
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Use custom manager
    objects = CustomUserManager()
    # Add all_objects manager to access all users (including deleted)
    all_objects = models.Manager()
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Assign role permissions on save if it's a new user or role has changed
        self.assign_role()
    
    def assign_role(self):
        """Assign role permissions based on the role field"""
        # Clear existing roles first
        clear_roles(self)
        
        # Assign new role - use proper capitalization to match your role classes
        if self.role == 'customer':
            assign_role(self, 'customer')  # Capital 'C' to match the class name
        elif self.role == 'vendor':
            assign_role(self, 'vendor')    # Capital 'V'
        elif self.role == 'staff':
            assign_role(self, 'staff')
        elif self.role == 'manager':
            assign_role(self, 'manager')
        elif self.role == 'admin':
            assign_role(self, 'admin')
    
    def has_active_pengajuan(self):
        """
        Check if user has any active PengajuanPenawaranPengadaan records.
        Returns True if the user has any pengajuan not in 'ditolak' or 'diterima' status
        """
        # Use imports inside method to avoid circular imports
        try:
            from pengajuan_penawaran_pengadaan.models import PengajuanPenawaranPengadaan
            
            # Check for any active pengajuan records based on the actual model structure
            # Using created_by field as per your model instead of user
            # Excluding only 'ditolak' and 'diterima' statuses as per your requirements
            active_count = PengajuanPenawaranPengadaan.objects.filter(
                created_by=self,
                is_deleted=False  # Only consider non-deleted pengajuan records
            ).exclude(
                status__in=['ditolak', 'diterima']
            ).count()
            
            return active_count > 0
            
        except ImportError:
            # If the model can't be imported, assume no active pengajuan
            return False
    
    def delete(self, using=None, keep_parents=False):
        """Soft delete the user instead of permanent deletion"""
        # Check if the user has active pengajuan records
        if self.has_active_pengajuan():
            raise ValidationError(
                "User cannot be deleted because they have active procurement proposals that are not yet accepted or rejected. "
                "Please process or cancel all active proposals before deleting this user."
            )
        
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def hard_delete(self):
        """Permanently delete the user from the database"""
        # Check if the user has active pengajuan records
        if self.has_active_pengajuan():
            raise ValidationError(
                "User cannot be deleted because they have active procurement proposals that are not yet accepted or rejected. "
                "Please process or cancel all active proposals before deleting this user."
            )
            
        super().delete()
    
    def restore(self):
        """Restore a soft-deleted user"""
        self.is_deleted = False
        self.deleted_at = None
        self.save()