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

from code2parquet_transform import (
    CodeToParquetTransform,
    CodeToParquetTransformConfiguration,
    data_factory_key,
    get_supported_languages,
    supported_langs_file_key,
)
from data_processing.runtime.pure_python import PythonTransformLauncher
from data_processing.runtime.pure_python.runtime_configuration import (
    PythonTransformRuntimeConfiguration,
)
from data_processing.utils import get_logger


logger = get_logger(__name__)


class CodeToParquetPythonConfiguration(PythonTransformRuntimeConfiguration):
    def __init__(self):
        super().__init__(transform_config=CodeToParquetTransformConfiguration(transform_class=CodeToParquetTransform))


if __name__ == "__main__":
    # launcher = NOOPRayLauncher()
    launcher = PythonTransformLauncher(CodeToParquetPythonConfiguration())
    logger.info("Launching noop transform")
    launcher.launch()