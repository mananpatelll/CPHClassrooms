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
    return render(request, "classrooms/list.html", {"building": building, "rooms": rooms})

def classroom_detail(request, pk):
    room = get_object_or_404(
        Classroom.objects.select_related("building").prefetch_related("panoramas", "photos"),
        pk=pk, is_published=True
    )
    return render(request, "classrooms/detail.html", {
        "room": room,
        "panos": room.panoramas.all(),
        "photos": room.photos.all(),   # <-- add this
    })