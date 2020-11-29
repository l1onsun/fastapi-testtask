.PHONY: docker-build docker-up docker-run

ENV=.env
PYTHON=python
DOCKER_IMAGE_NAME= testtask-image
DOCKER_CONTAINER_NAME= testtask-container
# VENV=notice

docker_build_depends =  $(shell find app database config make -name '*.py') Dockerfile Makefile

#include $(ENV)
#export

docker:
	@echo "Running $(MAKECMDGOALS) in docker"


make/.docker-build.timestamp: $(docker_build_depends)
	@echo "Running target docker-build..."
	docker build -t ${DOCKER_IMAGE_NAME} .
	@touch make/.docker-build.timestamp

docker-build: make/.docker-build.timestamp
	echo "What is $?"

docker-up: docker-build
	@echo "Running target $@..."
	# $(PYTHON) -m make.docker_up

docker-install:
	@echo "Running target $@..."
	docker exec ${DOCKER_IMAGE_NAME} make install VENV=ignore

docker-install-dev:
	@echo "Running target docker-install-dev"
	docker exec ${DOCKER_IMAGE_NAME} make install-dev VENV=ignore

docker-run: docker-build docker-up
	@echo "Running target $@..."
	# docker exec ${DOCKER_IMAGE_NAME} make run

docker-run-test: docker-build docker-up
	@echo "Running target $@..."
	docker exec ${DOCKER_IMAGE_NAME} make run-test VENV=ignore

docker-test-copy: tests/*
