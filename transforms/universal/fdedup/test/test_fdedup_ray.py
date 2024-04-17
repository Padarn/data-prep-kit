# (C) Copyright IBM Corp. 2024.
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import os

from data_processing.test_support.ray import AbstractTransformLauncherTest
from fdedup_transform import FdedupTableTransformConfiguration


class TestRayBlocklistTransform(AbstractTransformLauncherTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[tuple]:
        basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test-data"))
        config = {
            # When running in ray, our Runtime's get_transform_config() method  will load the domains using
            # the orchestrator's DataAccess/Factory. So we don't need to provide the bl_local_config configuration.
            # columns used
            "doc_column": "contents",
            "id_column": "int_id_column",
            "cluster_column": "cluster",
            # infrastructure
            "bucket_cpu": 0.5,
            "doc_cpu": 0.5,
            "mhash_cpu": 0.5,
            "num_doc_actors": 2,
            "num_bucket_actors": 1,
            "num_minhash_actors": 1,
            "num_preprocessors": 2,
            "num_permutations": 64,
            # fuzzy parameters
            "threshold": 0.8,
            "shingles_size": 5,
            "delimiters": " ",
            # Random delay between reads
            "random_delay_limit": 5,
            # snapshotting
            "snapshot_delay": 1,
            "use_doc_snapshot": False,
            "use_bucket_snapshot": False,
        }
        fixtures = [(FdedupTableTransformConfiguration(), config, basedir + "/input", basedir + "/expected")]
        return fixtures