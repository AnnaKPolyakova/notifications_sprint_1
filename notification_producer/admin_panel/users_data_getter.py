import logging
import uuid
from http import HTTPStatus
from typing import Union

import aiohttp
from config import settings
from validate_email import validate_email

logger = logging.getLogger('logger')


def _is_valid_email(value):
    return validate_email(value)


def _is_valid_chat_id(value):
    return isinstance(value, int)


class UsersDataGetter:

    VALUES_AND_CHECKS = {
        "email": _is_valid_email,
        "chat_id": _is_valid_chat_id,
    }

    def __init__(self, user_id, field):
        self.user_id: uuid.UUID = user_id
        self.field: str = field
        self.value: Union[str, None] = None

    async def get_user_data(self):
        for _ in range(settings.NUMBER_OF_TRIES_TO_GET_USERS):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        settings.GET_USER_INFO_HOST.format(
                            user_id=self.user_id
                        )
                ) as response:
                    if response.status != HTTPStatus.OK:
                        continue
                    if response.status == HTTPStatus.NOT_FOUND:
                        logger.info(
                            "User {user_id} not exist".format(
                                user_id=self.user_id
                            )
                        )
                        break
                    data = await response.json()
                    self.value = data.get(self.field, None)
                    if self.value is None:
                        return
                    if self.VALUES_AND_CHECKS[self.field] is None:
                        return self.value
                    if self.VALUES_AND_CHECKS[self.field](self.value):
                        return self.value
                    return False
