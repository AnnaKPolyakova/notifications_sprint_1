import logging
from http import HTTPStatus

import aiohttp
from config import settings
from validate_email import validate_email

logger = logging.getLogger(__name__)


class UsersDataGetter:
    def __init__(self, user_id):
        self.user_id = user_id

    @staticmethod
    def _is_valid_email(email):
        return validate_email(email)

    async def get_user_email(self):
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
                    mail = data.get('email', None)
                    if (
                            isinstance(mail, str) and
                            self._is_valid_email(mail) is True
                    ):
                        return mail
