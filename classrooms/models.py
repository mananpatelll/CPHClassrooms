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
    preview_file = models.ImageField(upload_to="buildings/previews/%Y/%m/%d/", blank=True, null=True)
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
    SEATING_CHOICES = [
        ("tables and chairs", "Tables and Chairs"),
        ("tablet armchairs", "Tablet armchairs")
    ]
    
    PC_TYPE = [
        ("windows", "Windows PC"),
        ("MacOs", "MacOs (Apple Mac)")
    ]
    # identity
    external_id = models.CharField(max_length=120, unique=True)
    building = models.ForeignKey(Building, related_name="classrooms", on_delete=models.PROTECT)
    room_number = models.CharField(max_length=20)
    
    
      # NEW: card preview image (optional)
    preview_image_file = models.ImageField(upload_to="classrooms/previews/%Y/%m/%d/", blank=True, null=True)
    room_type = models.CharField(max_length=10, blank=True, verbose_name = "Room type")
    capacity = models.PositiveIntegerField(default=0, verbose_name="Capacity")
    summary = models.CharField(max_length=200, blank=True, verbose_name="Summary")
    seating_type = MultiSelectField(choices=SEATING_CHOICES, blank=True, verbose_name = "Seating Type")
    is_published = models.BooleanField(default=False, verbose_name="Published")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    
    #Classroom config
    windows = models.BooleanField(default=False, verbose_name = "Windows in classroom")
    stage = models.BooleanField(default=False, verbose_name= "Stage")
    multilevel_podium = models.BooleanField(default=False, verbose_name = "Level 2 podium or Level 3 podium")
    privacy_panel = models.BooleanField(default=False, verbose_name = "Privacy panel for teacher desk")
    env_light = models.BooleanField(default=False, verbose_name="Environmental Controls (Lighting)")
    assistive_listening_device = models.BooleanField(default=False, verbose_name="Assistive Listening Device")
    hdesk = models.BooleanField(default=False, verbose_name = "Height adjustable desk/podium")
    door_windows = models.BooleanField(default=False, verbose_name = "Door with window")
    lock = models.CharField(max_length=50, verbose_name = "Lock Type", blank=True)
    
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
    #instructor_pc_equipped = models.BooleanField(default=False, verbose_name="Instructor PC Equipped")
    interactive_display = models.BooleanField(default=False, verbose_name="Interactive Display")
    instructor_monitor = models.BooleanField(default=False, verbose_name="Instructor Monitor")
    class_capture = models.BooleanField(default=False, verbose_name="Class Capture (Panopto)")
    pc_type = MultiSelectField(choices=PC_TYPE,blank = True, verbose_name = "Operating System")


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
    
    #admin info 
    projector_model = models.CharField(max_length=100, verbose_name = "Projector Model", blank=True)
    display_model = models.CharField(max_length =100, blank=True, verbose_name="Display Model and size")

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
    image_file = models.ImageField(upload_to="panoramas/%Y/%m/%d/", blank=True, null=True)
    preview_file = models.ImageField(upload_to="panoramas/previews/%Y/%m/%d/", blank=True, null=True)

    yaw = models.FloatField(default=0)
    pitch = models.FloatField(default=0)
    hfov = models.FloatField(default=90)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]


# models.py (just this change)
class ClassroomPhoto(models.Model):
    classroom = models.ForeignKey(Classroom, related_name="photos", on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)

    caption = models.CharField(max_length=140, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Photo for {self.classroom} ({self.order})"
    
    
# --- New: resources attached to a Building --------------------
class BuildingResource(models.Model):
    class Kind(models.TextChoices):
        YOUTUBE = "youtube", "YouTube Video"
        LINK = "link", "External Link"

    building = models.ForeignKey(Building, related_name="resources", on_delete=models.CASCADE)
    kind = models.CharField(max_length=16, choices=Kind.choices, default=Kind.LINK)
    title = models.CharField(max_length=160)
    url = models.CharField(max_length=600)
    # optional thumbnail to override auto-generated ones
    thumbnail_url = models.CharField(max_length=600, blank=True)
    summary = models.TextField(blank=True)
    published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        indexes = [
            models.Index(fields=["building", "published"]),
            models.Index(fields=["order", "created_at"]),
        ]

    def __str__(self):
        return f"{self.building.name}: {self.title}"

    # very lightweight YouTube id extraction for youtu.be / youtube.com
    @property
    def youtube_id(self):
        if self.kind != self.Kind.YOUTUBE:
            return None
        u = (self.url or "").strip()
        if "youtu.be/" in u:
            return u.rsplit("youtu.be/", 1)[-1].split("?")[0].split("&")[0]
        if "youtube.com" in u and "v=" in u:
            return u.split("v=", 1)[-1].split("&")[0]
        return None

    @property
    def display_thumbnail(self):
        if self.thumbnail_url:
            return self.thumbnail_url
        vid = self.youtube_id
        if vid:
            # fall back to standard YT thumbnail if not provided
            return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        return ""  # let template show a neutral placeholder
