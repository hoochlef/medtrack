from django import forms


class MedicationImageForm(forms.Form):
  # template_name = "tracker/form_template.html"
  medication_image = forms.ImageField(label='Upload Medication Image',
        help_text='Upload a clear photo showing the medication name',
        error_messages={
            'required': 'Please select an image to upload.',
            'invalid_image': 'Please upload a valid image file (JPG, PNG, etc.).',
            'invalid': 'Please upload a valid image file (JPG, PNG, etc.).'
        })


# def clean_medication_image(self):
#         """Additional validation for the image."""
#         image = self.cleaned_data.get('medication_image')
        
#         if image:
#             # Check file size (e.g., max 5MB)
#             if image.size > 5 * 1024 * 1024:
#                 raise forms.ValidationError('Image file too large (max 5MB).')
            
#             # Check file type
#             allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
#             if image.content_type not in allowed_types:
#                 raise forms.ValidationError('Only JPG and PNG images are allowed.')
        
#         return image