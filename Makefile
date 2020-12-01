help:
	@echo "usage:"
	@echo "> make [command=help] [ENV=.env] [PYTHON=python]"
	@echo ""
	@echo "commands:"
	@echo "    help			- show this help"
	@echo ""
	@echo "    install-vital		- install pip packages from requirments.txt"
	@echo "    install-dev		- install pip packages from requirments_dev.txt"
	@echo "    install-all    		- install all pip requirements"
	@echo ""
	@echo "    build-docker		- build docker container"
	@echo ""
	@echo "    run-local [ENV=.env]	- run local"
	@echo "    run-docker [ENV=.env]	- run in docker container"
	@echo "    run [ENV=.env]	    	- run local or docker based on ENV file"
	@echo ""
	@echo "    test-local [ENV=.env]	- test local"
	@echo "    test-docker [ENV=.env]	- test in docker container"
	@echo "    test [ENV=.env] 		- test local or docker based on ENV file"
	@echo ""
	@echo "    sort-requirements		- sort lines in requirements"

PYTHON=python
ENV=config/envs/default.env
USE_ENV=config/envs/default.env

ifeq (docker ,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  DOCKER_COMMANDS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(DOCKER_COMMANDS):;@:)
endif


docker-build:
	docker-compose --env-file config/envs/compose.default.env build
docker-build-test:
	docker-compose --env-file config/envs/compose.test.env build

docker-up:
	docker-compose --env-file config/envs/compose.default.env up
docker-up-test:
	docker-compose --env-file config/envs/compose.test.env up

docker: #docker-up
	@echo" docker exec $(DOCKER_CONTAINER_NAME) $(DOCKER_COMMANDS) "

run-gunicorn: #install
	gunicorn app.main:app -k uvicorn.workers.UvicornWorker -c config/gunicorn_conf.py

run-tests-unit:
	PYTHONPATH=. ENV=config/envs/test.env pytest tests/unit

run-tests-integration:
	PYTHONPATH=. ENV=config/envs/test.env pytest tests/integration

run-tests-docker:
	PYTHONPATH=. ENV=config/envs/compose.test.env pytest tests/docker

install:
	@echo "Running target install..."
	$(PYTHON) -m make.install requirements.txt
install-test:
	@echo "Running target install-test..."
	$(PYTHON) -m make.install requirements_test.txt

docker-install:
docker-install-test:

alembic-upgrade:
	alembic upgrade head

seed-database:
	python -m tests.seed_database

sort-reqs:
	$(PYTHON) -m make.sort requirements.txt
	$(PYTHON) -m make.sort requirements_test.txt

upgrade:
	$(PYTHON) -m make.install requirements.txt --upgrade
upgrade-test:
	$(PYTHON) -m make.install requirements_test.txt --upgrade

# include make/docker_commands.make
# include make/local_commands.make