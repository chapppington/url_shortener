from domain.entities.url import URLEntity
from infrastructure.database.models.url import URLModel


def convert_url_entity_to_model(entity: URLEntity) -> URLModel:
    return URLModel(
        id=entity.id,
        short_url=entity.short_url,
        long_url=entity.long_url,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def convert_url_model_to_entity(model: URLModel) -> URLEntity:
    return URLEntity(
        id=model.id,
        short_url=model.short_url,
        long_url=model.long_url,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
