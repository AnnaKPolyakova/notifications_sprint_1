import os

NUMBER_OF_TRIES_TO_GET_USERS = int(
    os.environ.get("NUMBER_OF_TRIES_TO_GET_USERS", 1)
)

GET_USER_INFO_HOST = os.environ.get("GET_USER_INFO_HOST")