from typing import Optional
from common.base_model import BaseModel
from common.base_data import BaseData
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Dict, List
from datetime import datetime
from common.models.tag import Tag


class TaskData(BaseData):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    is_done = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    tags = relationship('TagData', secondary="task_tag", backref="tasks")

    def update(self, task):
        self.title = task.title
        self.description = task.description
        self.is_done = task.is_done

class Task(BaseModel):
    id: Optional[int]
    title: str
    description: str
    is_done: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    tags: Optional[List[Tag]]

    def to_dict(self) -> Dict:
        include_keys = {
            "title": ...,
            "description": ...,
            "is_done": ...,
            "created_at": ...,
            "updated_at": ...
        }
        ret = self.dict(by_alias=True, include=include_keys)
        ret['id'] = str(self.id)
        if self.created_at is not None:
            ret['created_at'] = self.created_at.isoformat()
        if self.updated_at is not None:
            ret['updated_at'] = self.updated_at.isoformat()
        if self.tags is not None:
            ret['tags'] = list(map(lambda tag: tag.to_dict(), self.tags))
        return ret

    def to_data(self) -> TaskData:
        data = self.to_dict()
        if self.id is not None:
            data['id'] = int(self.id)
        else:
            if 'id' in data: del data['id']
            if 'created_at' in data: del data['created_at']
            if 'updated_at' in data: del data['updated_at']
        return TaskData(**data)