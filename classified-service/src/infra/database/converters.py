from src.domain.entities.classified import Classified as ClassifiedEntity
from src.infra.database.models.classified import Classified as ClassifiedModel


def convert_classified_entity_to_classified_model(
    classified: ClassifiedEntity,
) -> ClassifiedModel:
    return ClassifiedModel(
        oid=classified.oid,
        title=classified.title,
        description=classified.description,
        price=classified.price,
        owner_oid=classified.owner_oid,
        is_active=classified.is_active,
    )


def convert_classified_model_to_classified_entity(
    classified: ClassifiedModel,
) -> ClassifiedEntity:
    return ClassifiedEntity(
        oid=classified.oid,
        title=classified.title,
        description=classified.description,
        price=classified.price,
        owner_oid=classified.owner_oid,
        is_active=classified.is_active,
    )
