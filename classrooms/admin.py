from django.contrib import admin
from .models import Building, Classroom, Panorama, ClassroomPhoto


class PanoramaInline(admin.TabularInline):
    model = Panorama
    extra = 0


class ClassroomPhotoInline(admin.TabularInline):
    model = ClassroomPhoto
    extra = 0


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("name", "campus", "classrooms_count","tech_contact_name","tech_contact","tech_contact_email","more_info_url")
    list_filter = ("campus",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}



@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("building", "room_number", "capacity", "is_published", "updated_at")
    list_filter = ("building", "is_published",
                   "voice_amplification", "class_capture", "web_conference",
                   "apple_tv", "instructor_pc_equipped", "assistive_listening_device")
    search_fields = ("room_number", "summary", "building__name")
    fields = (
        "building", "room_number", "external_id", "is_published",
        "capacity", "summary",
        "preview_image",   # <-- new
        "voice_amplification", "class_capture", "web_conference",
        "handheld_microphone", "document_camera",
        "ceiling_microphone", "ceiling_camera",
        "web_conference_camera", "apple_tv",
        "instructor_pc_equipped", "assistive_listening_device",
        "whiteboards_count","book_url"
    )
    inlines = [PanoramaInline, ClassroomPhotoInline]
