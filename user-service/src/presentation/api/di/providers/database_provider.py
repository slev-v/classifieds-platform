from dishka import provide, Provider, Scope, make_async_container


class DatabaseProvider(Provider):
    pass
    # @provide(scope=Scope.APP)
    # def hasher_password(self) -> HasherPassword:
    #     return HasherPasswordImp()
    #
    # @provide(scope=Scope.APP)
    # def user_service(self, hasher_password: HasherPassword) -> UserService:
    #     return UserServiceImp(hasher_password)
