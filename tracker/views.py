import requests
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from config import settings

from .forms import MedicationImageForm


def medication_lookup(request):
    """view function intended for the image submission form"""

    if request.method == "POST":
        form = MedicationImageForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data["medication_image"]

            try:
                # TODO: Process the image (OCR, etc...)
                result = f"Image received: {image.name}, Size: {image.size} bytes"
            except Exception as e:
                messages.error(request, f"Error processing image: {str(e)}")
            else:
                messages.success(request, result)
                return HttpResponseRedirect(reverse("tracker:medication_lookup"))

    else:
        form = MedicationImageForm()

    return render(request, "tracker/medication_lookup.html", {"form": form})


def test_openfda(request):
    """Quick test to explore OpenFDA API response."""

    drug_name = "glucosamine"

    # OpenFDA endpoint for drug labels
    url = "https://api.fda.gov/drug/label.json"

    params = {
        "api_key": settings.OPENFDA_API_KEY,
        "search": f'openfda.brand_name:"{drug_name}"',
        "limit": 1,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return JsonResponse(data, json_dumps_params={"indent": 2})

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
