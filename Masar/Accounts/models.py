from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        FLEET_MANAGER = "fleet_manager", "Fleet Manager"
        DISPATCHER = "dispatcher", "Dispatcher"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DISPATCHER)

    @property
    def is_fleet_manager(self):
        return self.role == self.Role.FLEET_MANAGER