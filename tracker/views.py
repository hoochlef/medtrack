from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
import requests
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
                messages.success(request, result)

            except Exception as e:
                messages.error(request, f"Error processing image: {str(e)}")

            return redirect("tracker:medication_lookup")

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


# def contact(request):
#     # if this is a POST request we need to process the form data
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         form = ContactForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             subject = form.cleaned_data["subject"]
#             message = form.cleaned_data["message"]
#             sender = form.cleaned_data["sender"]
#             cc_myself = form.cleaned_data["cc_myself"]

#             recipients = ["email@example.me"]
#             if cc_myself:
#                 recipients.append(sender)

#             # send_mail(subject, message, sender, recipients)
#             # redirect to a new URL:
#             return render(request, 'tracker/thanks.html', {'subject': subject, 'message': message,
#                                                            'sender': sender, 'cc_myself': cc_myself})
#             # return HttpResponseRedirect("/thanks/")
#         # else:
#         #     # form.errors contains the max_length error
#         #     print(form.errors)

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = ContactForm()

#     return render(request, "tracker/name.html", {"form": form})
