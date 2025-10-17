# classrooms/views.py
from django.shortcuts import render, get_object_or_404
from .models import Building, Classroom

# classrooms/views.py
from django.db.models import Count, Q

def buildings_index(request):
    buildings = (
        Building.objects
        .annotate(published_room_count=Count('classrooms', filter=Q(classrooms__is_published=True)))
        .order_by("name")
    )
    return render(request, "classrooms/buildings.html", {"buildings": buildings})


def classroom_list_by_building(request, slug):
    building = get_object_or_404(Building, slug=slug)
    rooms = (Classroom.objects
             .filter(building=building, is_published=True)
             .select_related("building")
             .prefetch_related("panoramas", "photos")
             .order_by("room_number"))
    resources = building.resources.filter(published=True)

    return render(request, "classrooms/list.html", {"building": building, "rooms": rooms,  "resources": list(resources)})

def classroom_detail(request, pk):
    room = get_object_or_404(
        Classroom.objects.select_related("building").prefetch_related("panoramas", "photos"),
        pk=pk, is_published=True
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
        "instructor_pc_equipped",
        "instructor_monitor",
        "interactive_display",
        "class_capture",
        "env_light",
        "assistive_listening_device",
        'hdesk',

        # Boards and Screens 
        "chalk_board",
        "whiteboards_count",
        "projectors",
    ]
    feature_groups = {
        "Audio": ["voice_amplification","podium_microhpone","handheld_microphone","ceiling_microphone","lavalier_microphone"],
        "Video": ["web_conference_camera","ceiling_camera","document_camera","projectors"],
        "Presentation": ["wireless_presentation","instructor_pc_equipped","interactive_display","instructor_monitor","class_capture"],
        "Accessibility & Environment": ["assistive_listening_device","env_light","hdesk"],
        "Boards": ["chalk_board","whiteboards_count"],
    }
    highlights = []
    if room.class_capture: highlights.append("Panopto capture")
    if room.web_conference_camera: highlights.append("Web conferencing")
    if room.instructor_pc_equipped: highlights.append("Instructor PC")
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

    