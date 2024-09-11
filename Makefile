DC = docker compose
LOGS = docker logs

USER_COMPOSE = user-service/docker_compose
USER_APP = ${USER_COMPOSE}/app.yaml
USER_APP_DEV = ${USER_COMPOSE}/app.dev.yaml
USER_POSTGRES = ${USER_COMPOSE}/postgres.yaml
USER_REDIS = ${USER_COMPOSE}/redis.yaml
USER_MIGRATE = ${USER_COMPOSE}/migrate.yaml
USER_ENV = --env-file user-service/.env

CLASSIFIED_COMPOSE = classified-service/docker_compose
CLASSIFIED_APP = ${CLASSIFIED_COMPOSE}/app.yaml
CLASSIFIED_APP_DEV = ${CLASSIFIED_COMPOSE}/app.dev.yaml
CLASSIFIED_POSTGRES = ${CLASSIFIED_COMPOSE}/postgres.yaml
CLASSIFIED_MIGRATE = ${CLASSIFIED_COMPOSE}/migrate.yaml
CLASSIFIED_ENV = --env-file classified-service/.env

KAFKA = docker_compose/kafka.yaml

.PHONY: kafka
kafka:
	${DC} -p kafka-service -f ${KAFKA} up -d

.PHONY: kafka-down
kafka-down:
	${DC} -p kafka-service -f ${KAFKA} down


.PHONY: user-dev
user-dev:
	${DC} -p user-service -f ${USER_APP_DEV} ${USER_ENV} up --build -d

.PHONY: user-storages
user-storages:
	${DC} -p user-service -f ${USER_REDIS} -f ${USER_POSTGRES} ${USER_ENV} up -d --build

.PHONY: user-storages-down
user-storages-down:
	${DC} -p user-service -f ${USER_REDIS} -f ${USER_POSTGRES} ${USER_ENV} down

.PHONY: user-down-dev
user-down-dev:
	${DC} -p user-service -f ${USER_APP_DEV} ${USER_ENV} down

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


.PHONY: classified-dev
classified-dev:
	${DC} -p classified-service -f ${CLASSIFIED_APP_DEV} ${CLASSIFIED_ENV} up --build -d

.PHONY: classified-storages
classified-storages:
	${DC} -p classified-service -f ${CLASSIFIED_POSTGRES} ${CLASSIFIED_ENV} up -d --build

.PHONY: classified-storages-down
classified-storages-down:
	${DC} -p classified-service -f ${CLASSIFIED_POSTGRES} ${CLASSIFIED_ENV} down

.PHONY: classified-down-dev
classified-down-dev:
	${DC} -p classified-service -f ${CLASSIFIED_APP_DEV} ${CLASSIFIED_ENV} down

.PHONY: classified-dev-logs
classified-dev-logs:
	${LOGS} -f classified-service-main-app-1 -f

.PHONY: classified-down
classified-down:
	${DC} -p classified-service -f ${CLASSIFIED_APP} -f ${CLASSIFIED_APP_DEV} -f ${CLASSIFIED_POSTGRES} ${CLASSIFIED_ENV} down

.PHONY: classified-migrate
classified-migrate:
	${DC} -p classified-service -f ${CLASSIFIED_MIGRATE} ${CLASSIFIED_ENV} up --build
	${DC} -p classified-service -f ${CLASSIFIED_MIGRATE} ${CLASSIFIED_ENV} down
