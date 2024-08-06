from fastapi import APIRouter, Cookie, Response, status
from fastapi.exceptions import HTTPException
from dishka.integrations.fastapi import FromDishka, inject

from src.domain.entities.user import User
from src.domain.exceptions.base import DomainException
from src.application.mediator.base import Mediator
from src.application.commands.user import (
    CreateUserCommand,
    DeleteUserCommand,
    LoginUserCommand,
    LogoutUserCommand,
)
from src.application.queries.user import GetUserByOidQuery, GetUserBySessionOidQuery
from src.presentation.api.user.schemas import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    LoginUserRequestSchema,
    LoginUserResponseSchema,
    GetUserByOidResponseSchema,
)
from src.presentation.api.schemas import ErrorSchema

router = APIRouter(tags=["User"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Endpoint returns a current user by session_oid from Cookie.",
    responses={
        status.HTTP_200_OK: {"model": GetUserByOidResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
    summary="Returns a current user.",
)
@inject
async def get_current_user(
    mediator: FromDishka[Mediator], session_oid: str = Cookie(include_in_schema=False)
):
    try:
        user: User = await mediator.handle_query(GetUserBySessionOidQuery(session_oid))
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": exception.message}
        )
    return GetUserByOidResponseSchema.from_entity(user)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Endpoint creates a new user.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateUserResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    summary="Creates a new user.",
)
@inject
async def create_user(
    schema: CreateUserRequestSchema, mediator: FromDishka[Mediator]
) -> CreateUserResponseSchema:
    user: User
    try:
        user, *_ = await mediator.handle_command(
            CreateUserCommand(schema.username, schema.email, schema.password)
        )
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    return CreateUserResponseSchema.from_entity(user)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    description="Endpoint logs in a user.",
    responses={
        status.HTTP_200_OK: {"model": LoginUserResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    summary="Logs in a user.",
)
@inject
async def login_user(
    response: Response, schema: LoginUserRequestSchema, mediator: FromDishka[Mediator]
) -> LoginUserResponseSchema:
    session_oid: str
    try:
        session_oid, *_ = await mediator.handle_command(
            LoginUserCommand(schema.username, schema.password)
        )
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    response.set_cookie("session_oid", session_oid, httponly=True)
    return LoginUserResponseSchema(session_oid=session_oid)


@router.delete(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Endpoint logs out a user by session_oid from Cookie.",
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    summary="Logs out a user.",
)
@inject
async def logout_user(
    response: Response,
    mediator: FromDishka[Mediator],
    session_oid: str = Cookie(include_in_schema=False),
) -> None:
    try:
        await mediator.handle_command(LogoutUserCommand(session_oid=session_oid))
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    response.delete_cookie("session_oid")


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Endpoint deletes a user by session_oid from Cookie.",
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
    summary="Deletes a user.",
)
@inject
async def delete_user(
    mediator: FromDishka[Mediator],
    session_oid: str = Cookie(include_in_schema=False),
) -> None:
    try:
        await mediator.handle_command(DeleteUserCommand(session_oid=session_oid))
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": exception.message}
        )


@router.get(
    "/{user_oid}",
    status_code=status.HTTP_200_OK,
    description="Endpoint returns a user by oid.",
    responses={
        status.HTTP_200_OK: {"model": GetUserByOidResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
    summary="Returns a user by oid.",
)
@inject
async def get_user_by_oid(
    user_oid: str, mediator: FromDishka[Mediator]
) -> GetUserByOidResponseSchema:
    try:
        user: User = await mediator.handle_query(GetUserByOidQuery(user_oid=user_oid))
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": exception.message}
        )
    return GetUserByOidResponseSchema.from_entity(user)
