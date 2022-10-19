from settings import table
from pydantic import BaseModel


class Statistics(BaseModel):
    page_id: int
    page_name: str
    posts: int
    followers: int
    follow_requests: int
    likes: int
    owner_id: int
