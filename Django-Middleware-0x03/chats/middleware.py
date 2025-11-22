
from datetime import datetime
import logging
from django.http import HttpResponseForbidden


logger = logging.getLogger(__name__)
if not logger.handlers:
    fh = logging.FileHandler('requests.log')
    fh.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)


# In-memory store for tracking messages per IP address
# Key: IP address, Value: list of timestamps of messages sent
# Used for OffensiveLanguageMiddleware to limit message sending rate
messages = {}


class RequestLoggingMiddleware:
    """A middleware that logs each user’s requests to a file, including:
        - The timestamp
        - The user
        - The request path
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """A middleware that restricts access to the site during certain hours
       For example, block access outside of 9 AM to 5 PM
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        current_hour = datetime.now().hour

        if current_hour < 9 or current_hour >= 17:
            return HttpResponseForbidden("Access to this site is restricted to business hours (9 AM to 5 PM).")
        
        response = self.get_response(request)
        return response
    

class OffensiveLanguageMiddleware:
    """A middleware that limits the number of chat messages a user can send within a certain time window,
        based on their IP address
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.method == 'POST' and 'messages/' in request.path:
            # Get the ip address of the user
            ip = request.META.get('REMOTE_ADDR')

            if ip not in messages:
                messages[ip] = []
            
            # Filter out timestamps (messages) older than 1 minute
            one_minute_ago = datetime.now().timestamp() - 60
            messages[ip] = [ts for ts in messages[ip] if ts > one_minute_ago]

            # If the user has already sent 5 messages in the last minute, block the request to send the 6th
            if len(messages[ip]) >= 5:
                return HttpResponseForbidden("You have exceeded the limit of 5 messages per minute.")

            # If under the limit, allow the request to proceed and record the timestamp
            # Add the current message timestamp
            messages[ip].append(datetime.now().timestamp())
            print(messages)  # For debugging purposes

        response = self.get_response(request)
        return response



class RolepermissionMiddleware:
    """A middleware that restricts access to certain views based on user roles
       For example, only allow users with 'admin' role to access admin views
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Example: restrict access to /admin/ path to users with 'admin' role
        if 'api/admin/' in request.path:
            if not request.user.is_authenticated or not request.user.role == 'admin':
                return HttpResponseForbidden("You do not have permission to access this page.")
        
        response = self.get_response(request)
        return response
