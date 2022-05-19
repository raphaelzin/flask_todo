from typing import Generic
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from common.accessors.BaseDataSource import Model, ModelData, BaseDataSource

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

    def save(self, model: Model) -> Model:
        if model.id is not None:
            try:
                self.update_task(model)
            except Exception as e:
                raise e
        else:
            # create
            try:
                self.create_task(model.to_data())
            except Exception as e:
                raise e

    def delete(self, model: Model) -> Model:
        self.cache.delete(model.id)

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