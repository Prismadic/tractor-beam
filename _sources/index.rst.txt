.. tractor_beam documentation master file, created by
   sphinx-quickstart on Sat Dec 23 16:09:53 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. raw:: html

   <h1 align="center">

   Welcome to the 🛸 docs

.. raw:: html

   </h1>

|DIV|

.. toctree::
   :maxdepth: 3
   :caption: Packages & useful classes

   tractor_beam.abduct	
   tractor_beam.laser
   tractor_beam.visit	
   tractor_beam.utils

.. raw:: html

   <h1 align="center">

tractor-beam

.. raw:: html

   </h1>

.. raw:: html

   <p align="center">

high-efficiency text & file scraper with smart tracking

.. raw:: html

   </p>

.. raw:: html

   <p align="center">

~ client/server networking for building language model datasets fast ~

.. raw:: html

   </p>

💾 Installation
---------------

.. code:: bash

   pip install llm-tractor-beam

or

.. code:: bash

   python3 setup.py install

🛸 Tutorial
-----------

`examples <https://github.com/Prismadic/tractor-beam/blob/main/examples/examples.ipynb>`__

🌈 ``tractor.Beam()``
---------------------

The ``Beam`` class serves as the core engine of a highly configurable,
modular library designed for parallel processing and automation of tasks
such as web scraping, data downloading, processing, and storage. This
class leverages various components and lower-level functions to
orchestrate complex workflows. Here’s an in-depth look at its roles and
interactions with other components:

⚙️ Initialization and Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Upon initialization, the ``Beam`` class loads and verifies the
configuration using the ``Config`` class. It checks if the
configuration adheres to the expected structure and format,
indicating the system’s readiness to execute tasks as defined by
the user.

Job Processing and Workflow Management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **Job Processing**: The ``process_job`` and ``_runner`` methods are
   central to executing tasks defined in the configuration. These
   methods handle the execution flow of each job, including data
   downloading (``Abduct`` class), data recording (``Visits`` class),
   and data processing (``Focus`` class). This showcases the class’s
   ability to manage diverse tasks sequentially, ensuring each step is
   completed before moving to the next.
-  **Parallel and Delayed Execution**: The ``go`` method orchestrates
   the execution of all jobs, allowing for parallel processing to
   optimize resource utilization. It uses Python’s ``multiprocessing``
   to distribute tasks across available CPU cores, enhancing efficiency,
   especially for CPU-bound tasks. Additionally, it supports delayed
   execution for specific jobs, enabling time-controlled or periodic
   task execution.
-  **Resource Management**: By leveraging the ``Pool`` class from
   ``multiprocessing`` for parallel execution, the ``Beam`` class
   efficiently manages system resources. It calculates the optimal
   number of processes based on the number of available CPU cores and
   the number of jobs, ensuring a balance between performance and
   resource usage.

📝 ``utils.Config()``
---------------------

The ``Config`` class is responsible for loading, parsing, saving, and
manipulating configuration data. It can load configuration from a file
or a dictionary, parse the configuration data into a structured format,
save the configuration to a file, unbox the configuration by creating a
project directory, create a new project directory with a configuration
file, and destroy a project directory.

Example Usage
^^^^^^^^^^^^^

.. code:: python

   # Load configuration from a file
   config = Config('config.json')
   config.load_conf('config.json')

   # Load configuration from a dictionary
   config_dict = {
       "role": "watcher",
       "settings": {
           "name": "my_project",
           "proj_dir": "/path/to/project",
           "jobs": [
               {
                   "url": "https://example.com",
                   "types": ["type1", "type2"],
                   "beacon": "beacon1",
                   "delay": 1.5,
                   "custom": {
                       "func": "my_function",
                       "headers": {"header1": "value1"},
                       "types": ["type3", "type4"]
                   }
               }
           ]
       }
   }
   config.load_conf(config_dict)

   # Save the configuration to a file
   config.save()

   # Unbox the configuration by creating a project directory
   config.unbox()

   # Create a new project directory with a configuration file
   config.create()

   # Destroy a project directory
   config.destroy(confirm="my_project")

Code Analysis
^^^^^^^^^^^^^

Main functionalities
''''''''''''''''''''

-  Load configuration from a file or a dictionary
-  Parse the configuration data into a structured format
-  Save the configuration to a file
-  Unbox the configuration by creating a project directory
-  Create a new project directory with a configuration file
-  Destroy a project directory

Methods
^^^^^^^

-  ``__init__(self, conf: Union[str, dict, None] = None)``: Initializes
   a new instance of the ``Config`` class and loads the configuration.
-  ``load_conf(self, conf)``: Loads the configuration from a file or a
   dictionary.
-  ``parse_conf(self, conf_dict: Dict[str, Any]) -> Schema``: Parses the
   configuration data into a structured format.
-  ``save(self)``: Saves the configuration to a file.
-  ``unbox(self, overwrite: bool = False)``: Unboxes the configuration
   by creating a project directory.
-  ``create(self, config: dict = None)``: Creates a new project
   directory with a configuration file.
-  ``destroy(self, confirm: str = None)``: Destroys a project directory.


Fields
^^^^^^

-  ``conf``: The parsed configuration data.
-  ``conf.settings``: The settings of the configuration.
-  ``conf.settings.name``: The name of the configuration.
-  ``conf.settings.proj_dir``: The project directory of the
   configuration.
-  ``conf.settings.jobs``: The list of jobs in the configuration.
-  ``conf.settings.jobs.url``: The URL of a job.
-  ``conf.settings.jobs.types``: The types of a job.
-  ``conf.settings.jobs.beacon``: The beacon of a job.
-  ``conf.settings.jobs.delay``: The delay of a job.
-  ``conf.settings.jobs.custom``: The custom job data of a job.
-  ``conf.settings.jobs.custom.func``: The function of a custom job.
-  ``conf.settings.jobs.custom.headers``: The headers of a custom job.
-  ``conf.settings.jobs.custom.types``: The types of a custom job.

🧮 ``utils.BeamState()``
------------------------

The ``BeamState`` class is responsible for managing the state of a beam
in a laser system. It includes information about the host system, as
well as the states of different components such as abduction, focus, and
visit.

.. _example-usage-1:

Example Usage
^^^^^^^^^^^^^

.. code:: python

   # Create an instance of BeamState
   beam = BeamState()

   # Update the abduction state
   abduct_state = AbductState(conf={"param": "value"})
   beam.abduct_state_update(abduct_state)

   # Update the focus state
   focus_state = FocusState(conf={"param": "value"})
   beam.focus_state_update(focus_state)

   # Update the visit state
   record_state = RecordState(conf={"param": "value"})
   beam.record_state_update(record_state)

   # Update the host state
   beam.host_state_update()

   # Access the current state of the beam
   current_state = beam.states

.. _code-analysis-1:

Code Analysis
^^^^^^^^^^^^^

.. _main-functionalities-1:

Main functionalities
''''''''''''''''''''

-  Get information about the host system, including platform, CPU usage,
   memory usage, disk usage, network I/O, etc.
-  Update and retrieve the states of different components such as
   abduction, focus, and visit.
-  Keep track of the history of host states.

Methods
^^^^^^^

-  ``__init__()``: Initializes the ``BeamState`` class by setting the
   initial host info and states.
-  ``get_host_info()``: Retrieves the current host information and
   returns a ``HostInfo`` object.
-  ``abduct_state_update(state)``: Updates the abduction state by
   appending a new ``AbductState`` object to the ``abduct`` list in
   ``states``.
-  ``focus_state_update(state)``: Updates the focus state by appending a
   new ``FocusState`` object to the ``focus`` list in ``states``.
-  ``record_state_update(state)``: Updates the visit state by appending
   a new ``RecordState`` object to the ``visit`` list in ``states``.
-  ``host_state_update()``: Updates the host state by appending a new
   ``HostInfo`` object to the ``host_info`` list.

Fields
^^^^^^

-  ``host_info``: A list of ``HostInfo`` objects that represent the
   history of host states.
-  ``states``: An instance of the ``States`` class that contains the
   states of different components such as abduction, focus, and visit.


📝 ``abduct.Abduct()``
---------------------

The ``Abduct`` class is responsible for downloading files from a given
URL or a list of URLs. It can handle both simple URLs and URLs with
recursion. It also supports the option to overwrite existing files.

.. _example-usage-2:

Example Usage
^^^^^^^^^^^^^

.. code:: python

   # Initialize the Abduct class
   abduct = Abduct(conf=conf, job=job)

   # Download files from a single URL
   abduct.download()

   # Download files from a single URL and overwrite existing files
   abduct.download(o=True)

   # Download files from a single URL and specify a custom file name
   abduct.download(f="custom_file_name")

   # Download files from a URL with recursion
   abduct.download(types=["pdf", "docx"])

   # Download files from a URL with recursion and overwrite existing files
   abduct.download(types=["pdf", "docx"], o=True)

.. _code-analysis-2:

Code Analysis
^^^^^^^^^^^^^

.. _main-functionalities-2:

Main functionalities
''''''''''''''''''''

-  Initialize the ``Abduct`` class with a configuration and a job
   object.
-  Download files from a single URL or a list of URLs.
-  Handle URLs with recursion and filter files by their types.
-  Overwrite existing files if specified. \__\_ 

Methods
^^^^^^^

-  ``__init__(self, conf: dict = None, job: Job = None)``: Initializes
   the ``Abduct`` class with a configuration and a job object. It prints
   an info message if the configuration is loaded successfully.
-  ``_fetch_to_write(self, attachment, headers, attachment_path, file_name, block_size, o=False)``:
   Downloads a file from a given URL and writes it to the specified
   path. It appends the file information to the ``state.data`` list.
-  ``download(self, o: bool=False, f: str=None)``: Downloads files from
   a URL or a list of URLs. It handles both simple URLs and URLs with
   recursion. It can overwrite existing files if specified. It returns
   the ``state`` object. \__\_
   
Fields
^^^^^^

-  ``state``: An instance of the ``AbductState`` class that stores the
   current state of the ``Abduct`` class.
-  ``state.conf``: A dictionary that represents the configuration.
-  ``state.job``: An instance of the ``Job`` class that represents the
   current job.
-  ``state.data``: A list of dictionaries that stores the information of
   downloaded files. Each dictionary contains the file name and its
   path. \__\_

📡 ``abduct.beacons.*``
----------------------

“beacons” play a crucial role in a highly customizable and modular
system designed for web scraping, downloading, and processing data from
various sources. These beacons, represented by modules like the Stream
class, are key to achieving flexibility and modularity in the system.
The structure and functionality of the “beacons” can be documented as
follows:

Role of Beacons
'''''''''''''''

Modularity:
^^^^^^^^^^^

Beacons act as interchangeable modules within the system. Each beacon
corresponds to a specific source or type of data (e.g., financial
filings, news articles) and encapsulates the logic necessary for
fetching, parsing, and processing data from that source. This modularity
allows users to easily extend the system’s capabilities by adding new
beacons for different sources without altering the core functionality.

Customizability:
^^^^^^^^^^^^^^^

Beacons are designed to be customizable, allowing
users to specify parameters and behaviors specific to the data source
they target. This is evident in the Stream class, where the fetch method
can be tailored to parse and retrieve data according to the unique
structure of each source.


The Helpers class within a beacon further aids in bespoke
processing and manipulating the fetched data

Uniform Interface:
^^^^^^^^^^^^^^^^^^

Despite their differences in implementation, all beacons share a common
interface, exemplified by the mandatory inclusion of a Stream class with
consistent functions. This uniformity ensures that the main system can
interact with any beacon in a predictable manner, facilitating ease of
integration and use.

Enhanced Functionality through Helpers:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While the presence of a Stream class is mandatory for basic operations, the
inclusion of a Helpers class within a beacon provides additional utility
functions that are specific to the data or operations related to that
beacon. This structure offers an extended layer of customization,
enabling complex data manipulation and processing tasks that are
tailored to the beacon’s specific use case. 

Integration with the Main System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Beacons are seamlessly integrated into the main system, as
demonstrated by the use of importlib for dynamic module loading and the
structured approach to passing configurations and job details to
beacons. This integration allows the system to leverage the unique
capabilities of each beacon while maintaining a cohesive workflow.

Conclusion
''''''''''

The “beacons” in this system embody the principles of modularity,
customizability, and extensibility, serving as specialized modules that
can be dynamically integrated to add or modify the system’s data
processing capabilities. By adhering to a consistent interface while
allowing for beacon-specific customizations, the system achieves a
balance between uniformity and flexibility, enabling it to cater to a
wide range of data sources and processing requirements. This
architecture not only enhances the system’s utility and adaptability but
also facilitates ease of maintenance and expansion, making it a robust
solution for customizable and modular data processing tasks.

🔍 ``laser.Focus()``
--------------------

The ``Focus`` class is responsible for processing files by reading their
contents, detecting the encoding, and performing specific actions based
on the file type. It uses the ``Strip`` class to sanitize and extract
text content from XML or HTML documents. The processed data is then
written to a file using the ``writeme`` function.

.. _example-usage-3:

Example Usage
^^^^^^^^^^^^^

.. code:: python

   # Initialize a Focus object with a configuration and job
   focus = Focus(conf=conf, job=job)

   # Process a list of files
   data = [{'path': 'file1.xml'}, {'path': 'file2.html'}]
   result = focus.process(data)

   # Destroy a file
   focus.destroy(confirm='file1.xml')

.. _code-analysis-3:

Code Analysis
^^^^^^^^^^^^^

.. _main-functionalities-3:

Main functionalities
''''''''''''''''''''

-  Initialize a ``Focus`` object with a configuration and job
-  Process files by reading their contents, detecting the encoding, and
   extracting text content
-  Write the processed data to a file
-  Destroy a file if the confirmation matches the file name

Methods
^^^^^^^

-  ``__init__(self, conf: dict = None, job: Job = None)``: Initializes a
   ``Focus`` object with a configuration and job. Prints an
   initialization message.
-  ``process(self, data: dict = None)``: Processes a list of files by
   reading their contents, detecting the encoding, and extracting text
   content. Writes the processed data to a file. Returns the updated
   state of the ``Focus`` object.
-  ``destroy(self, confirm: str = None)``: Removes a file if the
   confirmation matches the file name. Prints a message indicating
   whether the file was successfully destroyed or not.

Fields
^^^^^^
-  ``state``: An instance of the ``FocusState`` class that stores the
   configuration and job information.
-  ``state.conf``: A dictionary representing the configuration.
-  ``state.job``: An instance of the ``Job`` class representing the job
   information.
-  ``state.data``: A list of dictionaries representing the processed
   data. Each dictionary contains the path of the file and the path of
   the cleaned file.

📝 ``visit.Visit()``
----------------------

The ``Visit`` class is responsible for creating and managing records in
a CSV file. It has methods for initializing the class, creating a new
CSV file, seeking specific records, and writing records to the CSV file.

.. _example-usage-4:

Example Usage
^^^^^^^^^^^^^

.. code:: python

   # Initialize the Visit class
   visit = Visit(conf=conf, job=job)

   # Create a new CSV file
   visit.create(data=data)

   # Seek specific records
   visit.seek(line=2)

   # Write records to the CSV file
   visit.write()

.. _code-analysis-4:

Code Analysis
^^^^^^^^^^^^^

.. _main-functionalities-4:

Main functionalities
''''''''''''''''''''

The main functionalities of the ``Visit`` class are: 
- Initializing the class with a configuration and job object 
- Creating a new CSV file with headers and data - Seeking specific records in the CSV file 
- Writing records to the CSV file

Methods
^^^^^^^ 

The ``Visit`` class has the following methods: 
   - ``__init__(self, conf: dict = None, job: Job = None)``: Initializes the class with a configuration and job object.
   - ``create(self, data: dict = None, o: bool = False)``: Creates a new CSV file with headers and data. 
   - ``seek(self, line: str | int = None, all: bool = False)``: Seeks specific records in the CSV file. 
   - ``write(self, o: bool = False, ts: bool = True, v: bool = False)``: Writes records to the CSV file.** 

Fields
^^^^^^

The ``Visit`` class has the following fields: 
   - ``headers``: A list to store the headers of the CSV file. 
   - ``state``: An instance of the ``RecordState`` class that stores the configuration, job, and data of the visit. \__\_

.. raw:: html

   <h3 align="center">

learn more about how Prismadic uses 🛸

subscribe to our `substack <https://prismadic.substack.com>`_

.. raw:: html

   </h3>


|A1| |A2|

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |A1| image:: https://github.com/Prismadic/.github/raw/main/profile/image_square.jpg
.. |A2| image:: https://github.com/Prismadic/.github/raw/main/profile/accent_color_square.jpg
.. |DIV| image:: https://github.com/Prismadic/magnet/raw/ef68535ecee236ff007638afa56de538b8fafd1a/divider.png