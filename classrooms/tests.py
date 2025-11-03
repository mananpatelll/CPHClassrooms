# classrooms/tests.py
import io
import shutil
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import (
    Building, Classroom, Panorama, ClassroomPhoto, BuildingResource
)

# Use a temp MEDIA_ROOT and local storage so tests never hit S3
TEMP_MEDIA = tempfile.mkdtemp()

@override_settings(
    MEDIA_ROOT=TEMP_MEDIA,
    DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
)
class ClassroomAppTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    # ------------- helpers -----------------
    def _img_file(self, name="test.jpg", size=(8, 8), color=(200, 50, 50)):
        """Make a tiny in-memory JPEG."""
        buf = io.BytesIO()
        Image.new("RGB", size, color).save(buf, format="JPEG")
        buf.seek(0)
        return SimpleUploadedFile(name, buf.read(), content_type="image/jpeg")

    def _seed(self):
        b = Building.objects.create(name="1810 Liacouras Walk", campus=Building.Campus.MAIN)
        c = Classroom.objects.create(
            external_id="rm-420",
            building=b,
            room_number="420",
            capacity=40,
            is_published=True,
        )
        # files go to temp media
        Panorama.objects.create(
            external_id="p-1",
            classroom=c,
            image_file=self._img_file("pano.jpg"),
            preview_file=self._img_file("pano_preview.jpg"),
            yaw=10,
            pitch=0,
            hfov=95,
            order=1,
        )
        ClassroomPhoto.objects.create(
            classroom=c,
            image_file=self._img_file("photo.jpg"),
            caption="Wide shot",
            order=1,
        )
        return b, c

    # ------------- model tests -----------------
    def test_building_slug_autofilled(self):
        b = Building.objects.create(name="TECH Center", campus=Building.Campus.MAIN)
        self.assertTrue(b.slug)
        self.assertIn("tech-center", b.slug)

    def test_building_classrooms_count_only_published(self):
        b = Building.objects.create(name="Anderson Hall")
        Classroom.objects.create(external_id="a-101", building=b, room_number="101", is_published=True)
        Classroom.objects.create(external_id="a-102", building=b, room_number="102", is_published=False)
        self.assertEqual(b.classrooms_count, 1)

    def test_classroom_unique_constraint(self):
        b = Building.objects.create(name="Gladfelter Hall")
        Classroom.objects.create(external_id="g-101", building=b, room_number="101")
        with self.assertRaises(Exception):
            Classroom.objects.create(external_id="g-102", building=b, room_number="101")

    def test_building_resource_youtube_helpers(self):
        b = Building.objects.create(name="Alter")
        r1 = BuildingResource.objects.create(
            building=b, kind=BuildingResource.Kind.YOUTUBE,
            title="Short", url="https://youtu.be/abc123?t=10"
        )
        r2 = BuildingResource.objects.create(
            building=b, kind=BuildingResource.Kind.YOUTUBE,
            title="Long", url="https://www.youtube.com/watch?v=xyz789&list=foo"
        )
        self.assertEqual(r1.youtube_id, "abc123")
        self.assertEqual(r2.youtube_id, "xyz789")
        self.assertIn("/abc123/", r1.display_thumbnail)
        self.assertIn("/xyz789/", r2.display_thumbnail)

    # ------------- view tests -----------------
    def test_buildings_index_renders(self):
        b, c = self._seed()
        url = reverse("buildings_index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "classrooms/buildings.html")
        self.assertContains(resp, b.name)

    def test_home_routes_to_buildings(self):
        # sanity: home path exists and is the same view
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "classrooms/buildings.html")

    def test_list_by_building_renders_rooms(self):
        b, c = self._seed()
        resp = self.client.get(reverse("classroom_list_by_building", args=[b.slug]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "classrooms/list.html")
        self.assertContains(resp, b.name)
        self.assertContains(resp, c.room_number)

    def test_detail_renders_pano_and_photos(self):
        _, room = self._seed()  # make a building, room, pano, photo

        url = reverse('classroom_detail', args=[room.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # pano container exists
        self.assertContains(resp, '<div id="pano"></div>', html=True)
        # pannellum init present
        self.assertContains(resp, "pannellum.viewer('pano'", html=False)
        # thumbs exist
        self.assertContains(resp, 'class="sidebar-thumbs"', html=False)
        self.assertContains(resp, '<img', html=False)
    