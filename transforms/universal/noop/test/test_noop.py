from typing import Tuple

import pyarrow as pa
from data_processing_test.transform.transform_test import AbstractTransformTest
from noop_transform import NOOPTransform


# # Every class sub-classing AbstractTransformTest must define this function this way.
# # It is the hook called by pytest that we used to install the test fixtures for the
# # specific instance of our test.
# def pytest_generate_tests(metafunc):
#     """
#     Called by pytest to install the fixtures for the test class in this file.
#     This will generally not change for all tests extending AbstractTransformTest test class.
#     :param metafunc:
#     :return:
#     """
#     test_instance = metafunc.cls()  # Create the instance of the class being tested.
#     test_instance.install_fixtures(metafunc)  # Use it to install the fixtures


table = pa.Table.from_pydict({"name": pa.array(["Tom"]), "age": pa.array([23])})
expected_table = table  # We're a noop after all.
expected_metadata_list = [{"nfiles": 1, "nrows": 1}, {}]  # transform() result  # flush() result


class TestNOOPTransform(AbstractTransformTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[Tuple]:
        fixtures = [
            (NOOPTransform({"sleep": 0}), [table], [expected_table], expected_metadata_list),
            (NOOPTransform({"sleep": 0}), [table], [expected_table], expected_metadata_list),
        ]
        return fixtures
