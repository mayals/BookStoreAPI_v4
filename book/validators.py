from django.core.exceptions import ValidationError

from urllib.parse import urlparse

def validate_hostname(*hostnames):
    hostnames = set(hostnames)
    def validator(value):
        try:
            result = urlparse(value)
            if result.hostname not in hostnames:
                raise ValidationError(f'The hostname {result.hostname} is not allowed.')
        except ValueError:
            raise ValidationError('invalid url')
    return validator