import asyncio
import logging
import uuid
from http import HTTPStatus
from typing import List, Optional

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

    def __init__(self, users_ids, field):
        self.users_ids: List[uuid.UUID] = users_ids
        self.field: str = field
        self.data: dict = dict()

    async def _get_user_data(self, page_number) -> Optional[dict]:
        last_id = page_number * settings.PAGE_SIZE_FOR_NUMBERS_INFO_HOST
        first_id = last_id - settings.PAGE_SIZE_FOR_NUMBERS_INFO_HOST + 1
        ids = self.users_ids[first_id - 1: last_id]
        data_ids = [str(user_id) for user_id in ids]
        for _ in range(settings.NUMBER_OF_TRIES_TO_GET_USERS):
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        settings.GET_USERS_INFO_HOST.format(
                            page=page_number,
                            field=self.field,
                        ),
                        json={"ids": data_ids}
                ) as response:
                    if response.status != HTTPStatus.OK:
                        continue
                    data = await response.json()
                    for user_id in data_ids:
                        if user_id not in data:
                            data[user_id] = False
                        if self.VALUES_AND_CHECKS[self.field] is not None:
                            if self.VALUES_AND_CHECKS[self.field](
                                data[user_id]
                            ) is False:
                                data[user_id] = False
                    return data
        return None

    def get_data_for_users(self) -> Optional[dict]:
        users_ids_count = len(self.users_ids)
        if users_ids_count == 0:
            return self.data
        requests_count = (
                users_ids_count // settings.PAGE_SIZE_FOR_NUMBERS_INFO_HOST
        )
        if users_ids_count % settings.PAGE_SIZE_FOR_NUMBERS_INFO_HOST > 0:
            requests_count += 1
        for page_number in range(1, requests_count + 1):
            part_data = asyncio.run(self._get_user_data(page_number))
            if part_data is None:
                return None
            self.data.update(part_data)
        return self.data
