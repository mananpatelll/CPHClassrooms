from django.shortcuts import render, get_object_or_404
from .models import Classroom

def classroom_list(request):
    rooms = (Classroom.objects
            .filter(is_published=True)
            .prefetch_related("panoramas")
            .order_by("building", "room_number"))
    return render(request, "classrooms/list.html", {"classrooms": rooms})

def classroom_detail(request, pk):
    room = get_object_or_404(Classroom.objects.prefetch_related("panoramas"), pk=pk, is_published=True)
    return render(request, "classrooms/detail.html", {"room": room})
