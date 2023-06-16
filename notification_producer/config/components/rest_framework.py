
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Notification API',
    'DESCRIPTION': 'Notification API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
