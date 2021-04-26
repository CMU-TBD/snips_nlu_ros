# SNIPS_NLU_ROS

A ROS wrapper for [the SNIPS NLU engine](https://github.com/snipsco/snips-nlu).

# Dependencies
Install the snips-nlu into the python environment using 
```
pip install snips-nlu
```


<!-- # Run
To run, set the `dataset_path` in the `start.launch` or manually set the rosparam of `snips_nlu_ros/dataset` to the path of the dataset. start the launch
file and you can start querying the NLU engine using the actionserver at `snips_nlu_ros/parse` with the `NLUAction`. There's also a python wrapper `snips_nlu_ros` for easy usage

# Sample Usage
Refer to `scripts/test_node.py` for usage using actionlib.

If Using python library
```
from snips_nlu_ros import SnipsNLU

nlu_engine = SnipsNLU()
result = nlu_engine.parse("This is a sentence")
print(result)

``` -->
