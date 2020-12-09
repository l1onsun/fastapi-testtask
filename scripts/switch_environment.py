#!/usr/bin/env python
import os
import fire

_env_destination = ".env"

_env_development_local = "config/envs/.env.development"
_env_development_docker = "config/envs/.env.development.docker"


class Switch:
    def __init__(self, path=None):
        if path is not None:
            self._switch(path)
            exit()
        self._dev_or_prod = None
        self._local_or_docker = None

    def _switch(self, path):
        if os.path.islink(_env_destination):
            os.remove(_env_destination)
        os.symlink(path, _env_destination)
        print(f"Switching to environment: ({path})")

    def development(self):
        assert self._dev_or_prod is None, "input conflict"
        self._dev_or_prod = "dev"
        return self

    def docker(self):
        assert self._local_or_docker is None, "input conflict"
        self._local_or_docker = "docker"
        return self

    def production(self):
        assert self._dev_or_prod is None, "input conflict"
        self._dev_or_prod = "prod"
        return self

    def local(self):
        assert self._local_or_docker in None, "input conflict"
        self._local_or_docker = "local"
        return self

    def __call__(self):
        if self._local_or_docker is None:
            if self._dev_or_prod is None:
                return print(f"current environment: {os.path.realpath(_env_destination)}")
            self._local_or_docker = "local"
        if self._dev_or_prod == "dev":
            if self._local_or_docker == "local":
                self._switch(_env_development_local)
            elif self._local_or_docker == "docker":
                self._switch(_env_development_docker)
            else:
                raise ValueError("unknown input")
        elif self._dev_or_prod == "prod":
            raise NotImplementedError("Switching to production environment not implemented yet")
        else:
            raise ValueError("should choose: development or production")


class production():
    def __init__(self):
        raise NotImplementedError("Switching to production environment not implemented yet")


if __name__ == '__main__':
    fire.Fire(Switch())
