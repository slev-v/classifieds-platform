from fastapi import APIRouter, Cookie, Response, status
from fastapi.exceptions import HTTPException
from dishka.integrations.fastapi import FromDishka, inject

from src.domain.entities.classified import Classified
from src.domain.exceptions.base import DomainException
from src.application.mediator.base import Mediator
from src.application.commands.classified import CreateClassifiedCommand
from src.presentation.api.classified.schemas import (
    CreateClassifiedRequestSchema,
    CreateClassifiedResponseSchema,
)
from src.presentation.api.schemas import ErrorSchema

router = APIRouter(tags=["Classified"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Endpoint creates a new classified.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateClassifiedResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    summary="Creates a new classified.",
)
@inject
async def create_classified(
    schema: CreateClassifiedCommand, mediator: FromDishka[Mediator]
) -> CreateClassifiedResponseSchema:
    classified: Classified
    try:
        classified, *_ = await mediator.handle_command(
            CreateClassifiedCommand(
                schema.title, schema.description, schema.price, schema.owner_oid
            )
        )
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    return CreateClassifiedResponseSchema.from_entity(classified)
