from datetime import datetime

from flask_restx import abort
from sqlalchemy.orm import Session

from src.domain.entities.company_entity import CompanyEntity, CompanyNewEntity, CompaniesPaginationEntity
from src.domain.ports.company_interface import ICompanyRepository
from src.infrastructure.adapters.database.models import User
from src.infrastructure.adapters.database.models.company import Company, ProfileImage
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


class CompanyRepository(ICompanyRepository):

    def __init__(self, adapter_db, storage_repository):
        self.engine = adapter_db.engine
        self.session = Session(adapter_db.engine)
        self.__storage_repository = storage_repository

    @staticmethod
    def build_urls_profile_images(profile_image):
        # Urls profile images
        profile_images = []
        if profile_image is not None:
            if profile_image.image_url is not None:
                idx_last_dot = profile_image.image_url.rindex('.')
                format_file = profile_image.image_url[idx_last_dot:]
                url_base = profile_image.image_url[:idx_last_dot - 2]
                profile_images.append(f"{url_base}-s{format_file}")
                profile_images.append(f"{url_base}-m{format_file}")
                profile_images.append(f"{url_base}-b{format_file}")
        return profile_images

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
            profile_image = self.session.query(ProfileImage).filter_by(image_url=company_entity.profile_image).first()
            profile_image_id = profile_image.id if profile_image is not None else None

            object_to_save = Company(
                company_name=company_entity.company_name,
                address=company_entity.address,
                chamber_commerce=company_entity.chamber_commerce,
                legal_representative=company_entity.legal_representative,
                operative_years=company_entity.operative_years,
                country=company_entity.country,
                city=company_entity.city,
                user_id=user_id,
                profile_image_id=profile_image_id
            )

            with Session(self.engine) as session_trans:
                session_trans.begin()
                try:

                    session_trans.add(object_to_save)

                    list_profile_images = self.build_urls_profile_images(profile_image)

                    # Save in cloud
                    if objects_cloud:
                        path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))
                        # prefix = f"{jwt_entity.rol}/{company_entity.uuid_user}/{path_datetime}"
                        prefix = f"seller/{company_entity.uuid_user}/documents_company/{path_datetime}"

                        for o in objects_cloud:
                            key = f"{prefix}/{o.filename}"
                            self.__storage_repository.put_object(body=o, key=key, content_type=o.content_type)
                except Exception as e:
                    session_trans.rollback()
                    e = api_error('CompanySavingError')
                    abort(code=e.status_code, message=e.message, error=e.error)
                else:
                    session_trans.commit()

                    res_company = CompanyEntity.from_orm(object_to_save)
                    res_company.profile_images = list_profile_images
                    session_trans.close()

                    return res_company

        else:
            e = api_error('CompanyExistingError')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_company_by_uuid(self, uuid: str) -> CompanyEntity:
        try:
            found_object = self.session.query(Company).filter_by(uuid=uuid).first()
            result_object = CompanyEntity.from_orm(found_object) if found_object is not None else None
            profile_image = self.session.query(ProfileImage).filter_by(id=found_object.profile_image_id).first()
            list_profile_images = self.build_urls_profile_images(profile_image)
            result_object.profile_images = list_profile_images
            return result_object

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
