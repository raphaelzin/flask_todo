from typing import Optional
from common.base_model import BaseModel
from common.base_data import BaseData
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from typing import Dict
from datetime import datetime

class TagData(BaseData):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __init__(self, title):
        self.title = title

class Tag(BaseModel):
    id: Optional[int]
    title: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def __init__(self, title):
        self.title = title

    def to_dict(self) -> Dict:
        include_keys = {
            "title": ...,
            "created_at": ...,
            "updated_at": ...
        }
        ret = self.dict(by_alias=True, include=include_keys)
        ret['id'] = str(self.id)
        if self.created_at is not None:
            ret['created_at'] = self.created_at.isoformat()
        if self.updated_at is not None:
            ret['updated_at'] = self.updated_at.isoformat()
        return ret

    def to_data(self) -> TagData:
        data = self.to_dict()
        if self.id is not None:
            data['id'] = int(self.id)
        else:
            if 'id' in data: del data['id']
            if 'created_at' in data: del data['created_at']
            if 'updated_at' in data: del data['updated_at']
        return TagData(**data)

# class TaskTag(BaseData):
#     __tablename__ = 'task_tag'
#     tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
#     task_id = Column(Integer, ForeignKey('task.id'), primary_key=True)