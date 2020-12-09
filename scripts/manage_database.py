import fire
import subprocess


class ManageDatabase:
    def migrate(self):
        cmd = ["alembic", "upgrade", "head"]
        print(*cmd)
        subprocess.run(cmd)
        return self

    def seed_test(self):
        cmd = ["python", "-m", "tests.scripts.seed_database"]
        print(*cmd)
        subprocess.run(cmd)
        return self

    def __call__(self):
        pass


if __name__ == '__main__':
    fire.Fire(ManageDatabase)
