help:
	@echo "usage:"
	@echo "> make [docker] [command=help] [ENV=.env] [PYTHON=python] [REQ=dev]"
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

ENV=.env
PYTHON=python

DOCKER_NAME=docker-name

scripts = app/* main/* database/* environ/* make/* Dockerfile Makefile

docker-check:
	$(eval DOCKER := True)

docker-build: scripts
	docker build -t {}

install:
	$(PYTHON) -m make.install requirements.txt
install-dev:
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
