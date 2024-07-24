from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from dishka.integrations.fastapi import FromDishka, inject

from src.domain.exceptions.base import ApplicationException
from src.application.mediator.base import Mediator
from src.application.commands.user import CreateUserCommand
from src.presentation.api.user.schemas import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)
from src.presentation.api.schemas import ErrorSchema

router = APIRouter(tags=["User"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Endpoint creates a new user.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateUserResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
@inject
async def create_user(
    schema: CreateUserRequestSchema, mediator: FromDishka[Mediator]
) -> CreateUserResponseSchema:
    try:
        user, *_ = await mediator.handle_command(
            CreateUserCommand(schema.username, schema.email)
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    return CreateUserResponseSchema.from_entity(user)
