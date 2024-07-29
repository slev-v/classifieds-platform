from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from dishka.integrations.fastapi import FromDishka, inject

from src.domain.exceptions.base import DomainException
from src.application.mediator.base import Mediator
from src.application.commands.user import CreateUserCommand, DeleteUserCommand
from src.application.queries.user import GetUserByOidQuery
from src.presentation.api.user.schemas import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    GetUserByOidResponseSchema,
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
            CreateUserCommand(schema.username, schema.email, schema.password)
        )
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    return CreateUserResponseSchema.from_entity(user)


@router.get(
    "/{user_oid}",
    status_code=status.HTTP_200_OK,
    description="Endpoint returns a user by oid.",
    responses={
        status.HTTP_200_OK: {"model": GetUserByOidResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
@inject
async def get_user_by_oid(
    user_oid: str, mediator: FromDishka[Mediator]
) -> GetUserByOidResponseSchema:
    try:
        user = await mediator.handle_query(GetUserByOidQuery(user_oid=user_oid))
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": exception.message}
        )
    return GetUserByOidResponseSchema.from_entity(user)


@router.delete(
    "/{user_oid}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Endpoint deletes a user.",
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
@inject
async def delete_user(user_oid: str, mediator: FromDishka[Mediator]) -> None:
    try:
        await mediator.handle_command(DeleteUserCommand(user_oid=user_oid))
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": exception.message}
        )
