Usage
=====

.. _register:

Registration
------------

To gain access to VICTOR, you must first register. Currently, we are authenticating users through Github, and thus all users 
are required to possess an account. To register, please visit the VICTOR website_ and press the register button in the top right.
This will direct you to a form where you can provide the neccesary information.

.. _website: https://localhost:9999

.. _runmodels:

Once you are able to access the hub, you will see a screen very similar to this:

.. image:: ./default.png

Run Models
------------

To run models, there are a few simple steps. First, navigate to the ``shared`` folder. You can either run the the ``*****_setup.sh``
 files directly, or copy one, either through manual selection (right click + copy) with the mouse, or through the terminal with ``cp shared/*****_setup.sh .`` when you are in the home directory.

.. note::

   All files in the ``shared`` folder are read/execute only. If you would like to contribute models, data, or ideas for improvement,
   please contact victor@ldeo.columbia.edu.

Once this runs, you will have all necessary files contained in a new folder in your home directory. Most folders will simply contain the executable
and the example notebook. All Juptyter notebook workflows will generate most of the supplemental files necessary for the model to run.

However, DEMs are not automatically included. Users then have 4 primary options: 
1. Navigate to the DEMs folder in ``shared`` and copy the relevant file to your home directory, if the file needs to be altered.
2. Read the DEM from ``$HOME/shared/DEMs`` directly in your workflow, if no changes are required.
3. Import your own DEM from a local machine, dragging and dropping into the file tree.
4. Utilize S3 buckets or an SQL connection (using boto3 or mysql python packages) to load files remotely. 

At this point, users can go through the first few cells immediately succeeding the import statement, inputting parameters as needed.
Thorough descriptions of each parameter are included. Once finished, the user can simply press the fast forward symbol to run all cells, or ``shift + enter/return`` to run each cell individually.

Citations and References
------------------------
Below are citations and related works used to create this project. To add additional citations or for clarification, contact victor@ldeo.columbia.edu

**Conflow**

See :ref:`Conflow Citations` here.

**Hazmap**

See :ref:`Hazmap Citations` here.

**IMEX-Lava**

See :ref:`IMEX Citations` here.

**Molasses**

See :ref:`Molasses Citations` here.

**MrLavaLoba**

See :ref:`MrLavaLoba Citations` here.

**pyFLOWGO**

See :ref:`pyFLOWGO Citations` here.

**Tephra2**

See :ref:`Tephra2 Citations` here.

Contributing Models and Hub Additions
-------------------------------------
If you believe your model would be a good fit for our platform, please email victor@ldeo.columbia.edu with a link to the code on a version-control platform
as well as a brief explanation. For additions to the hub itself, please refer to `our Github repository`_. Create an issue for general advice,
or create a pull request for specific changes/updates.  

.. _our Github repository: https://github.com/volcanocyber/VICTOR-notebook
