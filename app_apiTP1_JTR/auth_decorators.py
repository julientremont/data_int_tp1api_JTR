from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile
import hashlib
import secrets

def require_api_key(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return JsonResponse({'error': 'API key required'}, status=401)
        
        try:
            user_profile = UserProfile.objects.get(api_key=api_key, is_api_active=True)
            request.user_profile = user_profile
            request.user = user_profile.user
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        return func(request, *args, **kwargs)
    return wrapper

def require_permission(permission_code):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not hasattr(request, 'user_profile'):
                return JsonResponse({'error': 'Authentication required'}, status=401)
            
            if not request.user_profile.has_permission(permission_code):
                return JsonResponse({
                    'error': f'Permission denied. Required: {permission_code}'
                }, status=403)
            
            return func(request, *args, **kwargs)
        return wrapper
    return decorator