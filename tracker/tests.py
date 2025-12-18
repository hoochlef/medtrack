import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image


class MedicationLookupViewTests(TestCase):
    url = reverse("tracker:medication_lookup")

    def create_test_image(self, format="PNG", size=(100, 100)):
        """Helper to create valid test images"""
        file = io.BytesIO()
        image = Image.new("RGB", size, color="red")
        image.save(file, format)
        file.seek(0)
        return SimpleUploadedFile(
            f"test.{format.lower()}",
            file.read(),
            content_type=f"image/{format.lower()}",
        )

    def create_fake_image(self, filename="fake.png"):
        """Helper to create non-image file"""
        return SimpleUploadedFile(
            filename, b"This is not an image", content_type="image/png"
        )

    def test_get_request_shows_form(self):
        """Test that GET request displays the form"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload Medication Image")
        self.assertIn("form", response.context)

    def test_valid_image_upload_png(self):
        """Test uploading a valid PNG image"""
        image = self.create_test_image(format="PNG")

        response = self.client.post(
            self.url,
            {"medication_image": image},
            follow=True,  # Follow the redirect
        )

        self.assertEqual(response.status_code, 200)
        # Check success message appears
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertIn("Image received", str(messages[0]))
