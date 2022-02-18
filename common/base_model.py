from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):

    """
    Overloads Pydantic BaseModel and forces all objects to use orm_mode and be populated by field name and alias
    """
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class BaseRequestModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name = True