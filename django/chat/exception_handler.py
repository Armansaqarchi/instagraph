

def ws_exception_handler(exc, context):
    """
    by default the asyncConsumers does not handle exceptions like wsgi views do
    to enable exception handling, one way would be to override dispatch() method to wrap the endpoints in a
    try-except block
    """
    pass