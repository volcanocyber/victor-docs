Integrative and Compound Workflows
===================================

This section collects workflows that combine model outputs, compare multiple
approaches, or analyze uncertainty across a broader scientific workflow. The
notebooks are intended to support benchmarking, inversion, and downstream
analysis rather than a single model run.

Lava Flow Benchmarking
----------------------
There have been a number of papers published on the accuracy of lava simulation models. This group of 
workflows are inspired by the Cordonnier_ and Dietterich_ benchmark papers. The goal of these notebooks
are to allow for modular implementations of the tests, as well as both qualitative and quantitative representations
of the results. The models included in these notebooks are :ref:`MOLASSES <Molasses Citations>`,
:ref:`MrLavaLoba <MrLavaLoba Citations>`, :ref:`IMEX_LavaFlow <IMEX Citations>`, and
:ref:`Lava2d <Lava2d Citations>`. We note
that the models have a wide range of implementation, ranging from cellular automata to a complete multiphase advection-diffusion
setup. Though the accuracy of the models is key to their effectiveness, the workflows also aim to highlight the shortcomings and strengths
of each mathematical approach. The current experiments are as follows:

- Isoviscous spreading drop on a plane: This reflects the behavior of lava cooling. For the time-dependent
	models, intermittent timesteps are used to track the evolution of the flow front as the radius increases. The time-independent flows simply
	display their final output.

- Inclined isoviscous isothermal spreading:  This reflects the behavior of lava purely as a viscous gravity current. Similarly to the first workflow, time-dependent
	flows track the evolution of the down-slope and cross-slope extents, whereas the time-independent models present the final settling point.

- Isothermal, isoviscous sloping flow into obstacles: This reflects the response of viscous flows to topographic barriers and the scale of geometry that may divert flows.
	Results here focus primarily on different shaped obstacles and how each model accumulates lava at these points uniquely.

- Mauna Loa 2022 exemplar: This eruption is quite data rich, including a high resolution footprint of the complete flow.
	Through parameter tuning, the models can closely mirror that final footprint. Through the integration of BAM_,
	statistical analysis of the model output against the true footprint are expressed.

Through the creation of this suite of workflows, the VICTOR team aims to provide complex technical implementations in a
simplified and streamlined form. A similar implementation for PDC and lahar flows is in progress as well.

**Notebooks:** To be added.

Inversion Workflows
-------------------

This notebook uses observations and model outputs to estimate source
parameters. Using thousands of tephra2's final output, providing the thickness and mass of the deposited particulate,
it is possible to find the eruption source parameters with a high degree of certainty, providing the location, volume, 
and height of the ash cloud from the eruption. This notebook includes prior and parameter definitions, inversion configuration,
convergence checks, and posterior or best-fit result visualization.

**Notebooks:** To be added.

Noise on DM Analysis
--------------------

This notebook implements the analysis presented by Roman_ and Lundgren (2025)
to investigate how errors in digital elevation models affect lava-flow
forecasting and parameter estimation. The workflow studies topographic noise,
vertical measurement error, spatial resolution, and temporal sampling, and
tracks their effects on flow width, advance rate, and inferred effusion rate.

The notebook should reproduce the paper's simple noisy-topography experiments
and provide a modular way to vary the noise amplitude and sampling strategy.
Results should include sensitivity plots and uncertainty summaries that make
the approximately 10 percent relative-noise threshold visible, since noise of
that scale can substantially reduce simulated advance rates and compromise the
retrieval of eruption parameters.

**Notebooks:** To be added.

Adding a Workflow
-----------------

For each workflow, include the notebook link, a short description of its
scientific purpose, required input data, expected outputs, and any model- or
environment-specific setup instructions.

References
----------

.. _Cordonnier: https://doi.org/10.1144/SP426.7

Cordonnier, B., Lev, E., & Garel, F. (2015). Benchmarking lava-flow models.
In *Lava Flow Hazards and Modeling*, Geological Society, London, Special
Publications, 426, SP426.7. https://doi.org/10.1144/SP426.7

.. _Dietterich: https://doi.org/10.1186/s13617-017-0061-x

Dietterich, H. R., Lev, E., Chen, J., Richardson, J. A., & Cashman, K. V.
(2017). Benchmarking computational fluid dynamics models of lava flow
simulation for hazard assessment, forecasting, and risk management.
*Journal of Applied Volcanology*, 6, 9.
https://doi.org/10.1186/s13617-017-0061-x

.. _Roman: https://doi.org/10.1029/2025GL115913

Roman, A., & Lundgren, P. (2025). Resolution and error constraints of
topographic measurements for accurate lava flow forecasting. *Geophysical
Research Letters*, 52(21), e2025GL115913.
https://doi.org/10.1029/2025GL115913

.. _BAM: https://doi.org/10.1007/s00445-026-01983-9

Garin, F., Charbonnier, S. J., Connor, C. B., Lev, E., Krasnoff, S., & Patra,
A. (2026). Best-fit Assessment for Models (BAM): An open-source Python-based
statistical tool for assessing the performance of numerical models in
volcanology. *Bulletin of Volcanology*, 88(7), 79.
https://doi.org/10.1007/s00445-026-01983-9
