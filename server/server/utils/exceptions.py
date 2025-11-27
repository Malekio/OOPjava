from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': {
                'status_code': response.status_code,
                'message': 'An error occurred',
                'details': response.data
            },
            'success': False
        }
        
        # Log the error for monitoring
        logger.error(f"API Error: {response.status_code} - {response.data}")
        
        # Customize error messages based on status code
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data['error']['message'] = 'Invalid request data'
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_response_data['error']['message'] = 'Authentication required'
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response_data['error']['message'] = 'Permission denied'
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response_data['error']['message'] = 'Resource not found'
        elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            custom_response_data['error']['message'] = 'Rate limit exceeded'
        elif response.status_code >= 500:
            custom_response_data['error']['message'] = 'Internal server error'
            
        response.data = custom_response_data
    
    return response
