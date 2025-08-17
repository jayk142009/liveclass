from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, Http404
from django.conf import settings
import os, uuid
from datetime import datetime, timedelta

# Active rooms memory me store (production me DB better)
ACTIVE_ROOMS = {}


def index(request):
    """Landing page - Join or Create"""
    return render(request, "index.html")


def room(request, room_name):
    """Video chat + recording page with role"""
    if room_name not in ACTIVE_ROOMS or not ACTIVE_ROOMS[room_name]["active"]:
        raise Http404("Room expired or invalid")

    expiry = ACTIVE_ROOMS[room_name]["expiry"]
    if datetime.now() > expiry:
        ACTIVE_ROOMS[room_name]["active"] = False
        raise Http404("Room expired")

    # Role decide (default student)
    role = request.GET.get("role", "student")

    return render(request, "video.html", {
        "room_name": room_name,
        "role": role
    })


def create_room(request):
    """Admin ke liye naya room banata hai"""
    room_id = str(uuid.uuid4())[:8]   # short unique ID
    expiry = datetime.now() + timedelta(hours=2)  # 2 hours valid
    ACTIVE_ROOMS[room_id] = {"expiry": expiry, "active": True}

    # Teacher aur Student link
    teacher_link = request.build_absolute_uri(f"/room/{room_id}/?role=teacher")
    student_link = request.build_absolute_uri(f"/room/{room_id}/")

    return render(request, "room_created.html", {
        "teacher_link": teacher_link,
        "student_link": student_link,
        "room_id": room_id
    })


def end_room(request, room_id):
    """Admin manually room end karega"""
    if room_id in ACTIVE_ROOMS:
        ACTIVE_ROOMS[room_id]["active"] = False
    return redirect("index")


@csrf_exempt
@require_POST
def upload_recording(request):
    """Recording ko /media/ me save karta hai"""
    f = request.FILES.get("recording")
    if not f:
        return JsonResponse({"status": "error", "message": "No file received"}, status=400)

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    save_path = os.path.join(settings.MEDIA_ROOT, f.name)

    with open(save_path, "wb+") as dst:
        for chunk in f.chunks():
            dst.write(chunk)

    return JsonResponse({
        "status": "success",
        "file_url": settings.MEDIA_URL + f.name
    })
