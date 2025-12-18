import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image


class MedicationLookupViewTests(TestCase):
    url = reverse("tracker:medication_lookup")

    # ~~~~~~~~~~ Helper functions ~~~~~~~~~~~
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

    # TODO: add tests for corrupted image files, for example an image that didn't 
    # fully get sent due to a network problem
    # def create_corrupted_image(self):
    #     """Helper to create a corrupted image file"""
    #     # valid png header - magic bytes
    #     png_header = b"\x89PNG\r\n\x1a\n"

    #     # Added data [PNG Header] → [garbage data]
    #     corrupted_data = png_header + b"corrupted image data that is not valid"

    #     return SimpleUploadedFile(
    #         "corrupted.png", corrupted_data, content_type="image/png"
    #     )

    # ~~~~~~~~~~ Helper functions ~~~~~~~~~~~

    def test_get_request_shows_form(self):
        """Test that GET request displays the form"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload Medication Image")
        self.assertIn("form", response.context)

    def test_require_file_to_upload(self):
        """Test that there's a file embedded in the form for processing"""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "medication_image",
            "Please select an image to upload.",
        )

    def test_reject_fake_image(self):
        """Test that any imposter image is rejected"""
        fake_image = self.create_fake_image(filename="faker.png")
        response = self.client.post(self.url, {"medication_image": fake_image})

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "medication_image",
            "Please upload a valid image file.",
        )

    # def test_reject_corrupted_image(self):
    #     """Test that corrupted images are rejected"""
    #     corrupted_image = self.create_corrupted_image()

    #     response = self.client.post(self.url, {"medication_image": corrupted_image})

    #     self.assertEqual(response.status_code, 200)
    #     self.assertFormError(
    #         response.context["form"],
    #         "medication_image",
    #         "Invalid or corrupted image file.",
    #     )

    def test_reject_webp_image(self):
        """Test that WebP images are rejected"""
        image = self.create_test_image(format="WEBP")

        response = self.client.post(self.url, {"medication_image": image})

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "medication_image",
            "Allowed image formats: PNG, JPG, JPEG.",
        )

    def test_reject_gif_image(self):
        """Test that GIF images are rejected"""
        image = self.create_test_image(format="GIF")

        response = self.client.post(self.url, {"medication_image": image})

        self.assertEqual(response.status_code, 200)

        self.assertFormError(
            response.context["form"],
            "medication_image",
            "Allowed image formats: PNG, JPG, JPEG.",
        )

    def test_reject_large_file(self):
        """Test that files over 5MB are rejected"""
        # Create a 6MB image
        large_img = self.create_test_image(format="PNG", size=(3000, 3000))

        # Make it larger by adding data
        large_img_file_content = large_img.read()
        # Pad to 6MB
        padded_content = large_img_file_content + b"0" * (6 * 1024 * 1024)

        large_img_file = SimpleUploadedFile(
            "large.png", padded_content, content_type="image/png"
        )

        response = self.client.post(self.url, {"medication_image": large_img_file})

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "medication_image",
            "Image file too large (max 5MB).",
        )

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

    def test_valid_image_upload_jpeg(self):
        """Test uploading a valid jpg/jpeg image"""

        image = self.create_test_image(format="JPEG")

        response = self.client.post(
            self.url,
            {"medication_image": image},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertIn("Image received", str(messages[0]))

    def test_successful_upload_redirects(self):
        """Upon successful POST request the page should redirect"""
        image = self.create_test_image(format="PNG")

        response = self.client.post(
            self.url,
            {"medication_image": image},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tracker:medication_lookup"))
