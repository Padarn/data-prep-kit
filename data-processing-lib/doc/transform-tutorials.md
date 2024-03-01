# Transform Tutorials

All transforms operate on a [pyarrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)
read for it by the RayWorker and produce zero or more transformed tables.
The transformed tables are then written out by the RayWorker - the transform need not
worry about I/O associated with the tables.
This means the Transform itself need only be concerned with the conversion of one
in memory table at a time.  

### Transform Basics
In support of this model the class 
[AbstractTableTransform](../src/data_processing/transform/table_transform.py) 
is expected to be extended when implementing a transform.
The following methods are defined:
* ```__init__(self, config:dict)``` - an initializer through which the transform can be created 
with implementation-specific configuration.  For example, the location of a model, maximum number of
rows in a table, column(s) to use, etc. 
* ```transform(self, table:pyarrow.Table) -> tuple(list[pyarrow.Table], dict)``` - this method is responsible
for the actual transformation of a given table to zero or more output tables, and optional 
metadata regarding the transformation applied.  Zero tables might be returned when
merging tables across calls to `transform()` and more than 1 table might be returned
when splitting tables by size or other criteria.
  * _output tables list_ - the RayWork handles the various number of returned tables as follows: 
    * 0 - no file will be written out and the input file name will not be used in the output directory.
    * 1 - one parquet file will be written to the output directory with 
    * N - N parquet files are written to the output with `_<index>` appended to the base file name
  * _dict_ - is a dictionary of transform-specific data keyed to numeric values.  The RayWorker will
         accumlute/add dictionaries across all calls to transform across all RayWorkers.  As an example, a
         transform might wish to track the number of instances of PII entities detected and might return 
        this as `{ "entities" : 1234 }`.
* ```flush() -> tuple(list[pyarrow.Table], dict)``` - this is provided for transforms that
make use of buffering (e.g. coalesce) across calls to `transform()` and need to be flushed
of all buffered data at the end of processing of input tables.  The return values are handled
in the same was as the return values for `transform()`.  Since most transforms will likely
not need this feature, a default implementation is provided to return an empty list and empty dictionary.

### Running in Ray
When a transform is run using the Ray-based framework a number of other capabilities are involved:
* Transform Runtime - this uses the command line arguments (see below) to define the 
configuration data used to initialize the transform.
* Transform Configuration - defines the following:
  * the transform class to be used, 
  * command line arguments used to initialize the Transform Runtime and generally, the Transform.
  * Transform Runtime class to use
  * transform short name 
* Transform Launcher - this is a class generally used to implement `main()` that makes use
of a Transform Configuration to start the Ray runtime and execute the transforms.

Roughly speaking the following steps are completed to establish transforms in the RayWorkers
1. Launcher parses the CLI parameters using the Transform Configuration, 
2. Launcher passes the Transform Configuration and CLI parameters to the RayOrchestrator
3. RayOrchestrator create the Transform Runtime using the CLI parameters 
4. Transform runtime generates transform initialization/configuration and optional Ray components
5. RayWorker is started with configuration from the Transform Runtime.
6. RayWorker creates the Transform using the configuration provided by the Transform Runtime.

![Processing Architecture](processing-architecture.jpg)

#### Transform Launcher
The `TransformLauncher` class uses the Transform Configuration
and provides a single method, `launch()`, that kicks off the Ray environment.
For example,
```python
launcher = TransformLauncher(MyTransformConfiguration())
launcher.launch()
```
Note that the launcher defines some additional CLI parameters that are used to
control the operation of the orchestrator and workers.  Things such
as memory, number of workers, where to locate the input and output files, etc.
Discussion of these options is beyond the scope of this document 
(see [Launcher Options](launcher-options.md) for a list of available options.)

#### Transform Configuration
The 
[DefaultTableTransformConfiguration](../src/data_processing/ray/transform_runtime.py)
class is sub-classed and initialized with transform-specific name, and implementation 
and runtime classes.
In addition, it is responsible for providing transform-specific
methods to define and filter optional command line arguments.
Finally, it creates the Transform Runtime, for which a default
implementation uses the class available in the Transform Configuration.
```python

class MyTransformConfiguration(DefaultTableTransformConfiguration):

    def __init__(self):
        super().__init__(name="MyTransform", transform_class=MyTransform,
                          runtime_class=MyTransformRuntime
        self.params = {}
    def add_input_params(self, parser: ArgumentParser) -> None:
        ...
    def apply_input_params(self, args: Namespace) -> bool:
        ...
    def create_transform_runtime(self) -> DefaultTableTransformRuntime:
        ...
```
Details are covered in the samples below.

#### Transform Runtime
The 
[DefaultTableTransformRuntime](../src/data_processing/ray/transform_runtime.py)
class is provided and will be 
sufficient for many use cases, especially 1:1 table transformation.
However, some transforms will require use of the Ray environment, for example,
to create additional workers, establish a shared memory object, etc.
Of course, these transforms will generally not run standalone from the Ray environment. 

```python
class DefaultTableTransformRuntime:

    def __init__(self, params: dict[str, Any]):
        ...

    def get_transform_config(
        self, data_access_factory: DataAccessFactory, statistics: ActorHandle, files: list[str]
    ) -> dict[str, Any]:
        ...

    def compute_execution_stats(self, stats: dict[str, Any]) -> dict[str, Any]:
        ...
```

The RayOrchestrator initializes the instance with the CLI parameters provided by the Transform Configurations
`get_input_params()` method.

The `get_transform_config()` method is used by the RayOrchestrator to create the parameters
used to initialize the Transform in the RayWorker. 
This is where additional Ray components would be added to the environment 
and references added to them, as needed, in the returned dictionary of configuration data
that will initialize the transform.
For those transforms that don't need this support, the default implementation
simpy returns the CLI parameters used to initialize the runtime instance.

The `computed_execution_stats()` provides an opportunity to augment the statistics
collected and aggregated by the TransformStatistics actor. It is called by the RayOrchestrator
after all files have been processed.

### Tutorial Examples
With these basic concepts in mind, we start with a simple example and 
progress to more complex transforms. 
Before getting started  you may want to consult the 
[transform development environment](transform-dev-env.md) documentation.
* [Simplest transform](simplest-transform-tutorial.md)
Here we will take a simple example to show the basics of creating a simple transform
that takes a single input Table, and produces a single Table.
* [Advanced transform](advanced-transform-tutorial.md)
* [Porting from GUF 0.1.6](transform-porting.md)

Once a transform has been built, testing can be enabled with the testing framework:
* [Transform Testing](testing-transforms.md) - shows how to test a transform
independent of the Ray framework.
* [End-to-End Testing](testing-e2e-transform.md) - shows how to test the
transform running in the Ray environment.