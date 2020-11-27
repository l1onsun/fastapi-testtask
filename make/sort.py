import sys, os
from contextlib import contextmanager

@contextmanager
def temp_open(path: str):
    with open(path, 'w') as file:
        yield file
    os.remove(path)

def update_reqs(old_reqs: str):
    with temp_open(old_reqs + '.save') as temp:
        lines = []
        with open(old_reqs, 'r') as old:
            for line in old:
                lines.append(line)
                temp.write(line)
        lines.sort()
        with open(old_reqs, 'w') as new:
            for line in lines:
                new.write(line)

if __name__ == "__main__":
    for req in sys.argv[1:]:
        assert os.path.isfile(req)
    for req in sys.argv[1:]:
        update_reqs(req)
        
