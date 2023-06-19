import os

NUMBER_OF_TRIES_TO_GET_USERS = int(
    os.environ.get("NUMBER_OF_TRIES_TO_GET_USERS", 1)
)

GET_USER_INFO_HOST = os.environ.get("GET_USER_INFO_HOST")
AUTH_HOST = os.environ.get("AUTH_HOST", "")
GET_USERS_INFO_HOST = os.environ.get("GET_USERS_INFO_HOST", "")
PAGE_SIZE_FOR_NUMBERS_INFO_HOST = int(
    os.environ.get("PAGE_SIZE_FOR_NUMBERS_INFO_HOST", 10)
)
