from django.db import models

class Classroom(models.Model):
    external_id = models.CharField(max_length=120, unique=True)
    building = models.CharField(max_length=120)
    room_number = models.CharField(max_length=20)
    capacity = models.IntegerField(default=0)
    summary = models.CharField(max_length=200, blank=True)  # short blurb
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    attributes = models.JSONField(default=dict, blank=True)  

    class Meta:
        indexes = [
            models.Index(fields=["building", "room_number"]),
            models.Index(fields=["is_published"]),
        ]
        unique_together = (("building","room_number"),)

    def __str__(self): return f"{self.building} {self.room_number}"

class Panorama(models.Model):
    external_id = models.CharField(max_length=120, unique=True)
    classroom = models.ForeignKey(Classroom, related_name="panoramas", on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=True)
    image_url = models.URLField()               # 2:1 equirectangular (webp/jpg)
    preview_url = models.URLField(blank=True)   # low-res placeholder (optional)
    yaw = models.FloatField(default=0)
    pitch = models.FloatField(default=0)
    hfov = models.FloatField(default=90)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
