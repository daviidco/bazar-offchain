from datetime import datetime

from flask_restx import abort
from sqlalchemy.orm import Session

from src.domain.entities.company_entity import CompanyEntity, CompanyNewEntity, CompaniesPaginationEntity
from src.domain.ports.company_interface import ICompanyRepository
from src.infrastructure.adapters.database.models import User
from src.infrastructure.adapters.database.models.company import Company
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


class CompanyRepository(ICompanyRepository):

    def __init__(self, adapter_db, storage_repository):
        self.engine = adapter_db.engine
        self.session = Session(adapter_db.engine)
        self.__storage_repository = storage_repository

    def new_company(self, jwt_entity, company_entity: CompanyNewEntity,
                    objects_cloud: list) -> CompanyEntity:
        user = self.session.query(User).filter_by(uuid=company_entity.uuid_user).first()
        if user is None:
            user_to_save = User(
                uuid=company_entity.uuid_user,
                rol="seller"  # jwt_entity.rol,
            )
            self.session.add(user_to_save)
            self.session.commit()

        user_id = user.id if user is not None else user_to_save.id
        company = self.session.query(Company).filter_by(user_id=user_id).first()

        if company is None:
            object_to_save = Company(
                company_name=company_entity.company_name,
                address=company_entity.address,
                chamber_commerce=company_entity.chamber_commerce,
                legal_representative=company_entity.legal_representative,
                operative_years=company_entity.operative_years,
                country=company_entity.country,
                city=company_entity.city,
                user_id=user_id
            )

            with Session(self.engine) as session_trans:
                session_trans.begin()
                try:

                    session_trans.add(object_to_save)
                    if objects_cloud:
                        path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))
                        # prefix = f"{jwt_entity.rol}/{company_entity.uuid_user}/{path_datetime}"
                        prefix = f"seller/{company_entity.uuid_user}/{path_datetime}"

                        for o in objects_cloud:
                            key = f"{prefix}/{o.filename}"
                            self.__storage_repository.put_object(body=o, key=key, content_type=o.content_type)
                except:
                    session_trans.rollback()
                    e = api_error('CompanySavingError')
                    abort(code=e.status_code, message=e.message, error=e.error)
                else:
                    session_trans.commit()
                    return CompanyEntity.from_orm(object_to_save)

        else:
            e = api_error('CompanyExistingError')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_company_by_uuid(self, uuid: str) -> CompanyEntity:
        try:
            found_object = self.session.query(Company).filter_by(uuid=uuid).first()
            found_object = CompanyEntity.from_orm(found_object) if found_object is not None else None
            return found_object

        except Exception as e:
            raise Exception(f'Error: {str(e)}')

    def get_companies_count(self) -> int:
        count = self.session.query(Company).count()
        count = count if count is not None else 0
        return count

    def get_all_companies(self, limit: int, offset: int) -> CompaniesPaginationEntity:
        total = self.get_companies_count()
        list_objects = self.session.query(Company).offset(offset).limit(limit).all()
        return CompaniesPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects)
