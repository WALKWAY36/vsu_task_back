from rest_framework.exceptions import Throttled
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, Throttled):
        detail_message = response.data.get('detail')
        
        response.data = {
            'error': detail_message
        }
    
    return response