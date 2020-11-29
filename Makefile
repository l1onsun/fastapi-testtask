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

ifeq (docker ,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  DOCKER_COMMANDS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(DOCKER_COMMANDS):;@:)
endif

docker: #docker-up
	@echo" docker exec $(DOCKER_CONTAINER_NAME) $(DOCKER_COMMANDS) "

run-gunicorn: #install
	gunicorn app.main:app -k uvicorn.workers.UvicornWorker -c config/gunicorn_conf.py

test:
	PYTHONPATH=. ENV=config/envs/dev.env pytest -s tests

install:
	@echo "Running target install..."
	$(PYTHON) -m make.install requirements.txt
install-dev:
	@echo "Running target install-dev..."
	$(PYTHON) -m make.install requirements_dev.txt

docker-install:
docker-install-dev:

sort-reqs:
	$(PYTHON) -m make.sort requirements.txt
	$(PYTHON) -m make.sort requirements_dev.txt

upgrade:
	$(PYTHON) -m make.install requirements.txt --upgrade
upgrade-dev:
	$(PYTHON) -m make.install requirements_dev.txt --upgrade

# include make/docker_commands.make
# include make/local_commands.make