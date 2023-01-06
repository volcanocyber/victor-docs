Models
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

Utilizing Workflows
--------------------

Below are brief descriptions of each model currently available, and their associated example workflows.
The VICTOR team recommends use of the workflows at least through the output standardization process for
maximum user experience. All outputs will be in either ascii shapefile, csv, or netCDF formats depending
on the model, for compatibility's sake. 

VICTOR offers three sets of options for visualization. The first is through any of the dozen libraries included in
the built-in conda environment. Second is the custom library ``victor.py`` for sharp and accurate
plotting through a handful of reuable functions. For the most versastile work, a virtual desktop with
QGIS and Paraview (and likely more programs in the future) reside for a fully featured experience.

.. _Conflow Citations:

Conflow/Confort
----------------

Confort is an updated version of Conflow, an open-source numerical model for flow in eruptive conduits during steady-state pyroclastic eruptions.
Confort's improvements include more accurate rheological parameters and equations, evaluations of crystal-bearing rheology,
additions of crystal and vesicle size distribution, and integration of degassing in both equilibrium and disequilibrium conditions.

The example workflow sparse and should be fairly easy to follow. After importing the necessary libraries,
The first cell contains all input parameters, ranging from the pressure at the beginning and ends of the model to the weight percent
of various chemical compounds and particles. The following two cells can be run without input. Following these, please
thoroughly read the markdown cell, and select 7 outputs from the list of 27. Input those numbers into the next cell in a list.
Every subsequent cell can be run without user interaction. There is an intermediate output specified by the ``name`` variable,
but the most gracefully formatted file will always be ``Conflow.csv``, output to the current directory.

**References:**

Silvia Campagnola; Claudia Romano; Larry G Mastin; Alessandro Vona (2016), "Confort 15 (Conflow improvement)," https://theghub.org/resources/3743.

.. _Hazmap Citations:

Hazmap
-------

Hazmap is a computer program for simulating sedimentation of volcanic particles from discrete point sources and 
which outputs the corresponding ground deposit in its aptly named deposit mode. Additionally, Hazmap is able to evaluate the probability 
of overcoming a given loading threshold in the ground deposit by using a set of different wind profiles recorded in different days in its probability mode.

The example Hazmap workflow begins with a variety of flags and specifications for the Hazmap grid and output structure.
Comments should give some context for the inputs, though a manual is hyperlinked for the user's convenience.
The next cell is the last that requires user input. Take note that all four of ``diameters, densities, shapes, weight_percent``
should be equal lengths, and equal to ``num_particle_types``. The weights should also add up to 100, as they are percentages.

Subsequent cells can be run without additional interactions, resulting in a netCDF file named ``hazmap.nc`` and a contour graph.
We are currently working on adding a basemap background to this graph.

**References:**

Macedonio et al., 2005 G. Macedonio, A. Costa and A. Longo, A computer model for volcanic ash fallout and assessment of subsequent hazard, Comput. Geosci. 31 (7) (2005), pp. 837–845.

Antonio Costa (2013), "Hazmap," https://theghub.org/resources/hazmap.

.. _IMEX Citations:

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


**References:**

Elisa Biaioli's thesis: https://dx.doi.org/10.15167/biagioli-elisa_phd2021-10-27

E. Biagioli, M. de’ Michieli Vitturi, and F. Di Benedetto. Modified shallow water model for viscous fluids and positivity preserving numerical approximation. Applied Mathematical Modeling, 94:482–505, 2021. doi: 10.1016/j.apm.2020.12.036.

M. de’ Michieli Vitturi, T. Esposti Ongaro, G. Lari, and A. Aravena. IMEX_SfloW2D 1.0. a depth-averaged numerical flow model for pyroclastic avalanches. Geosci. Model Dev., 12: 581–595, 2019. doi: 10.5194/gmd-12-581-2019.

.. _Molasses Citations:

MOLASSES
------------

MOdular LAva Simulation Software for Earth Science, or MOLASSES for short, is a probabalistic lava flow simulation tool. The required
inputs are very straightforward. In the first cell after the imports, all the user mnust enter is the residual thickness, 
the total volume of lava erupted, the pulse volume per simulation tick, and the DEM filename, along with the origin points
in UTM of the eruption. The user may optionally repeat runs due to the probabalisticnature of the model. After this cell, 
the rest of the model can run without input. If desired, the zoom level can be selected between a snapshot of the flow area and
the overall DEM with the flow overlayed. The workflow will output a well formatted CSV named ``flow.csv`` for the user, as well as 
a JPG of the final figure.


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

.. _pyFLOWGO Citations:

pyFLOWGO
-----------

Lava flow advance may be modeled through tracking the evolution of the lava’s thermo-rheological properties, which
are defined by viscosity and yield strength. These rheological properties evolve, in turn, with cooling and crystallization.
Such model was conceived by Harris and Rowland (2001) who developed a 1-D model, FLOWGO, in which velocity
of a control volume flowing down a channel depends on rheological properties computed following the lava cooling and
crystallization path estimated via a heat balance box model. pyFLOWGO is an updated version written completely in Python
for increased flexibility and modernity.

The first input cell directly follows the imports, simply asking for the name of the flow, the slope file, which is *not* a DEM,
and the step size. The next cell requests flags to calculate a specific type of flux. Following this, the user must pick the method used
for calculating various aspects of the lava's physical properties. Next, the physical dimensions of the channel should be entered.
The final two cells specify eruption event parameters and thermal parameters. All subsequent cells can be run without further alteration.
In this case, the visualizations are done through a Python script included in the pyFLOWGO library.

**References:**

Chevrel, M., Labroquere, J., Harris, A., and Rowland, S. (2017). Pyflowgo: an open-source platform for simulation of
channelized lava thermo-rheological properties. Computational Geosciences.

.. _Tephra2 Citations:

Tephra2
------------
Tephra2 is a tephra dispersion model, that estimates the mass of tephra that would accumulate at a site or over a region, 
given explosive eruption conditions. There are a variety of inputs required here for an accurate representation.

The user must first input coordinate and date information to grab reanalysis data. In order to make the experience as
simple as possible, we use the Copernicus API. However, as long as the user follows the provided format in the Github_.
The user can then run the next handful of cells until they see the heading for the configuration file. Here, the user must
input quantitative data about the tephra expulsion itself, though the vent UTM coordinates are assumed to be at the same position
as the wind file by default. Following the first 7 main inputs, another 12 optional inputs are included for more granular modeling,
though defaults will be used if not set. The user can then continue again until they reach the grid file header. The grid radius, spacing, and
elevation must be input, where the the volcano's UTM coordinates again are assumed to be the same. From here, every cell through the end can be run
resulting in an isomass tricontour of the tephra dispersion. The VICTOR team is working on adding a basemap and additional data to the visualization at the moment.

.. _Github: https://github.com/geoscience-community-codes/tephra2

**References:**

Bonadonna, C., Connor, C. B., Houghton, B. F., Connor, L., Byrne, M., Laing, A., and Hincks, T. K. (2005) Probabilistic modeling of tephra dispersal: 
Hazard assessment of a multiphase rhyolitic eruption at Tarawera, New Zealand, Journal of Geophysical Research: Solid Earth 110(B3). DOI 10.1029/2003JB002896

Connor, Laura J., and Charles B. Connor (2006) Inversion is the key to dispersion: understanding eruption dynamics by
 inverting tephra fallout In H. M. Mader, S. G. Coles, C. B. Connor & L. J. Connor (Eds.), Statistics in Volcanology, Geological Society of London Special Publications 231. DOI 10.1144/IAVCEI001.18

Biass, Sebastien, Bagheri, Gholamhossein, Aeberhard, William H., and Bonadonna, Costanza (2014) TError: 
towards a better quantification of the uncertainty propagated during the characterization of tephra deposits, Statistics in Volcanology 1(2):1-27. DOI 10.5038/2163-338X.1.2

Biass, S., Bonadonna, C., Connor, L., and Connor, C. (2016) TephraProb: a Matlab package for probabilistic hazard
 assessments of tephra fallout, Journal of Applied Volcanology 5(1):10. DOI 10.1186/s13617-016-0050-5 