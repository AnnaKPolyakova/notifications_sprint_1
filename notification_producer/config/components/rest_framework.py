
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Notification API',
    'DESCRIPTION': 'Notification API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
