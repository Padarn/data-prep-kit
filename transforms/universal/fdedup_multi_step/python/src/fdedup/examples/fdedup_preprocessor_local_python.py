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

from data_processing.runtime.pure_python import PythonTransformLauncher
from data_processing.utils import ParamsUtils
from fdedup.transforms.base import (preprocessor_doc_column_name_cli_param,
                                    preprocessor_int_column_name_cli_param,
                                    preprocessor_delimiters_cli_param,
                                    preprocessor_num_permutations_cli_param,
                                    preprocessor_threshold_cli_param,
                                    preprocessor_shingles_size_cli_param,
                                    preprocessor_minhash_snapshot_directory_cli_param)
from fdedup.transforms.python import FdedupPreprocessorPythonTransformRuntimeConfiguration

# create launcher
launcher = PythonTransformLauncher(FdedupPreprocessorPythonTransformRuntimeConfiguration())
# create parameters
input_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../test-data/input"))
output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../output"))
local_conf = {
    "input_folder": input_folder,
    "output_folder": output_folder,
}
code_location = {"github": "github", "commit_hash": "12345", "path": "path"}
params = {
    # Data access. Only required parameters are specified
    "data_local_config": ParamsUtils.convert_to_ast(local_conf),
    # orchestrator
    "runtime_pipeline_id": "pipeline_id",
    "runtime_job_id": "job_id",
    "runtime_code_location": ParamsUtils.convert_to_ast(code_location),
    # fdedup parameters
    preprocessor_doc_column_name_cli_param: "contents",
    preprocessor_int_column_name_cli_param: "Unnamed: 0",
    preprocessor_delimiters_cli_param: " ",
    preprocessor_num_permutations_cli_param: 64,
    preprocessor_threshold_cli_param: .8,
    preprocessor_shingles_size_cli_param: 5,
}
sys.argv = ParamsUtils.dict_to_req(d=params)

# launch
launcher.launch()