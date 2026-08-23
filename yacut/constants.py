import string

SHORT_ID_LENGTH = 6
SHORT_ID_MAX_LENGTH = 16

ALLOWED_CHARS = string.ascii_letters + string.digits
SHORT_ID_PATTERN = r'^[A-Za-z0-9]+$'
RESERVED_SHORT_IDS = ('files',)

DUPLICATE_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
INVALID_SHORT_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'

DISK_API_HOST = 'https://cloud-api.yandex.net/'
DISK_API_VERSION = 'v1'
UPLOAD_FOLDER = 'app:/'
