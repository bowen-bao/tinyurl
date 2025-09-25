import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from shortener.services import create_short_link
from shortener.models import Link
from shortener.validators import is_valid_url
from shortener.services import get_cached_url, cache_url
from ratelimit.decorators import ratelimit

def home(request):
    return HttpResponse("TinyURL backend is running.")

@csrf_exempt
@require_http_methods(["POST"])
@ratelimit(key='ip', rate='10/m', block=True)
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
    """
        Redirect to the long URL for a given short code.
        First check Redis cache; if not found, fall back to DB and then cache it.
    """
    # 1) Try Redis cache first
    cached_url = get_cached_url(code)
    if cached_url:
        # We can't increment clicks or check expiry if we skip DB,
        # so fetch minimal info only if you want those features
        try:
            link = Link.objects.get(code=code)
            if link.expires_at and timezone.now() > link.expires_at:
                return HttpResponseNotFound("Link expired")
            # update click count
            Link.objects.filter(pk=link.pk).update(clicks=link.clicks + 1)
        except Link.DoesNotExist:
            # If somehow cached but DB record removed, treat as not found
            return HttpResponseNotFound("Not found")
        return HttpResponseRedirect(cached_url)

    # 2) Fallback to database
    try:
        link = get_object_or_404(Link, code=code)
        if link.expires_at and timezone.now() > link.expires_at:
            return HttpResponseNotFound("Link expired")

        # increment click count
        Link.objects.filter(pk=link.pk).update(clicks=link.clicks + 1)

        # 3️⃣ Cache the long URL for future lookups
        cache_url(code, link.long_url, ttl=3600)

        return HttpResponseRedirect(link.long_url)
    except Link.DoesNotExist:
        return HttpResponseNotFound("Not found")

def health(request):
    return JsonResponse({"ok": True})