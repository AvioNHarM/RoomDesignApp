import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Account(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_id = models.CharField(
        max_length=100, unique=True, default=uuid.uuid4, editable=False
    )
    username = models.CharField(max_length=64)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        if not self.user_id:
            self.user_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def check_password(self, password):
        return check_password(password, self.password)


class Model(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    model_file = models.FileField(upload_to="models/")
    axis = models.JSONField(default=list)
    rotations = models.JSONField(default=list)
    size = models.IntegerField()
    img = models.ImageField(upload_to="model_images/", blank=True, null=True)
    tags = models.JSONField(default=list)
    listed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="rooms")
    description = models.TextField(blank=True)
    room_file = models.FileField(upload_to="rooms/")
    sizes = models.JSONField(default=list)

    def __str__(self):
        return self.name


class RoomModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_models")
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    size = models.IntegerField()
    rotations = models.JSONField(default=list)
    axis = models.JSONField(default=list)

    def __str__(self):
        return f"{self.model.name} in room {self.room.name}"
