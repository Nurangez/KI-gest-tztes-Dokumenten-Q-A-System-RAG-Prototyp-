import sys, os, json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "..", "..", "src")
sys.path.append(SRC_DIR)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pipeline import answer_question


@csrf_exempt
def ask_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        frage = data.get("frage")
        antwort = answer_question(frage)
        return JsonResponse({"antwort": antwort})
    return JsonResponse({"error": "Nur POST erlaubt"}, status=405)