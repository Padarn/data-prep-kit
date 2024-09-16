# Fuzzy Deduplication Ray-base KubeFlow Pipeline Transformation 


## Summary 
This project allows execution of the [multi step fuzzy dedup](../ray) as a 
[KubeFlow Pipeline](https://www.kubeflow.org/docs/components/pipelines/overview/). As 
defined [here](../README.md), this version of fuzzy dedup is a combination of 3 transforms:
* Fuzzy dedup preprocessor
* Fuzzy dedup bucket processor
* Fuzzy dedup filter

As a result, we provide here three workflows - one for each step. Each step has its own 
resource requirements and can be executed independently. Note although, that supporting
actors parameters - number of doc, minhash and bucket actors and dedup parameters - threshold
and number of permutations can not change between steps. The number of actors is computed by 
the preprocessor workflow based on the amount of documents and should be entered in the 
subsequent ones.

For production purposes it also makes sense to create a "super workflow" combining all 3 steps

The detail pipeline is presented in the [Simplest Transform pipeline tutorial](../../../../kfp/doc/simple_transform_pipeline.md) 

## Compilation

In order to compile pipeline definitions run
```shell
make workflow-build
```
from the directory. It creates a virtual environment (make workflow-venv) and after that compiles the pipeline 
definitions in the folder. The virtual environment is created once for all transformers. 

Note: the pipelines definitions can be compiled and executed on KFPv1 and KFPv2. Meantime, KFPv1 is our default. If you
prefer KFPv2, please do the following:
```shell
make clean
export KFPv2=1
make workflow-build
```

The next steps are described in [Deploying a pipeline](../../../../kfp/doc/simple_transform_pipeline.md#deploying-a-pipeline-)
and [Executing pipeline and watching execution results](../../../../kfp/doc/simple_transform_pipeline.md#executing-pipeline-and-watching-execution-results-)