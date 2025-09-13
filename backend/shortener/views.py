import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from shortener.services import create_short_link
from shortener.models import Link
from shortener.validators import is_valid_url


@csrf_exempt
@require_http_methods(["POST"])
def shorten(request):
    try:
        body = json.loads(request.body or "{}")
        long_url = body.get("url")
        custom = body.get("customCode")

        if not long_url:
            return JsonResponse({"error": "url is required"}, status=400)

        if not is_valid_url(long_url):
            return JsonResponse({"error": "invalid URL"}, status=400)

        link = create_short_link(long_url, custom_code=custom)
        return JsonResponse({"code": link.code, "shortUrl": f"/{link.code}"}, status=201)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)


def resolve(request, code: str):
    try:
        link = get_object_or_404(Link, code=code)
        if link.expires_at and timezone.now() > link.expires_at:
            return HttpResponseNotFound("Link expired")
        Link.objects.filter(pk=link.pk).update(clicks=link.clicks + 1)
        return HttpResponseRedirect(link.long_url)
    except Link.DoesNotExist:
        return HttpResponseNotFound("Not found")


def health(request):
    return JsonResponse({"ok": True})