from .test_data import test_managers, TestManager, test_managers_list
from tests.test_case_helpers import test_case, get_uuid_set, get_test_uuid_set

@test_case('/managers/list')
def check_managers_list(json_managers_list):
    assert len(json_managers_list) == len(test_managers_list)

    json_managers_uuids = get_uuid_set(json_managers_list)
    test_managers_uuids = get_test_uuid_set(test_managers_list)

    assert json_managers_uuids == test_managers_uuids, "recived and test data are not equal"
    return True


@test_case(f'/managers/{test_managers.FooOwner.id}')
def check_foo_owner(json_managers_list):
    assert len(json_managers_list) == 3

    json_managers_uuids = get_uuid_set(json_managers_list)
    test_managers_uuids = get_test_uuid_set(
        [test_managers.One, test_managers.Two, test_managers.Three])

    assert json_managers_uuids == test_managers_uuids, "recived and expected data are not equal"

    return True
