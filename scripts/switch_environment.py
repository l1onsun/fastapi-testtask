#!/usr/bin/env python
import shutil
import fire

def development():
    print("Switch to development environment")

def production():
    print("Switch to production environment (NotImplemented)")
    raise NotImplemented

def test():
    print("test")

if __name__ == '__main__':
    fire.Fire()