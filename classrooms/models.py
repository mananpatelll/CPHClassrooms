from django.db import models
from django.utils.text import slugify
from multiselectfield import MultiSelectField

class Building(models.Model):
    class Campus(models.TextChoices):
        MAIN = "MAIN", "Main Campus"
        HSC  = "HSC",  "Health Sciences Center"
        AMBLER = "AMBLER", "Ambler Campus"           
        CENTER_CITY = "CENTER_CITY", "Center City"   
        JAPAN = "JAPAN", "Temple Japan"              

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
    
    WIRELESS_CHOICES = [
        ("kramer", "Kramer"),
        ("apple_tv", "Apple TV"),
        ("screenbeam", "ScreenBeam"),
    ]
    # identity
    external_id = models.CharField(max_length=120, unique=True)
    building = models.ForeignKey(Building, related_name="classrooms", on_delete=models.PROTECT)
    room_number = models.CharField(max_length=20)
    
      # NEW: card preview image (optional)
    preview_image = models.CharField(
        max_length=500, blank=True,
        help_text="Shown on cards. e.g. /media/alter-101-preview.jpg"
    )
    
    capacity = models.PositiveIntegerField(default=0, verbose_name="Capacity")
    summary = models.CharField(max_length=200, blank=True, verbose_name="Summary")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    # Microhpones/Speakers and cameras 
        #Speakers
    voice_amplification = models.BooleanField(default=False, verbose_name="Voice Amplification (Speakers)")
        #Microhpones
    podium_microhpone = models.BooleanField(default=False, verbose_name = "Podium Microphone")
    handheld_microphone = models.BooleanField(default=False, verbose_name="Handheld Microphone")
    ceiling_microphone = models.BooleanField(default=False, verbose_name="Ceiling Microphone")
    lavalier_microphone = models.BooleanField(default=False, verbose_name= "Wireless Lavalier Micrphone (Clipon)")
        #Cameras
    web_conference_camera = models.BooleanField(default=False, verbose_name="Web Conference Camera (PC)")
    ceiling_camera = models.BooleanField(default=False, verbose_name="Wall Mounted Camera (Zoom)")
    document_camera = models.BooleanField(default=False, verbose_name="Document Camera")


        
    # Presentation/ desk features
        #Presentation Features 
    wireless_presentation = MultiSelectField(choices=WIRELESS_CHOICES, blank=True, verbose_name= "Wireless Presentation")
    instructor_pc_equipped = models.BooleanField(default=False, verbose_name="Instructor PC Equipped")
    interactive_display = models.BooleanField(default=False, verbose_name="Interactive Display")
    instructor_monitor = models.BooleanField(default=False, verbose_name="Instructor Monitor")
    class_capture = models.BooleanField(default=False, verbose_name="Class Capture (Panopto)")
    env_light = models.BooleanField(default=False, verbose_name="Environmental Controls (Lighting)")
    assistive_listening_device = models.BooleanField(default=False, verbose_name="Assistive Listening Device")
    hdesk = models.BooleanField(default=False, verbose_name = "Height adjustable desk/podium")

    # Boards and Screens 
    chalk_board = models.PositiveIntegerField(default=0, verbose_name="Chalkboards")
    whiteboards_count = models.PositiveIntegerField(default=0, verbose_name="Whiteboards")
    projectors = models.PositiveIntegerField(default=0, verbose_name="Projectors")

    

    book_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Booking URL from 25Live",
        verbose_name="Booking URL"
    )

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
