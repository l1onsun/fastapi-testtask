import uuid

class TestCase():
    def __init__(self, url, test_func):
        self.url = url
        self.test = test_func


test_cases = []


def test_case(url: str):
    def decorator(test_func):
        test_cases.append(TestCase(url, test_func))
        return test_func

    return decorator


def get_uuid_set(json_managers_list):
    json_managers_uuids = set()

    for jmanager in json_managers_list:
        id = uuid.UUID(jmanager['id'])
        assert id not in json_managers_uuids, f"two managers with same id: {id}"
        json_managers_uuids.add(id)

    return json_managers_uuids


def get_test_uuid_set(test_managers_list):
    test_managers_uuids = set()

    for test_man in test_managers_list:
        assert test_man.id not in test_managers_uuids, \
            f"invalid test data: two managers with same id: {test_man.id} "
        test_managers_uuids.add(test_man.id)

    return test_managers_uuids
