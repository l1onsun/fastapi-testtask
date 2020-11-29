exec = """if [ "$( docker container inspect -f '{{.State.Running}}' $container_name )" == "true" ]; then ..."""

import sys
import subprocess

if __name__ == "__main__":
    container_name = sys.argv[1]
    subprocess.check_call(['docker', 'container', 'inspect', '-f', '{{.State.Running}}', container_name])