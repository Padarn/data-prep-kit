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
import sys
from ast import Param

from data_processing.runtime.pure_python import PythonTransformLauncher
from data_processing.utils import ParamsUtils
from signature_calc_transform_python import (
    SignatureCalculationPythonTransformConfiguration,
)


# create parameters
input_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test-data", "input"))
output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output", "test_scdata"))
local_conf = {"input_folder": input_folder, "output_folder": output_folder}
code_location = {"github": "github", "commit_hash": "12345", "path": "path"}
s3_creds = {
    "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
    "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "url": os.getenv("AWS_ENDPOINT_URL"),
}
s3_config = {
    "input_folder": "s3://cos-optimal-llm-pile/spark_test/fuzzy_dedup_test_data/",
    "output_folder": "s3://cos-optimal-llm-pile/spark_test/fuzzy_dedup_test_output_data/s3_test_3/",
}

params = {
    # Data access. Only required parameters are specified
    "data_local_config": ParamsUtils.convert_to_ast(local_conf),
    "scdata_local_config": ParamsUtils.convert_to_ast(local_conf),
    # execution info
    "runtime_pipeline_id": "pipeline_id",
    "runtime_job_id": "job_id",
    "runtime_code_location": ParamsUtils.convert_to_ast(code_location),
    "minhash_num_permutations": 112,
    "minhash_num_bands": 14,
    "minhash_num_segments": 2,
    # "scdata_s3_cred": ParamsUtils.convert_to_ast(s3_creds),
    # "scdata_s3_config": ParamsUtils.convert_to_ast(s3_config),
}


if __name__ == "__main__":
    # Set the simulated command line args
    sys.argv = ParamsUtils.dict_to_req(d=params)
    print(sys.argv)

    sys.argv.append("--data_s3_cred")
    sys.argv.append(ParamsUtils.convert_to_ast(s3_creds))

    # create launcher
    launcher = PythonTransformLauncher(runtime_config=SignatureCalculationPythonTransformConfiguration())
    # Launch python to process the input
    launcher.launch()