Usage
=====

Models Overview
----------------

VICTOR supports a wide array of both numerical and probabalistic models
on its systems. Execution of the models can be done directly from the command line
through the command line, though we recommend running everything through Jupyter Notebooks.

Each notebook is built uniquely for the model, though as many aspects
as possible are generalized. Most often, this results in significantly
diverging methods of parameter input, but a very similar output and visualization.
For example, current models are built in Fortran, C, C++, and Python, and thus require
different libraries and input formats. Visualizations and data parsing, however, are all done primarily using
the *rasterio*, *matplotlib*, and *xarray* libraries, though others are available for your convenience. Additionally,
common actions for the hub, such as file I/O and cross-library visualization are referenced in the *VICTOR* module.

.. note:: Due to the varied languages and file requirements, additional files neccesary for the models may be included in
    the generated folders. Intended output files will be clearly specified by both the workflow and documentation.


IMEX
----------

IMEX-SfloW2d is a depth-averaged numerical flow model for pyroclastic avalanches. 
The configuration file is extremely in depth, so the workflow splits it into more manageable pieces.
We begin with simple parameters to set a run name, simulation time constraints, and output files. Next are
radial source parameters, described as where ``The source of mass is initialized. The cells belonging 
to the source are are identified ( source_cell(j,k) = 2 )``. The next cell sets bounds for the DEM we use, 
and some flags that allow for more granular setting of constants. The next cell functions as a sanity check for the DEM.

After the DEM, we set temperature parameters of the environment and related material thermal constants, followed by the algorithms
selected for the numerical slope calculations for each cell. Gravity is a configurable option for future flexibility. Rheological 
parameters and constants are then assigned, followed by gas transport parameters, which constitute gas attributes and pressure specification.

The given parameters are a condensed version of the overall choices. Additional scenarios can be added, such as the pyroclastic source
generating from a collapsing volume. Further documentation will be provided in the future, though the souce code is the only reference for now.
All values after the DEM check can be kept as is for a reasonable estimate. The three cells before are the only places that must be changed in reference 
to the DEM to function properly.

Subsequent cells write out the config files and run the model. THe only other place input is neccesary is a one line cell with the ``step`` variable.
IMEX outputs data at every dt chosen by the user, so in order to view data at a given timestamp, you **must** choose a step. All subsequent cells can
ran without input to give a detailed output of both temperature and thickness of the flow at a given time. Additionally, seperate netCDF files 
containing time series data for the temperature and depth are both supplied as output, along with a JPG of the figure.

.. _IMEX Citations:

**References:**


Elisa Biaioli's thesis: https://dx.doi.org/10.15167/biagioli-elisa_phd2021-10-27

E. Biagioli, M. de’ Michieli Vitturi, and F. Di Benedetto. Modified shallow water model for viscous fluids and positivity preserving numerical approximation. Applied Mathematical Modeling, 94:482–505, 2021. doi: 10.1016/j.apm.2020.12.036.

M. de’ Michieli Vitturi, T. Esposti Ongaro, G. Lari, and A. Aravena. IMEX_SfloW2D 1.0. a depth-averaged numerical flow model for pyroclastic avalanches. Geosci. Model Dev., 12: 581–595, 2019. doi: 10.5194/gmd-12-581-2019.


MOLASSES
------------

MOdular LAva Simulation Software for Earth Science, or MOLASSES for short, is a probabalistic lava flow simulation tool. The required
inputs are very straightforward. In the first cell after the imports, all the user mnust enter is the residual thickness, 
the total volume of lava erupted, the pulse volume per simulation tick, and the DEM filename, along with the origin points
in UTM of the eruption. The user may optionally repeat runs due to the probabalisticnature of the model. After this cell, 
the rest of the model can run without input. If desired, the zoom level can be selected between a snapshot of the flow area and
the overall DEM with the flow overlayed. The workflow will output a well formatted CSV named ``flow.csv`` for the user, as well as 
a JPG of the final figure.

.. _Molasses Citations:

**References:**

Connor, L. J., Connor, C. B., Meliksetian, K., & Savov, I. (2012) Probabilistic approach to modeling lava flow inundation: a lava flow hazard assessment for a nuclear facility in Armenia. Journal of Applied Volcanology (1):3. DOI 10.1186/2191-5040-1-3

Kubanek, J., Richardson, J. A., Charbonnier, S. J., & Connor, L. J. (2015) Lava flow mapping and volume calculations for the 2012–2013 Tolbachik, Kamchatka, fissure eruption using bistatic TanDEM-X InSAR. Bulletin of Volcanology 77(12):106. DOI 10.1007/s00445-015-0989-9 

.. _MrLavaLoba Citations:

MrLavaLoba
------------

MrLavaLoba is a stochastic model for simulating lava flows, written in Python. THe workflow for this model begins with a large
amount of text, explaining input parameters in detail. After neccesary libraries are imported, all parameters are in the next cell.
A DEM sanity check follows, continuing on to write out the input files and run the model. A convenient progress bar will show the 
remaining time for model calculations. MrLavaLoba outputs snapshows at a given *dt* interval, so the user must pick a step to visualize.
The rest of the workflow configures and displays the flow based on the output shapefiles given, saving a JPG of the final figure.

**References:**

M. de' Michieli Vitturi and S. Tarquini. MrLavaLoba: A new probabilistic model for the simulation of lava flows as a settling process,
Journal of Volcanology and Geothermal Research, Volume 349, 2018, Pages 323-334, ISSN 0377-0273, https://doi.org/10.1016/j.jvolgeores.2017.11.016.