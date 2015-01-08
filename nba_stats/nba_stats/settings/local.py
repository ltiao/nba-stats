from .base import *

MEDIA_URL = '/media/'
MEDIA_ROOT = '/Users/tiao/Desktop/nba-stats-media'

STATIC_ROOT = '/Users/tiao/Desktop/staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR.child('static'),
)

TEMPLATE_DIRS = [
	BASE_DIR.child('templates'),
]
