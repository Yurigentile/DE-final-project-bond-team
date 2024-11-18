from datetime import datetime
from decimal import Decimal

def custom_json_serializer(obj):
    """
    Default JSON serilaiser doesn't handle datetime and decimal data types.
    This is custom JSON serialiser handles them both.
    """

    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj