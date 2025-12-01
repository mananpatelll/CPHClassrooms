from django.contrib import admin
from .models import Building, Classroom, Panorama, ClassroomPhoto, BuildingResource
from django import forms

class PanoramaInline(admin.TabularInline):
    model = Panorama
    extra = 0
    fields = ("image_file", "preview_file", "yaw", "pitch", "hfov")



class ClassroomPhotoInline(admin.TabularInline):
    model = ClassroomPhoto
    extra = 0
    fields = ("image_file",)


class ClassroomAdminForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = "__all__"
        widgets = {"wireless_presentation": forms.CheckboxSelectMultiple}   
        



@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    form = ClassroomAdminForm

    list_display = ("building", "room_number", "capacity", "is_published", "updated_at")
    list_filter = ("building", "is_published",
                   "voice_amplification", "class_capture", "assistive_listening_device") #"instructor_pc_equipped",
    search_fields = ("room_number", "summary", "building__name")
    fields = (
        "building","room_type", "room_number", "external_id", "is_published", "stage", "multilevel_podium",
        "privacy_panel","windows","door_windows","lock",
        "capacity", "summary","seating_type",
        "preview_image_file",
        "voice_amplification",
        "podium_microhpone", "handheld_microphone","ceiling_microphone", "lavalier_microphone",
        "web_conference_camera","ceiling_camera","document_camera",
        
        "wireless_presentation","instructor_monitor", "interactive_display",#"instructor_pc_equipped"
        "class_capture","pc_type","touchscreen_presentation",
        "env_light","assistive_listening_device","hdesk",
        "chalk_board","whiteboards_count","projectors","projector_model","display_model",
        "book_url"
    )
    inlines = [PanoramaInline, ClassroomPhotoInline]


class BuildingResourceInline(admin.TabularInline):
    model = BuildingResource
    extra = 0
    fields = ("published", "order", "kind", "title", "url", "thumbnail_url", "summary")
    show_change_link = True

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("name", "campus", "classrooms_count","tech_contact_name","tech_contact","tech_contact_email","more_info_url")
    list_filter = ("campus",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BuildingResourceInline]  # ← add this

