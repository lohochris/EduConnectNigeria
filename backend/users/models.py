from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

# Custom User Manager
class CustomUserManager(BaseUserManager):
    """Manager to handle user creation using email as the primary identifier."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)  # Ensure new users are active by default

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    ROLE_STUDENT = 'student'
    ROLE_TUTOR = 'tutor'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = {
        ROLE_STUDENT: 'Student',
        ROLE_TUTOR: 'Tutor',
        ROLE_ADMIN: 'Admin'
    }

    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15, blank=True, null=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Enter a valid phone number.")]
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES.items(), default=ROLE_STUDENT)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Remove username field since we're using email
    username = None  

    # Fix related_name conflicts
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # No extra required fields

    objects = CustomUserManager()  # Assign custom manager

    class Meta:
        db_table = "users_customuser"
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        """Ensure email is always saved in lowercase."""
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    # Role-based helper methods
    def is_student(self):
        return self.role == self.ROLE_STUDENT

    def is_tutor(self):
        return self.role == self.ROLE_TUTOR

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "user_profiles"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.user.email}'s Profile"
