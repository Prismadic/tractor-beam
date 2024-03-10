<center>
<p align="center">
   <img height="250" width="250" src="./tractor_beam.png">
   <br>
   <h3 align="center">tractor-beam</h3>
   <p align="center">high-efficiency text & file scraper with smart tracking</p>
   <p align="center"><i>~ client/server networking for building language model datasets <b>fast</b> ~</i></p>
</p>

</center>

## 💾 Installation

``` bash
pip install llm-tractor-beam
```

or

``` bash
python3 setup.py install
```

## 🛸 Tutorial

[examples](https://github.com/Prismadic/tractor-beam/blob/main/examples/examples.ipynb)

### 🌈 tractor.Beam()

The `Beam` class serves as the core engine of a highly configurable, modular library designed for parallel processing and automation of tasks such as web scraping, data downloading, processing, and storage. This class leverages various components and lower-level functions to orchestrate complex workflows. Here's an in-depth look at its roles and interactions with other components:

#### Initialization and Configuration

> [!NOTE]  
> Upon initialization, the `Beam` class loads and verifies the configuration using the `Config` class. It checks if the configuration adheres to the expected structure and format, indicating the system's readiness to execute tasks as defined by the user.

#### Job Processing and Workflow Management
- **Job Processing**: The `process_job` and `_runner` methods are central to executing tasks defined in the configuration. These methods handle the execution flow of each job, including data downloading (`Abduct` class), data recording (`Records` class), and data processing (`Focus` class). This showcases the class's ability to manage diverse tasks sequentially, ensuring each step is completed before moving to the next.
- **Parallel and Delayed Execution**: The `go` method orchestrates the execution of all jobs, allowing for parallel processing to optimize resource utilization. It uses Python's `multiprocessing` to distribute tasks across available CPU cores, enhancing efficiency, especially for CPU-bound tasks. Additionally, it supports delayed execution for specific jobs, enabling time-controlled or periodic task execution.
- **Resource Management**: By leveraging the `Pool` class from `multiprocessing` for parallel execution, the `Beam` class efficiently manages system resources. It calculates the optimal number of processes based on the number of available CPU cores and the number of jobs, ensuring a balance between performance and resource usage.

#### Modular Components Interaction
- **Abduct**: Handles the downloading of data from specified URLs or sources. It's a critical first step in the workflow, fetching the necessary data for subsequent processing.
- **Records**: Responsible for creating and writing records of the processed data. This component ensures that data collected and processed by the system is stored in a structured and retrievable manner.
- **Focus**: Focuses on processing and purifying the downloaded data. This component can include filtering, cleaning, or transforming data to meet specific requirements or formats.

#### Customization and Flexibility
- The system is designed with customization and flexibility in mind, allowing users to define jobs with specific parameters and behaviors. This is evident in the ability to include delays in job execution and the use of a dynamic configuration that can be tailored to various tasks.

#### Cleanup and Destruction

> [!IMPORTANT]
> **Resource Cleanup**: The `destroy` method provides a mechanism for cleaning up or deleting resources (e.g., downloaded files, logs) based on user confirmation. This feature is essential for managing disk space and ensuring that sensitive data can be securely removed when no longer needed.

#### Conclusion
The `Beam` class exemplifies a robust framework for automating and managing a wide range of data-related tasks. Its architecture promotes modularity, efficiency, and flexibility, making it suitable for applications that require sophisticated data handling capabilities, such as web scraping, data analysis, and automated reporting. By abstracting the complexities of task scheduling, parallel execution, and component interaction, the `Beam` class offers a powerful toolset for developers and researchers to streamline their workflows and optimize resource usage.

---

### 📡 clone.beacons

"beacons" play a crucial role in a highly customizable and modular system designed for web scraping, downloading, and processing data from various sources. These beacons, represented by modules like the Stream class, are key to achieving flexibility and modularity in the system. The structure and functionality of the "beacons" can be documented as follows:

##### Role of Beacons

#### Modularity:
Beacons act as interchangeable modules within the system. Each beacon corresponds to a specific source or type of data (e.g., financial filings, news articles) and encapsulates the logic necessary for fetching, parsing, and processing data from that source. This modularity allows users to easily extend the system's capabilities by adding new beacons for different sources without altering the core functionality.
#### Customizability:
Beacons are designed to be customizable, allowing users to specify parameters and behaviors specific to the data source they target. This is evident in the Stream class, where the fetch method can be tailored to parse and retrieve data according to the unique structure of each source. 

> [!TIP]  
> The Helpers class within a beacon further aids in bespoke processing and manipulating the fetched data

#### Uniform Interface:
Despite their differences in implementation, all beacons share a common interface, exemplified by the mandatory inclusion of a Stream class with consistent functions. This uniformity ensures that the main system can interact with any beacon in a predictable manner, facilitating ease of integration and use.
#### Enhanced Functionality through Helpers:
While the presence of a Stream class is mandatory for basic operations, the inclusion of a Helpers class within a beacon provides additional utility functions that are specific to the data or operations related to that beacon. This structure offers an extended layer of customization, enabling complex data manipulation and processing tasks that are tailored to the beacon's specific use case.
#### Integration with the Main System:
Beacons are seamlessly integrated into the main system, as demonstrated by the use of importlib for dynamic module loading and the structured approach to passing configurations and job details to beacons. This integration allows the system to leverage the unique capabilities of each beacon while maintaining a cohesive workflow.

##### Conclusion

The "beacons" in this system embody the principles of modularity, customizability, and extensibility, serving as specialized modules that can be dynamically integrated to add or modify the system's data processing capabilities. By adhering to a consistent interface while allowing for beacon-specific customizations, the system achieves a balance between uniformity and flexibility, enabling it to cater to a wide range of data sources and processing requirements. This architecture not only enhances the system's utility and adaptability but also facilitates ease of maintenance and expansion, making it a robust solution for customizable and modular data processing tasks.

## 📝 needs

- [x] worker/server engineering
- [x] good readme
- [x] config template / management
  - [ ] optional encryption of config unboxings
- [ ] tests 😢
  - [ ] move more to `.utils`
  - [x] if / ternary conventions
- [x] implement API response option for `Abduct`
  - [x] custom header arg for `Abduct`
- [x] add multiprocessing where needed
  - [x] put `tqdm` in the right places
