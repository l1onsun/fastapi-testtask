from database import orm
from .test_models import *

_g_owner = orm.GlobalRoleEnum.owner
_g_employee = orm.GlobalRoleEnum.employee
_p_admin = orm.ProjectRoleEnum.admin
_p_manager = orm.ProjectRoleEnum.manager


class TestManagers:
    FooOwner = TestManager(name="Foo Owner")
    BarOwner = TestManager(name="Bar Owner")
    BazOwner = TestManager(name=" Baz Owner")

    One = TestManager(name="User One")
    Two = TestManager(name="User Two")
    Three = TestManager(name="User Three")
    Four = TestManager(name="User Four")
    Five = TestManager(name="User Five")
    Six = TestManager(name="User Six")
    Seven = TestManager(name="User Seven")
    Eight = TestManager(name="User Eight")
    Nine = TestManager(name="User Nine")
    Ten = TestManager(name="User Ten")


test_managers = _m = TestManagers()


class TestProjects:
    Alpha = TestProject(name="Project Alpha")
    Beta = TestProject(name="Project Beta")
    Gamma = TestProject(name="Project Gamma")
    Delta = TestProject(name="Project Delta")
    Epsilon = TestProject(name="Project Epsilon")
    Zeta = TestProject(name="Project Zeta")


test_projects = _p = TestProjects()


class TestCompanies:
    Foo = TestCompany(
        name="Foo Company",
        managers=[
            (_m.FooOwner, _g_owner),
            (_m.One, _g_employee),
            (_m.Two, _g_employee),
            (_m.Three, _g_employee)
        ],
        projects=[
            (_p.Alpha, [
                (_m.FooOwner, _p_admin),
                (_m.One, _p_manager),
                (_m.Two, _p_manager),
            ]),
            (_p.Beta, [
                (_m.One, _p_admin),
                (_m.Three, _p_manager),
            ]),
            (_p.Gamma, [
                (_m.Two, _p_admin),
                (_m.Five, _p_manager),
                (_m.Six, _p_manager)
            ])
        ])

    Bar = TestCompany(
        name="Bar Company",
        managers=[
            (_m.BarOwner, _g_owner),
            (_m.Four, _g_owner),
            (_m.Five, _g_employee),
            (_m.Six, _g_employee),
            (_m.Seven, _g_employee),
        ],
        projects=[
            (_p.Delta, [
                (_m.BarOwner, _p_admin),
                (_m.Five, _p_admin),
                (_m.Seven, _p_manager),
            ]),
        ])

    Baz = TestCompany(name="Baz Company",
                      managers=[
                          (_m.BazOwner, _g_owner),
                          (_m.Eight, _g_employee),
                          (_m.Nine, _g_employee),
                          (_m.Ten, _g_employee),
                      ],
                      projects=[
                          (_p.Epsilon, [
                              (_m.BazOwner, _p_admin),
                              (_m.Eight, _p_admin),
                              (_m.Six, _p_manager),
                              (_m.Seven, _p_manager),
                          ]),
                          (_p.Zeta, [
                              (_m.BazOwner, _p_admin),
                              (_m.Nine, _p_admin),
                              (_m.Six, _p_manager),
                              (_m.Seven, _p_manager),
                              (_m.Ten, _p_manager),
                          ])
                      ])


test_companies = TestCompanies()

test_companies_list: List[TestCompany] = TestCompany.list
test_managers_list: List[TestManager] = TestManager.list
test_projects_list: List[TestProject] = TestProject.list

