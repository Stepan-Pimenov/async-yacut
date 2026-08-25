import re
import string

SHORT_LENGTH = 6
SHORT_MAX_LENGTH = 16
ORIGINAL_MAX_LENGTH = 2048
GENERATION_ATTEMPTS = 10

ALLOWED_CHARS = string.ascii_letters + string.digits
SHORT_PATTERN = f'^[{re.escape(ALLOWED_CHARS)}]+$'
RESERVED_SHORTS = ('files',)

REDIRECT_VIEW = 'redirect'
