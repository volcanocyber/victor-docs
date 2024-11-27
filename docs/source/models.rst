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

.. list-table:: Currently available Models (please reach out if interested in other tools not currently listed)
   :widths: 50 50
   :header-rows: 1

   * - Volcanic Process
     - Relevant Models
   * - Lava Flows
     - IMEX-Lava, Lava2d, pyFLOWGO,	MrLavaLoba, MOLASSES,	VolcFlow, VENUSS
   * - PDCs
     - TITAN2D, IMEX_SfloW2D_V2 
   * - Ash Dispersal
     - HAZMAP, HySPLIT, Fall3D
   * - Tephra dispersal
     - Tephra2, Fall3D
   * - Gas dispersal
     - DISGAS, HySPLIT, TWODEE
   * - Lahars
     - LaharZ
   * - Slope Stability
     - Scoops3D
   * - Sulfur/Geochemical Degassing
     - Sulfur_X
   * - Conduit ascent
     - CONFORT


Utilizing Workflows
--------------------

Below are brief descriptions of each model currently available, and their associated example workflows.
The VICTOR team recommends use of the workflows at least through the output standardization process for
maximum user experience. All outputs will be in either ascii shapefile, csv, or netCDF formats depending
on the model, for compatibility's sake. 

VICTOR offers three sets of options for visualization. The first is through any of the dozen libraries included in
the built-in conda environment. Second is the custom library ``victor.py`` for sharp and accurate
plotting through a handful of reuable functions. For the most versastile work, a virtual desktop with
QGIS resides for a fully featured experience.

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

.. _Disgas Citations:

Disgas
--------
DISGAS (passive DISpersion of GASes and particles) is a Eulerian model for passive dispersion of diluted gas and fine dust particles.
Turbulent diffusion is based on the K-theory, and the wind field can be evaluated assuming either a wind profile based on the similarity theory or using
a terrain-following mass consistent wind model. The model can be used to forecast concentration of gas (or dust) over complex terrains.

The DISGAS workflow begins with parameters relating to the date of the simulation, as well as its duration, and options concerning if it was continuing from an existing run.
Next, one must enter data about the grid and general topography. The grid information is required, though the exact elevation can either be sourced from a file or simplified into a slope.
The third cell asks the user how they want to treat the model. When treated as a gas with no settling velocity, extra parameters are not needed.
However, when treated as a set of particles, the physical properties and mathematical methods to calculate the settling velocity.
Then, the user must specify the vertical and horizontal wind turbulence models as well as the soil roughness model and diffusion coefficients.
The final input cell requests the user to input file paths for supplemental input data in addition to output intervals and the option to output directional velocities and concentration.

The next two cells format the input and run the model.
Depending on the number of wind data points provided, multiple layers will be output. The user must then specify a layer,
and can then run the following cell to output a set of plots over the timespan.

**References**

\A. Costa, G. Macedonio, Chiodini G., 2005. Numerical model of gas dispersion emitted from volcanic sources. Annals of Geophysics, Vol. 48: 805-815. https://www.annalsofgeophysics.eu/index.php/annals/article/view/3236

Granieri D., Costa A., Macedonio G., Chiodini G., Bisson M. (2013) Carbon dioxide in the city of Naples: contribution and effects of the volcanic source, J. Volcanol. Geotherm. Res., Vol. 260: 52-61, doi: 10.1016/j.jvolgeores.2013.05.003 https://www.sciencedirect.com/science/article/pii/S0377027313001443

Costa A., Macedonio G. (2016) DISGAS: A model for passive DISpersion of GAS, Rapporti tecnici INGV, N. 332, Istituto Nazionale Di Geofisica e Vulcanologia, Italy http://datasim.ov.ingv.it/download/disgas/manual-disgas-2.0.pdf

Fall3D
--------
FALL3D is a 3D model for atmospheric passive transport and deposition of particles, aerosols, and radionuclides based on the so-called
advection-diffusion-sedimentation (ADS) equation.

The code version 8.x has been redesigned and rewritten from scratch in order to overcome legacy issues and allow for successive
optimisations in the preparation towards extreme-scale computing. The new versions include significant improvements from the point of
view of model physics, numerical algorithmic methods, and computational efficiency. In addition, the capabilities of the model have been extended
by incorporating new features such as the possibility of running ensemble forecasts and dealing with multiple atmospheric species (i.e. volcanic ash
and gases, mineral dust, and radionuclides). Ensemble run capabilities are supported since version 8.1, making it possible to quantify model uncertainties
and improve forecast quality.

The workflow is currently in development in a partnership between the VICTOR team and Leo Mingari of INGV. 

**References**

Folch, Arnau, Costa, Antonio, Macedonio, Giovanni, & Mingari, Leonardo. (2022). FALL3D (8.1.2). Zenodo. https://doi.org/10.5281/zenodo.6343786


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

Macedonio et al., 2005 G. Macedonio, A. Costa and A. Longo, A computer model for volcanic ash fallout and assessment of subsequent hazard, Comput. Geosci. 31 (7) (2005), pp. 837–845. https://www.sciencedirect.com/science/article/pii/S0098300405000269

Antonio Costa (2013), "Hazmap," https://theghub.org/resources/hazmap.

.. _Hysplit Citations:

Hysplit
----------

The Hybrid Single-Particle Lagrangian Integrated Trajectory model (HYSPLIT)[1] is a computer model created by NOAA that is used to compute air parcel trajectories to determine how far and in what direction a parcel of air, and subsequently air pollutants, will travel.

VICTOR contains the entirety of Hysplit, though our workflow focuses on modeling ash deposition and concentration.
First, the user is asked to specify the particle distribution configuration, vertical and horizontal turbulence models, as well as the output file name.
Equally as important in the first cell is the number of particles per cycle, as well as the maximum particles released.

The second input cell requires the user to enter the start date, latitude/longitude of the volcano and the ash column, and the maximum runtime of the model.
It also requires an input data grid. For each particle, an identifier, along with emission rate, hours of emission, and start time are necessary.

The final input cell has the user concentration grid information, along with sampling interval timing, and then a swath of particle information including,
but not limited to, the density, diameter, deposition velocity and decay rate if it is an unstable molecule.

Upon completing the inputs, the user will run the model and be given a choice of timesteps to pick from. After this choice, every other cell can be run. Three images will be the result.
First, the workflow uses a built-in visualizer from Hysplit. Next, it uses the matplotlib library. Finally, we use Bokeh for and interactivate and more data-rich experience.

**References:**

Stein, A.F., Draxler, R.R, Rolph, G.D., Stunder, B.J.B., Cohen, M.D., and Ngan, F., (2015). NOAA's HYSPLIT atmospheric transport and dispersion modeling system, Bull. Amer. Meteor. Soc., 96, 2059-2077, http://dx.doi.org/10.1175/BAMS-D-14-00110.

Rolph, G., Stein, A., and Stunder, B., (2017). Real-time Environmental Applications and Display sYstem: READY. Environmental Modelling & Software, 95, 210-228, https://doi.org/10.1016/j.envsoft.2017.06.025this link opens in a new window. ( http://www.sciencedirect.com/science/article/pii/S1364815217302360)

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

Subsequent cells write out the config files and run the model. The only other place input is neccesary is a one line cell with the ``step`` variable.
IMEX outputs data at every dt chosen by the user, so in order to view data at a given timestamp, you **must** choose a step. All subsequent cells can
ran without input to give a detailed output of both temperature and thickness of the flow at a given time. Additionally, seperate netCDF files 
containing time series data for the temperature and depth are both supplied as output, along with a JPG of the figure.


**References:**

Elisa Biaioli's thesis: https://dx.doi.org/10.15167/biagioli-elisa_phd2021-10-27

E. Biagioli, M. de’ Michieli Vitturi, and F. Di Benedetto. Modified shallow water model for viscous fluids and positivity preserving numerical approximation. Applied Mathematical Modeling, 94:482–505, 2021. doi: 10.1016/j.apm.2020.12.036. https://www.sciencedirect.com/science/article/pii/S0307904X21000019

M. de’ Michieli Vitturi, T. Esposti Ongaro, G. Lari, and A. Aravena. IMEX_SfloW2D 1.0. a depth-averaged numerical flow model for pyroclastic avalanches. Geosci. Model Dev., 12: 581–595, 2019. doi: 10.5194/gmd-12-581-2019. https://gmd.copernicus.org/articles/12/581/2019/

.. _Laharz Citations:

LAHARZ
---------

LaharZ is an open source tool which can be used to model various flow hazards, developed by Keith Blair
most significantly lahars. Its inputs are a digital elevation model (DEM), a stream file 
(which defines stream thalwegs) and a flow direction file. From these inputs, 
LaharZ creates an energy cone based on a height/length (H/L) ration; a set of initiation points 
(which can be edited) and a set of flow files based on a range of volumes.

The stream and flow files can be created on any appropriate QIS system; the resulting flows can 
similarly be displayed on any GIS system. However, LaharZ has been written and tested using QGIS.

The graphics produced can be displayed on any visualisation tool (including QGIS’s 3D mapping tool).
However, LaharZ has been written and tested using Paraview for 3D graphics.

The programme is based on Schilling, S.P., 1998.

For detailed documentation, please see `the documentation`_ on Keith's  Github repository

.. _the documentation: https://github.com/Keith1815/laharz/blob/main/docs/Laharz%202.1.3a%20User%20Guide.pdf

**References:**

Schilling, S.P., 1998, LaharZ—GIS Programs for automated mapping of lahar-inundation hazard zones: U.S. Geological Survey Open-File Report 98-638, 80 p. https://pubs.usgs.gov/publication/ofr98638

Griswold, J.P., and Iverson, R.M., 2008, Mobility statistics and automated hazard mapping for debris flows and rock avalanches (ver. 1.1, April 2014): U.S. Geological Survey Scientific Investigations Report 2007-5276, 59 p. https://pubs.usgs.gov/sir/2007/5276/

Widiwijayanti, C., Voight, B., Hidayat, D. et al. Objective rapid delineation of areas atrisk from block-and-ash pyroclastic flows and surges. Bull Volcanol 71, 687–703 (2009). https://doi.org/10.1007/s00445-008-0254-6

Widiwijayanti, C., 2018, LaharZ: an open-source tool for the modeling of surface flows and hazards. Geosci. Model Dev., 9: 1–17, 2018. doi: 10.5194/gmd-9-1-2018. https://gmd.copernicus.org/articles/9/1/2018

.. _Lava2d Citations:

Lava2d uses a 2D depth-averaged finite volume framework to solve the propagation of a rheologically variable shallow viscoplastic gravity current flowing across natural terrain. The model does not average the thermal or rheological information over the flow depth, maintaining fidelity to the strong thermal stratification 
in lava flows by incorporating a more realistic thermal profile based on the transient cooling of a hot laminar flow of a high-Prandtl-number fluid. The novel aspects of the approach to energy propagation reduces the significant numerical 
stiffness of typical depth-averaged energy equations resulting from large cooling rates at the surface and base of the flow as well as eliminating the need for ad hoc relationships between depth-averaged temperature and surface temperature.

**References:**

 Hyman, D. M. R., Dietterich, H. R., & Patrick, M. R. (2022). Toward next-generation lava flow forecasting: Development of a fast, physics-based lava propagation model. Journal of Geophysical Research: Solid Earth, 127, e2022JB024998. https://doi.org/10.1029/2022JB024998 

.. _Magmaxiysm Citations:

Magmaxiysm
-----------
This model simulates the dynamics of a viscoelastic medium surrounding an axisymmetric magma cavity. A small python module `magmaxisym`` 
is provided for simulating the dynamics of a Maxwell-type viscoelastic medium surrounding an ellipsoidal axisymmetric magma cavity. 
The module is entirely based on the open source finite element library NGSolve.

**References:**

Rucker, C., Erickson, B. A., Karlstrom, L., Lee, B., & Gopalakrishnan, J. (2022). A computational framework for time‐dependent deformation in viscoelastic magmatic systems.
Journal of Geophysical Research: Solid Earth, 127(9). https://doi.org/10.1029/2022jb024506 

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

Connor, L. J., Connor, C. B., Meliksetian, K., & Savov, I. (2012) Probabilistic approach to modeling lava flow inundation: a lava flow hazard assessment for a nuclear facility in Armenia. Journal of Applied Volcanology (1):3. DOI 10.1186/2191-5040-1-3 https://appliedvolc.biomedcentral.com/articles/10.1186/2191-5040-1-3

Kubanek, J., Richardson, J. A., Charbonnier, S. J., & Connor, L. J. (2015) Lava flow mapping and volume calculations for the 2012–2013 Tolbachik, Kamchatka, fissure eruption using bistatic TanDEM-X InSAR. Bulletin of Volcanology 77(12):106. DOI 10.1007/s00445-015-0989-9 https://link.springer.com/article/10.1007/s00445-015-0989-9

.. _MrLavaLoba Citations:

MrLavaLoba
------------

MrLavaLoba is a stochastic model for simulating lava flows, written in Python. The workflow for this model begins with a large
amount of text, explaining input parameters in detail. After neccesary libraries are imported, all parameters are in the next cell.
A DEM sanity check follows, continuing on to write out the input files and run the model. A convenient progress bar will show the 
remaining time for model calculations. MrLavaLoba outputs snapshows at a given *dt* interval, so the user must pick a step to visualize.
The rest of the workflow configures and displays the flow based on the output shapefiles given, saving a JPG of the final figure.

**References:**

M. de' Michieli Vitturi and S. Tarquini. MrLavaLoba: A new probabilistic model for the simulation of lava flows as a settling process,
Journal of Volcanology and Geothermal Research, Volume 349, 2018, Pages 323-334, ISSN 0377-0273, https://doi.org/10.1016/j.jvolgeores.2017.11.016.

.. _Plumeria_wd Citations:

Plumeria_wd
------------
Plumeria is a one-dimensional model for wind-driven volcanic plumes. 
It was originally written in 2007 in Visual Basic to analyze plumes during the 2004-2008 eruption of Mount St. Helens (Mastin, 2007).  
The version in this folder, Plumeria_wd, has been modified for crosswinds, translated to Fortran, and tested by comparing predicted with observed plume heights from multiple eruptions (Mastin, 2014). 
It was compared with other 1D and 3D plume models 2016 (Costa et al., 2016).  
It has been used in several published studies to estimate mass eruption rate from plume height (e.g., Mastin et al., 2013; Mastin et al., in press), to assess when condensation and freezing may occur in plumes,
 and their association with lightning (e.g., Van Eaton et al., 2016, 2019, Smith et al., 2023), and to compare the path of bent plumes in laboratory studies (McNeal et al., 2019).

**References:**

Mastin, L.G., 2024, plumeria_wd software.  U.S. Geological Survey software program.  https://doi.org/10.5066/P1HVRKVN

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
channelized lava thermo-rheological properties. Computational Geosciences. https://ui.adsabs.harvard.edu/abs/2018CG....111..167C/abstract

.. _Scoops3D Citations:

Scoops3D
-----------

Scoops3D evaluates slope stability throughout a digital landscape represented by a digital elevation
 model (DEM). The program uses a three-dimensional (3D) method of columns limit-equilibrium analysis
 to assess the stability of many potential landslides (typically millions) within a user-defined 
 size range. For each potential landslide, Scoops3D assesses the stability of a rotational, spherical
slip surface encompassing many DEM cells. It provides the least-stable potential landslide for each DEM
 cell in the landscape, as well the associated volumes and (or) areas.

 The associated workflow provides a compartmentalized way to test landslide scenarios. Cells initially ask the user
 for descriptive information and input/output folders. Continuing on, a groundwater pressure and material properties
 are a vital required input. Continuing on, the user must enter an earthquake loading coefficient as a fraction of gravity.
 Next, the method for computing the factor of safety is specified. The subsequent three cells are used to specify the search area,
 which is a 3D domain. These parameters include DEM x, y, and z boundaries, as well as upper and lower
 limits for surface failure. Finally, a handful of flags may be set to generate additional outputs
 for the convenience of the modeler. Further cells can be run without additional input, though the visualized output can be changed
 between the primary outputs.

 For additional context and a more detailed manual, please `refer to this document <https://pubs.usgs.gov/tm/14/a01/pdf/tm14-a1.pdf>`_ 

**References:**

Reid, M.E., Christian, S.B., Brien, D.L., and Henderson, S.T., 2015, Scoops3D—Software to analyze 3D slope
stability throughout a digital landscape: U.S. Geological Survey Techniques and Methods, book 14, chap. A1, 218 p.,
http://dx.doi.org/10.3133/tm14A1


.. _Sulfur_X Citations:

Sulfur_X
------------

Sulfur_X is an advanced degassing model to track the evolution of S, CO2, H2O, and redox states in melt and co-existing vapor in ascending mafic-intermediate magma.
In particular, Sulfur_X shows that sulfur can start degassing in the lower crust or near-surface depending on the initial S6+/ΣS and H2O in the melt.

The workflow begins requesting initial values to set the state of the mode, including temperature, sulfur concentration, and granularity of pressure. 
Next, the user must input their choices for the degassing approach for COH and sulfur. Additional information on the algorithms used can be found in the model's documentation.
The following cell requires a file with melt inclusion data, which is key for an accurate assessment of degassing. Subsequently,
the user can toggle Monte Carlo runs for error estimation, and set the melt fraction. Finally, advanced inputs can be entered, concerning the exact composition of the
sulfide, the tolerance of FO2, and the water-melt fraction relation in the case of crysytallization.

The model creates graphs to present the output, which the workflow embeds as images for the user to analyze and save.


**References:**

ing, S., Plank, T., Wallace, P., Rasmussen, D. J., in press. Sulfur_X: 
A model of sulfur degassing during magma ascent. Geochemistry, Geophysics, Geosystems. https://doi.org/10.31223/X56H0F.

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
Hazard assessment of a multiphase rhyolitic eruption at Tarawera, New Zealand, Journal of Geophysical Research: Solid Earth 110(B3). DOI 10.1029/2003JB002896 https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2003JB002896

Connor, Laura J., and Charles B. Connor (2006) Inversion is the key to dispersion: understanding eruption dynamics by inverting tephra fallout In H. M. Mader, S. G. Coles, C. B. Connor & L. J. Connor (Eds.), Statistics in Volcanology, Geological Society of London Special Publications 231. DOI 10.1144/IAVCEI001.18 https://pubs.geoscienceworld.org/gsl/books/edited-volume/1732/chapter/107601115/Inversion-is-the-key-to-dispersionunderstanding

Biass, Sebastien, Bagheri, Gholamhossein, Aeberhard, William H., and Bonadonna, Costanza (2014) TError:  towards a better quantification of the uncertainty propagated during the characterization of tephra deposits, Statistics in Volcanology 1(2):1-27. DOI 10.5038/2163-338X.1.2 https://digitalcommons.usf.edu/siv/vol1/iss1/2/

Biass, S., Bonadonna, C., Connor, L., and Connor, C. (2016) TephraProb: a Matlab package for probabilistic hazard assessments of tephra fallout, Journal of Applied Volcanology 5(1):10. DOI 10.1186/s13617-016-0050-5 https://appliedvolc.biomedcentral.com/articles/10.1186/s13617-016-0050-5


.. _Titan2D Citations:

Titan2D
----------

TITAN2D is a geoflow simulation software application, specifically used for granular flows. As a deterministic model,
it requires a large array of parameters to be properly configured.

To begin, the user enters information for DEM format, the DEM itself, as well as some fundamental constants. This first section also includes iteration limits, and output intervals.
Next, numeric parameters are required. The user can choose to toggle adaptive mesh refinements for more accurate calculations at each timestep, along with the size of the initial pile and
the order of PDE to solve. Finally, the user must specify the material model and associated constants. We select the Coloumb model by default, though there are a total of four options.

Numerous optional additions can be made, including extra points of origin for lava, flux locations, and discharge planes for measuring flow over an are are all
toggleable options for the user. After this, the user can run another 4 cells and choose a timestamp once the model finishes running. All following cells can then be
run and result in a very detailed snapshot of the lava depth at the moment specified.

**References:**
Patra, A., Bevilacqua, A., Akhavan-Safaei, A., Pitman, E. B., Bursik, M., &amp; Hyman, D. (2020). Comparative analysis of the structures and outcomes of geophysical flow models and modeling assumptions using uncertainty quantification. Frontiers in Earth Science, 8. https://doi.org/10.3389/feart.2020.00275 

.. _Twodee Citations:

TWODEE-2
----------

TWODEE is a code for dispersion of heavy gases based on the solution of a shallow water equations system for fluid depth, depth-averaged horizontal velocities and depth-averaged fluid density. 
The workflow begins with a cell for the user to set parameters related to the date, runtime, and name of the current simulation.
Next, the user must input spacing values and UTM values for the topography. If a file is provided, elevation is sourced from it
though if not, a generalized slope is required from user entered values. The following two cells require
numerical terms, including the densities of the two gasses being compared and many environmental and entrainment coefficients as well as physical constants.
Subsequently, the user is asked to enter some location data for the meteorology, or more aptly the wind.
The second to last configuration cell simply asks the user to enter paths to various files, depending on the mode the user chose.
If not required, the cell can be left blank or as-is from the template. Finally, output parameters can be withheld or added as needed,
allowing for highly flexible output files. 

The next two cells can be run without any change, as they are creating a formatted input file and running the model. The following two cells open the result file and give a brief description of the possible values to display.
These values range from wind velocity and cloud thickness to gas concentration and altitude of critical concentration.
Currently, the user must then enter the set of values they want to display, and a lower bound. The bound allows for more accurate visualizations due to negligable low value data points.
The final cell can be run as is, and will result in a sharp, detailed plot of the chosen data over the topography.

**References**
Hankin, R., Britter, R. (1999a). TWODEE: the Health and Safety Laboratory's shallow layer model for heavy gas dispersion. Part 1. Mathematical basis and physical assumptions. J. Hazard. Mater. A66, 211-226.

Hankin, R., Britter, R. (1999b). TWODEE: the Health and Safety Laboratory's shallow layer model for heavy gas dispersion. Part 2. Outline and validation of the computational scheme. J. Hazard. Mater. A66, 227-237.

Hankin, R., Britter, R. (1999c). TWODEE: the Health and Safety Laboratory's shallow layer model for heavy gas dispersion. Part 3. Experimental validation (Thorney island). J. Hazard. Mater. A66, 237-261.
https://pubmed.ncbi.nlm.nih.gov/10334822/

Costa A., Chiodini G., Granieri D., Folch A., Hankin R.K.S., Caliro S., Cardellini C., Avino R. (2008). A shallow layer model for heavy gas dispersion from natural sources: application and hazard assessment at Caldara di Manziana, Italy., Geochem. Geophys. Geosyst., 9, Q03002, doi: 10.1029/2007GC001762. https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2007GC001762

Folch A., Costa A., Hankin R.K.S., 2009. TWODEE-2: A shallow layer model for dense gas dispersion on complex topography, Comput. Geosci., doi:10.1016/j.cageo.2007.12.017
https://www.sciencedirect.com/science/article/pii/S0098300408001404

Chiodini G., Granieri D., Avino R., Caliro S., Costa A., Minopoli C., Vilardo G., (2010) Non-volcanic CO2 Earth degassing: The case of Mefite di Ansanto (Southern Apennines), Italy, Geophys. Res. Lett., Vol. 37, L11303, doi: 10.1029/2010GL042858 https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010GL042858

.. _Venuss Citations:

VENUSS
-------
VENUSS is a model that uses finite element analysis (GetFEM++) to model solidifying and fracturing lava. As the main data is served primarily
through a JSON file, we refer users to the VENUSS documentation and Janine Birnbaum's thesis_ for more information.

.. _thesis: https://meetingorganizer.copernicus.org/EGU24/EGU24-16851.html

**References**:

Janine Birnbaum. (2023). JanineBirnbaum18/GetFem_breakouts: Initial release (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.8335429

.. _Volcflow Citations:

VolcFlow
-------
VolcFlow is a finite-difference Eulerian code based on the depth-averaged approach and developed for the simulation of isothermal geophysical flows.  Currently,
the only workflow that has this implemented is our PDC benchmark. The primary values changed by the user are the time constraints and the mechanical behavior.
The latter helps specify the type of solid flow to be simulated (i.e.. PDC, lahar, debris). 

**References**:

Kelfoun K. (2017). A two-layer depth-averaged model for both the dilute and the concentrated parts of pyroclastic currents. Journal of Geophysical Research – Solid Earth vol.122, – DOI:10.1002/2017JB014013.

Kelfoun K., Gueugneau V., Komorowsk JC, Aisyah N., Cholik N., Merciecca C. (2017). Simulation of block-and-ash flows and ash-cloud surges of the 2010 eruption of Merapi volcano with a two-layer model. Journal of Geophysical Research – Solid Earth vol.122, – DOI:10.1002/2017JB013981.

Gueugneau V., Kelfoun K., Druitt T. (2019). Investigation of surge-derived pyroclastic flow formation by numerical modeling of the 25 June 1997 dome collapse at Soufrière Hills Volcano, Montserrat. Bulletin of Volcanology vol.81, p.25, – DOI:10.1007/s00445-019-1284-y.


