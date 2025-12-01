# classrooms/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Building, Classroom
from django.views.decorators.cache import cache_page
# classrooms/views.py
from django.db.models import Count, Q


#@cache_page(300) # Cache for 5 minutes
def buildings_index(request):
    buildings = (
        Building.objects
        .annotate(published_room_count=Count('classrooms', filter=Q(classrooms__is_published=True)))
        .order_by("name")
    )
    return render(request, "classrooms/buildings.html", {"buildings": buildings})


#@cache_page(300)
def classroom_list_by_building(request, slug):
    building = get_object_or_404(Building, slug=slug)
    rooms = (Classroom.objects
             .filter(building=building, is_published=True)
             .select_related("building")
             .prefetch_related("panoramas", "photos")
             .order_by("room_number"))
    resources = building.resources.filter(published=True)

    return render(request, "classrooms/list.html", {"building": building, "rooms": rooms,  "resources": list(resources)})


#@cache_page(300)
def classroom_detail(request, slug, room_number):
    room = get_object_or_404(
        Classroom.objects.select_related("building").prefetch_related("panoramas", "photos"),
        building__slug = slug, room_number = room_number, is_published=True
    )
    feature_fields = [
        # Microhpones/Speakers and cameras 
        "voice_amplification",
            #Microphones
        'podium_microhpone',
        "handheld_microphone",
        "ceiling_microphone",
        'lavalier_microphone',

            #Cameras
        "web_conference_camera",
        "ceiling_camera",
        "document_camera",

        # Presentation/ desk features
                #Presentation Features 
        "wireless_presentation",
        #"instructor_pc_equipped",
        "instructor_monitor",
        "interactive_display",
        "class_capture",
        "env_light",
        "assistive_listening_device",
        'hdesk',

        # eniroment
        "chalk_board",
        "whiteboards_count",
        "projectors",
        "stage",
        "privacy_panel",
        "windows",
        "door_windows",
        
        "pc_type",
    ]
    feature_groups = {
        "Accessibility & Environment": ["assistive_listening_device","env_light","hdesk","stage","privacy_panel","windows","door_windows"],
        "Audio": ["voice_amplification","podium_microhpone","handheld_microphone","ceiling_microphone","lavalier_microphone"],
        "Video": ["web_conference_camera","ceiling_camera","document_camera","projectors"],
        "Presentation": ["wireless_presentation","interactive_display","instructor_monitor","class_capture", "pc_type", "touchscreen_presentation"], #"instructor_pc_equipped"
        "Boards": ["chalk_board","whiteboards_count"],
    }
    highlights = []
    if room.class_capture: highlights.append("Panopto capture")
    if room.web_conference_camera: highlights.append("Web conferencing")
    if room.interactive_display: highlights.append("Interactive display")
    if room.wireless_presentation: highlights.append("Wireless: " + room.get_wireless_presentation_display())
    return render(request, "classrooms/detail.html", {
        "room": room,
        "features": feature_fields,
        "feature_groups": feature_groups,
        "highlights": highlights,
        "panos": room.panoramas.all(),
        "photos": room.photos.all(),
    })
    return render(request, "classrooms/detail.html", {"room": room})
    
#@cache_page(300)
def classroom_detail_pk(request, pk):
    room = get_object_or_404(
        Classroom.objects.select_related("building"),
        pk=pk, is_published=True
    )
    return redirect(
        reverse("classroom_detail", args=[room.building.slug, room.room_number]),
        permanent=True
    )