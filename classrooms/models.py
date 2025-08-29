from django.db import models
from django.utils.text import slugify


class Building(models.Model):
    class Campus(models.TextChoices):
        MAIN = "MAIN", "Main Campus"
        HSC  = "HSC",  "Health Sciences Center"
        AMBLER = "AMBLER", "Ambler Campus"           # add others you need
        CENTER_CITY = "CENTER_CITY", "Center City"   # example extra
        JAPAN = "JAPAN", "Temple Japan"              # example extra

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    campus = models.CharField(max_length=32, choices=Campus.choices, default=Campus.MAIN)
    preview = models.CharField(max_length=500, blank=True, help_text="e.g. /media/preview.jpeg")
    tech_contact_name = models.CharField(max_length=120, blank = True)
    tech_contact = models.CharField(max_length=50, blank=True)
    tech_contact_email = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    more_info_url = models.CharField(max_length=500, blank=True)



    class Meta:
        ordering = ["name"]

    def __str__(self): return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def classrooms_count(self):
        return self.classrooms.filter(is_published=True).count()


class Classroom(models.Model):
    # identity
    external_id = models.CharField(max_length=120, unique=True)
    building = models.ForeignKey(Building, related_name="classrooms", on_delete=models.PROTECT)
    room_number = models.CharField(max_length=20)
    
      # NEW: card preview image (optional)
    preview_image = models.CharField(
        max_length=500, blank=True,
        help_text="Shown on cards. e.g. /media/alter-101-preview.jpg"
    )

    # display
    capacity = models.PositiveIntegerField(default=0)
    summary = models.CharField(max_length=200, blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    # normalized features (from your list)
    voice_amplification = models.BooleanField(default=False)
    class_capture = models.BooleanField(default=False)
    web_conference = models.BooleanField(default=False)

    handheld_microphone = models.BooleanField(default=False)
    document_camera = models.BooleanField(default=False)
    ceiling_microphone = models.BooleanField(default=False)
    ceiling_camera = models.BooleanField(default=False)

    web_conference_camera = models.BooleanField(default=False)
    apple_tv = models.BooleanField(default=False)
    instructor_pc_equipped = models.BooleanField(default=False)
    assistive_listening_device = models.BooleanField(default=False)

    whiteboards_count = models.PositiveIntegerField(default=0)
    book_url =models.CharField(max_length=500, blank= True, help_text = "Booking URL from 25live")
    class Meta:
        indexes = [
            models.Index(fields=["building", "room_number"]),
            models.Index(fields=["is_published"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["building", "room_number"], name="uniq_building_room_fk")
        ]

    def __str__(self): return f"{self.building.name} {self.room_number}"


class Panorama(models.Model):
    external_id = models.CharField(max_length=120, unique=True)
    classroom = models.ForeignKey(Classroom, related_name="panoramas", on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=True)
    image_url = models.CharField(max_length=500, blank=True, help_text="e.g. /media/preview.jpeg")
            # keep URL to /media/.. for now
    preview_url = models.CharField(max_length=500, blank=True, help_text="e.g. /media/preview.jpeg")

    yaw = models.FloatField(default=0)
    pitch = models.FloatField(default=0)
    hfov = models.FloatField(default=90)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]


# models.py (just this change)
class ClassroomPhoto(models.Model):
    classroom = models.ForeignKey(Classroom, related_name="photos", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500, blank=True, help_text="e.g. /media/some.jpg")
    caption = models.CharField(max_length=140, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Photo for {self.classroom} ({self.order})"
