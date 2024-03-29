import os

if int(os.environ.get('LOGGING_ON', 1)) == 1:
    LOG_FILE = os.getenv('LOG_FILE', 'tes-play.log')
    LOG_PATH = os.getenv('LOG_PATH', '')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'formatters': {
            'default': {
                'format':
                    '%(asctime)s %(levelname)s: '
                    '%(message)s [%(pathname)s:%(lineno)d]',
            },
            'verbose': {
                'format': '[{asctime}] [{name}] '
                          '[{levelname}] {module} > {message}',
                'style': '{',
                "format_date": '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'debug-console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                'filters': ['require_debug_true'],
            },
        },
        'loggers': {
            'django': {
                'handlers': ['debug-console'],
                'level': LOG_LEVEL,
                'propagate': True,
            },
            'logger': {
                'handlers': ['debug-console'],
                'level': LOG_LEVEL,
                'propagate': True,
            },
            '': {
                'handlers': ['debug-console'],
                'level': LOG_LEVEL,
                'propagate': True,
            },
        },
    }
