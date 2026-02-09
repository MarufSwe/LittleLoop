from django.http import HttpResponse
from django.conf import settings
import os


def debug_config(request):
    """Debug view to check configuration"""
    output = f"""
    <h1>Configuration Debug</h1>
    <ul>
        <li><strong>DEBUG:</strong> {settings.DEBUG}</li>
        <li><strong>DATABASE_URL in env:</strong> {'DATABASE_URL' in os.environ}</li>
        <li><strong>Database HOST:</strong> {settings.DATABASES['default'].get('HOST', 'Not set')}</li>
        <li><strong>Database NAME:</strong> {settings.DATABASES['default'].get('NAME', 'Not set')}</li>
    </ul>
    """
    return HttpResponse(output)
