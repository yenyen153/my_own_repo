from pydantic import BaseModel, HttpUrl, field_validator, ConfigDict
import re

class PttPostModel(BaseModel):
    board_name: str
    title: str
    link: HttpUrl
    author_ptt_id: str
    date: str
    content: str
    @field_validator('date')
    @classmethod
    def validate_date(cls, value:str) -> str:
        if not re.search(r"\d{4}[/]\d{2}[/]\d{2}\s\d{2}[:]\d{2}[:]\d{2}", value):
            raise ValueError('wrong date format')
        return value

    class Config(ConfigDict):
        from_attributes = True


class AuthorBase(BaseModel):
    author_ptt_id: str
    author_nickname: str

    class Config(ConfigDict):
        from_attributes = True

class BoardBase(BaseModel):
    board: str
    url: str

    class Config(ConfigDict):
        from_attributes = True

class PostBase(BaseModel):
    title: str
    link: str
    date: str
    content: str

    class Config(ConfigDict):
        from_attributes = True

class PostCreate(PostBase):
    board_name: str
    author_ptt_id: str
    author_nickname: str
    title: str
    content: str
    link: str
    date: str

    @field_validator('date')
    @classmethod
    def validate_date(cls, value: str) -> str:
        if not re.search(r"\d{4}[/]\d{2}[/]\d{2}\s\d{2}[:]\d{2}[:]\d{2}", value):
            raise ValueError('wrong date format')
        return value

    class Config(ConfigDict):
        from_attributes = True

class PostUpdate(PostBase):
    board_name: str
    author_ptt_id: str
    author_nickname: str

    class Config(ConfigDict):
        from_attributes = True

class PostResponse(PostBase):
    id: int
    board_id: int
    author_id: int
    title: str
    link: str
    content: str
    date: str

    @field_validator('date')
    @classmethod
    def validate_date(cls, value: str) -> str:
        if not re.search(r"\d{4}[/]\d{2}[/]\d{2}\s\d{2}[:]\d{2}[:]\d{2}", value):
            raise ValueError('wrong date format')
        return value

    class Config(ConfigDict):
        from_attributes = True
