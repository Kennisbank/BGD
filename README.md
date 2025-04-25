# BredeGroeneDijk
The Wide Green Dike Project

This model was developed by Peter Jansson and colleagues as part of a task to conceptualise an innovative infrastructure renewal process in the Netherlands as a System Dynamics problem, including barriers to upscaling. 

The model dashboard can be accessed [here](https://exchange.iseesystems.com/public/maaike-van-aalst/dijken-en-natuur). The project is led by the waterboard Hunze en Aa's. More info on the stakeholders involved can be found [here](https://www.hunzeenaas.nl/projecten/brede-groene-dijk/).

![BGD](img/bgd.jpeg)

## Navigating the Repository

The full system dynamic model: [Dijken_en_Natuur_v4_small](models\Dijken_en_Natuur_v4_small.xmile) is provided in the [XMILE](https://systemdynamics.org/resources-old/xmile/) open source standard format. It can be found in the [models](models) directory. 

### Using the model data and configuration in System Dynamics modeling software
The original model was created in the [Stella](https://en.wikipedia.org/wiki/STELLA_(programming_language)) propietary software distributed by [isee systems](https://www.iseesystems.com/). However, it should be possible to import XMILE file containing the full model data and configuration in other [system dynamics software programs](https://en.wikipedia.org/wiki/Comparison_of_system_dynamics_software) that follow the XMLE standard, i.e. [Vensim](https://vensim.com/).

### Controlling the model with Python (expert modelers)
For more advanced system dynamics modeling experts the full model is also provided as [Python](https://www.python.org/) .py file, also in the models directory. This version of the model, generated from the XMILE file using the [PySD](https://github.com/SDXorg/pysd) python package, can be reconfigured, edited, controlled, run, or (re)serialized as XMLE files in Python - using PySD. The PySD documentation can be accessed [here](https://pysd.readthedocs.io/en/master/). For you convenience, the repository's [pyproject.toml](pyproject.toml) file can be used to build a python environment capable of controlling the model with PySD.

### Data Sources
Publically available external data (if any) can be found in the [data](data) directory.

### License
Please note the [LICENSE](LICENSE) file describes how the repository data is distributed for use. A seperate LICENSE file may or may not be found in the [model](model) and/or [data](data) directories. If a seperate LICENSE file is found in those directories, it applies to the distribution and use of the model or data files, respectively; and it supercedes the repository license, for model or data files, respectively.




