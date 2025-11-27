from django.shortcuts import render
from django.http import JsonResponse
import requests
from config import settings

def index(request):
    return render(request, "tracker/index.html")

def test_openfda(request):
    """Quick test to explore OpenFDA API response."""
    
    drug_name = "glucosamine"
    
    # OpenFDA endpoint for drug labels
    url = "https://api.fda.gov/drug/label.json"
    
    params = {
        'api_key': settings.OPENFDA_API_KEY,
        'search': f'openfda.brand_name:"{drug_name}"',
        'limit': 1
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return JsonResponse(data, json_dumps_params={'indent': 2})
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)