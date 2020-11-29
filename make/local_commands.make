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