from config.database_env import database_env
import asyncio

from database import orm
from database.rod import DatabaseManager
from typing import List, Dict

import uuid


def id_from_tag(tag: str):
    return uuid.uuid5(uuid.NAMESPACE_DNS, tag)


class TestData:
    companies: Dict[str, orm.Company] = {
        'foo': orm.Company(name="Foo Company"),
        'bar': orm.Company(name="Bar Company"),
        'baz': orm.Company(name="Baz Company"),
    }

    users: Dict[str, orm.User] = {
        "master": orm.User(name="Foo Master", role=orm.GlobalRoleEnum.owner, company=companies['foo']),
        "bar_boss": orm.User(name="Bar Boss", role=orm.GlobalRoleEnum.owner, company=companies['bar']),
        "baz_leader": orm.User(name="Leader of Baz", role=orm.GlobalRoleEnum.owner, company=companies['baz']),

        "user_one": orm.User(name="User One", role=orm.GlobalRoleEnum.employee, company=companies['foo']),
        "user_two": orm.User(name="User Two", role=orm.GlobalRoleEnum.employee, company=companies['foo']),
        "user_three": orm.User(name="User Three", role=orm.GlobalRoleEnum.employee, company=companies['bar']),
        "user_four": orm.User(name="User Four", role=orm.GlobalRoleEnum.employee, company=companies['baz']),
        "user_five": orm.User(name="User Five", role=orm.GlobalRoleEnum.employee, company=companies['baz']),
        "user_six": orm.User(name="User Six", role=orm.GlobalRoleEnum.employee, company=companies['baz']),
        "user_seven": orm.User(name="User Seven", role=orm.GlobalRoleEnum.employee, company=companies['baz']),
    }

    projects: Dict[str, orm.Project] = {
        "project_alpha": orm.Project(name="Project A"),
        "project_beta": orm.Project(name="Project B"),
        "project_gamma": orm.Project(name="Project G"),
        "project_delta": orm.Project(name="Project D"),
    }

    memberships: List[Dict] = [
        dict(user_tag="master", project_tag="project_alpha", role=orm.ProjectRoleEnum.admin),
        dict(user_tag="master", project_tag="project_beta", role=orm.ProjectRoleEnum.admin),
        dict(user_tag="bar_boss", project_tag="project_beta", role=orm.ProjectRoleEnum.admin),

        dict(user_tag="user_one", project_tag="project_beta", role=orm.ProjectRoleEnum.manager),
    ]


def gen_persistent_ids():
    for company_tag, company in TestData.companies.items():
        company.id = id_from_tag(company_tag)
    for user_tag, user in TestData.users.items():
        user.id = id_from_tag(user_tag)
    for project_tag, project in TestData.projects.items():
        project.id = id_from_tag(project_tag)


async def insert_test_data(db_manager: DatabaseManager):
    async with db_manager.session(write=True) as session:
        for company_tag, company in TestData.companies.items():
            company.id = id_from_tag(company_tag)
            session.add(company)
        for user_tag, user in TestData.users.items():
            user.id = id_from_tag(user_tag)
            session.add(user)
        for project_tag, project in TestData.projects.items():
            project.id = id_from_tag(project_tag)
            session.add(project)
        await session.commit()

        for tags in TestData.memberships:
            user_id = id_from_tag(tags['user_tag'])
            project_id = id_from_tag(tags['project_tag'])
            role = tags['role']
            membership = orm.Membership(user_id=user_id, project_id=project_id, role=role)
            session.add(membership)
        await session.commit()


async def drop_and_create(db_manager: DatabaseManager):
    assert database_env.allow_drop_tables, \
        "Droping tables is not allowed (env var ALLOW_DROP_TABLES is False)"
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(orm.Base.metadata.drop_all)
        await conn.run_sync(orm.Base.metadata.create_all)


async def seed_database(db_manager: DatabaseManager):
    await drop_and_create(db_manager)
    await insert_test_data(db_manager)


if __name__ == "__main__":
    asyncio.run(seed_database(DatabaseManager()))
