from uuid import UUID

from pydantic import BaseModel


class UserID(BaseModel):
    user_id: UUID


class UserKey(BaseModel):
    user_id: UUID
    key: str


class UserData(BaseModel):
    user_id: UUID
    key: str
    value: str


class KeyValueResponse(BaseModel):
    key: str
    value: str
