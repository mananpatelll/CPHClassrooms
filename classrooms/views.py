# classrooms/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Classroom, Panorama
from django.http import Http404
from django.utils.text import slugify
from .models import Classroom

def _building_map():
    """slug -> canonical building name (only published rooms)"""
    names = (Classroom.objects
             .filter(is_published=True)
             .values_list("building", flat=True)
             .distinct())
    return {slugify(n): n for n in names}

def buildings_index(request):
    """
    Home: grid of buildings. Each tile shows a preview image (first room's first pano)
    and the room count. Clicking a tile goes to the classroom list for that building.
    """

    rooms = (Classroom.objects
             .filter(is_published=True)
             .prefetch_related(
                 Prefetch("panoramas", queryset=Panorama.objects.order_by("order","id"))
            )
             .order_by("building", "room_number"))

    seen = {}   # slug -> index in tiles
    tiles = []  # [{name, slug, count, preview}]
    for r in rooms:
        s = slugify(r.building)
        if s not in seen:
            pano = r.panoramas.first()
            tiles.append({
                "name": r.building,
                "slug": s,
                "count": 1,
                "preview": (pano.preview_url or pano.image_url) if pano else None,
            })
            seen[s] = len(tiles) - 1
        else:
            tiles[seen[s]]["count"] += 1

    # Optional: sort alphabetically by building name
    tiles.sort(key=lambda x: x["name"].lower())

    return render(request, "classrooms/buildings.html", {"buildings": tiles})

def classroom_list_by_building(request, building_slug):
    """
    Reuses your existing list template, but filtered to one building.
    """
    mapping = _building_map()
    building_name = mapping.get(building_slug)
    if not building_name:
        raise Http404("Building not found")

    rooms = (Classroom.objects
             .filter(is_published=True, building__iexact=building_name)
             .prefetch_related("panoramas")
             .order_by("room_number"))

    return render(request, "classrooms/list.html", {
        "classrooms": rooms,
        "building_name": building_name,  # for heading/breadcrumb
    })

# keep your existing classroom_detail unchanged
def classroom_detail(request, pk):
    room = get_object_or_404(
        Classroom.objects.prefetch_related("panoramas"),
        pk=pk, is_published=True
    )
    return render(request, "classrooms/detail.html", {"room": room})
