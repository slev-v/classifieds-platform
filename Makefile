DC = docker compose
LOGS = docker logs
USER_COMPOSE = user-service/docker_compose
USER_APP = ${USER_COMPOSE}/app.yaml
USER_APP_DEV = ${USER_COMPOSE}/app.dev.yaml
USER_POSTGRES = ${USER_COMPOSE}/postgres.yaml
USER_REDIS = ${USER_COMPOSE}/redis.yaml
USER_MIGRATE = ${USER_COMPOSE}/migrate.yaml
USER_ENV = --env-file user-service/.env

KAFKA = docker_compose/kafka.yaml

.PHONY: user-dev
user-dev:
	${DC} -p user-service -f ${USER_APP_DEV} -f ${KAFKA} ${USER_ENV} up --build -d

.PHONY: user-storages
user-storages:
	${DC} -p user-service -f ${USER_REDIS} -f ${USER_POSTGRES} ${USER_ENV} up -d --build

.PHONY: user-storages-down
user-storages-down:
	${DC} -p user-service -f ${USER_REDIS} -f ${USER_POSTGRES} ${USER_ENV} down

.PHONY: user-down-dev
user-down-dev:
	${DC} -p user-service -f ${USER_APP_DEV} -f ${KAFKA} ${USER_ENV} down

.PHONY: user-dev-logs
user-dev-logs:
	${LOGS} -f user-service-main-app-1 -f

.PHONY: user-down
user-down:
	${DC} -p user-service -f ${USER_APP} -f ${USER_APP_DEV} -f ${KAFKA} -f ${USER_REDIS} -f ${USER_POSTGRES} ${USER_ENV} down

.PHONY: user-migrate
user-migrate:
	${DC} -p user-service -f ${USER_MIGRATE} ${USER_ENV} up --build
	${DC} -p user-service -f ${USER_MIGRATE} ${USER_ENV} down
