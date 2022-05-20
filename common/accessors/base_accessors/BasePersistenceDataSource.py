from typing import Generic, List
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from common.accessors.base_accessors.BaseDataSource import Model, ModelData, BaseDataSource

class BasePersistenceDataSource(BaseDataSource[Model, ModelData], Generic[Model, ModelData]):

    def __init__(self, session):
        super(BaseDataSource, self).__init__()
        self._db_session = session

    def get_by_id(self, id: str) -> Model:
        model: Model = None

        try:
            stmt = select(self.dataModelType).where(self.dataModelType.id == id)
            result = self._db_session.execute(stmt).scalars().one()
            model = self.modelType.from_orm(result)
        except ValueError as e:
            print(f"Error: {e}")
        except NoResultFound:
            print("No result found for UUID {0}".format(str(id)))
        
        return model

    def get_all(self) -> List[Model]:
        models: List[self.modelType] = []

        try:
            stmt = select(self.dataModelType)
            for row in self._db_session.execute(stmt).scalars():
                models.append(self.modelType.from_orm(row))
        except ValueError as e:
            print(f"Error: {e}")
        return models

    def save(self, model: Model) -> Model:
        if model.id is not None:
            try:
                self.update_model(model)
            except Exception as e:
                raise e
        else:
            try:
                self.create(model.to_data())
            except Exception as e:
                raise e

    def delete(self, id) -> Model:
        stmt = select(self.dataModelType).where(self.dataModelType.id == id)
        result = self._db_session.execute(stmt).scalars().one()
        self._db_session.delete(result)
        self._db_session.commit()

    def update_model(self, data):
        stmt = select(self.dataModelType).where(self.dataModelType.id == data.id)
        result = self._db_session.execute(stmt).scalars().one()
        result.update(data)
        self._db_session.commit()
        pass

    def create(self, data: ModelData):
        self._db_session.add(data)
        self._db_session.commit()
        pass