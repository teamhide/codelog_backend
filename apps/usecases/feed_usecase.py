import re
from dataclasses import dataclass
from typing import List, Union, NoReturn

import requests

from apps.entities import FeedEntity, TagEntity
from apps.repositories import FeedMySQLRepo, UserMySQLRepo
from core.exceptions import abort
from core.settings import get_config
from core.utils import TokenHelper


@dataclass
class OGTag:
    title: str = None
    image: str = None
    description: str = None


class FeedUsecase:
    def __init__(self):
        self.feed_repo = FeedMySQLRepo()
        self.user_repo = UserMySQLRepo()


class GetFeedListUsecase(FeedUsecase):
    def execute(self, header: str, prev: int = None) -> List[FeedEntity]:
        if header:
            payload = TokenHelper.decode(token=header.split()[1])

            feeds = self.feed_repo.get_feed_list(
                user_id=payload['user_id'],
                prev=prev,
            )
        else:
            feeds = self.feed_repo.get_feed_list(prev=prev)
        return feeds


class CreateFeedUsecase(FeedUsecase):
    def execute(
        self,
        url: str,
        tags: str,
        is_private: str,
        payload: dict,
    ) -> Union[FeedEntity, NoReturn]:
        # Extract payload from token
        user = self.user_repo.get_user(user_id=payload['user_id'])

        if not user:
            abort(400, error='user does not exist')

        # Get og tag info
        og_info = self._parse(url=url)

        # Check tags is valid
        if self._process_tags(tags=tags) is False:
            abort(400, error='invalid tag')

        # Process tags
        tags = self._process_tags(tags=tags)

        # Create feed
        feed = self.feed_repo.create_feed(
            user_id=user.id,
            url=url,
            tags=tags[:3],
            image=og_info.image,
            title=og_info.title,
            description=og_info.description,
            is_private=True if is_private == 'true' else False,
        )

        return feed

    def _parse(self, url: str) -> Union[OGTag, NoReturn]:
        try:
            r = requests.get(url=url, headers=get_config().request_headers)
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.MissingSchema,
        ):
            abort(400, error='incorrect url')

        ogtag = OGTag()

        title_pattern = '"og:title" content="(.+?)"'
        title = re.findall(title_pattern, r.text)

        if title:
            ogtag.title = title[:50]
        else:
            ogtag.title = None

        image_pattern = '"og:image" content="(.+?)"'
        image = re.findall(image_pattern, r.text)

        if image and image[0].startswith('http'):
            ogtag.image = image
        else:
            ogtag.image = None

        description_pattern = '"og:description" content="(.+?)"'
        description = re.findall(description_pattern, r.text)

        if description:
            ogtag.description = description[:50]
        else:
            ogtag.description = None

        return ogtag

    def _process_tags(self, tags: str) -> Union[List, bool]:
        if len(tags) > 100:
            return False

        tags = re.findall('#\w+\s*\w+', tags)

        for tag in tags:
            if len(tag) > 20:
                return False

        return tags


class GetTagListUsecase(FeedUsecase):
    def execute(self) -> List[TagEntity]:
        return self.feed_repo.get_tag_list()


class SearchFeedUsecase(FeedUsecase):
    def execute(
        self,
        header: str,
        keyword: str,
        prev: int = None,
    ) -> List[FeedEntity]:
        if header:
            payload = TokenHelper.decode(token=header.split()[1])
            feeds = self.feed_repo.search_feed(
                keyword=keyword,
                prev=prev,
                user_id=payload['user_id'],
            )
        else:
            feeds = self.feed_repo.search_feed(keyword=keyword, prev=prev)
        return feeds


class DeleteFeedUsecase(FeedUsecase):
    def execute(self, payload: dict, feed_id: int) -> Union[NoReturn, bool]:
        user = self.user_repo.get_user(user_id=payload['user_id'])

        if not user:
            abort(404, error='user does not exist')

        feed = self.feed_repo.get_feed(feed_id=feed_id)

        if feed.user_id != user.id:
            abort(401, error='do not have permission')

        self.feed_repo.delete_feed(feed_id=feed_id)

        return True
