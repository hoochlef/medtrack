from django import forms
from PIL import Image


class MedicationImageForm(forms.Form):
    # template_name = "tracker/form_template.html"
    medication_image = forms.ImageField(
        label="Upload Medication Image",
        help_text="Upload a clear photo showing the medication name",
        error_messages={
            "required": "Please select an image to upload.",
            "invalid_image": "Please upload a valid image file.",
        },
    )

    def clean_medication_image(self):
        """Additional validation for the image."""
        image_file = self.cleaned_data.get("medication_image")

        if image_file:
            if image_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large (max 5MB).")

            try:
                img = Image.open(image_file)  # Open file to check format

                if img.format.upper() not in ["JPEG", "PNG", "JPG"]:
                    raise forms.ValidationError(
                        "Allowed image formats: PNG, JPG, JPEG."
                    )

            except forms.ValidationError:
                raise
            except Exception:
                raise forms.ValidationError("Invalid or corrupted image file.")

        return image_file
