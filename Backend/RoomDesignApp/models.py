import uuid
from django.db import models


# Create your models here.
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


class Model(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    model_file = models.FileField(upload_to="models/")
    axis = models.JSONField(default=list)
    rotations = models.JSONField(default=list)
    size = models.IntegerField()
    img = models.ImageField(upload_to="model_images/", blank=True, null=True)
    tags = models.JSONField(default=list)
    listed = models.BooleanField(default=True)
    sizes = models.JSONField(default=list)
    initial_rotations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RoomModel(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    size = models.IntegerField()
    rotations = models.JSONField(default=list)
    axis = models.JSONField(default=list)

    def __str__(self):
        return f"RoomModel of {self.model.name}"


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    room_file = models.FileField(upload_to="rooms/")
    models = models.ManyToManyField("RoomModel", related_name="rooms")
    sizes = models.JSONField(default=list)

    def __str__(self):
        return self.name
