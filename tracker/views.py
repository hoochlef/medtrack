import markdown
from django.contrib import messages
from django.shortcuts import redirect, render

from tracker.helpers import convert_image_to_nump_array
from tracker.services import run_custom_slm, run_ocr

from .forms import MedicationImageForm


def medication_lookup(request):
    """view function intended for the image submission form"""

    if request.method == "POST":
        form = MedicationImageForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data["medication_image"]
            
            # 1. convert uploaded image to a format that ocr model can work with
            image_array = convert_image_to_nump_array(image)

            # 2. run ocr on the image
            ocr_result = run_ocr(image_array)

            # 3. pass the ocr result to the model
            slm_response = run_custom_slm(ocr_result)

            # Convert markdown to HTML
            html_response = markdown.markdown(slm_response)

            messages.success(request, html_response, extra_tags="safe")
            return redirect("tracker:medication_lookup")

    else:
        form = MedicationImageForm()

    return render(request, "tracker/medication_lookup.html", {"form": form})
