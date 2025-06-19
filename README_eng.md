# Testing Tool User Guide

Here are instructions for running the modes and how to collect and display the results.

## Table of Contents
- [Source Code Structure](#source-code-structure)
- [0. Preparation](#0-preparation)
- [1. Single-Process Testing](#1-single-process-testing)
- [2. Two-Process Testing](#2-two-process-testing)
- [3. Scientific Publications](#3-scientific-publications)
- [Citations](#citations)

---

## Source Code Structure

The source code consists of folders for different purposes.

The directories ```pythonfuzz```, ```pythonfuzz_with_dqn```, ```pythonfuzz_with_ppo```, ```pythonfuzz_with_grpo``` contain the source code of the single-process experiment scripts.

The directories with the prefix ```colabmode_``` contain the source code of the two-process experiment scripts.

The ```experiment_results``` directory contains the analysis files, including the average execution speed, average memory consumption, and the graph of coverage over time.

The ```targets``` directory contains the target programs. The files in this directory are of the form ```libraryName_fuzz```, where ```libraryName``` is the library to be tested.

## 0. Preparation

Before testing, make sure the library to be tested is installed.

```bash
pip/pip3 install libraryName
```

Create a target program file for testing, named ```libraryName_fuzz.py```.

Copy the ```targets``` folder to the folder containing the scenario to be run.

Delete the log file ```libraryName_log.py``` in the scenario folder if it exists.

---

## 1. Single-process testing

This mode is for running tests using a single process.

Suppose the scenario to be tested is named ```scenario```.

### Steps:

```bash
cd scenario
python/python3 main.py libraryName_fuzz
```

You can add ```timeout``` to test within a specified time.

For example, if you need to test within a day, execute the command

```bash
timeout 86400s python/python3 main.py libraryName_fuzz
```

The log file is recorded in ```libraryName_log.txt```.

Copy this file to the ```experiment_results``` directory to process the results.

## 2. Testing two processes

This mode is for running tests that combine two processes.

Suppose we run ```colabmode_scenario_1``` and ```colabmode_scenario_2``` in parallel.

### Steps:

Open terminal 1:

```bash
cd colabmode_scenario_1
python/python3 main.py libraryName_fuzz ../shared_seeds_queue
```

Open terminal 2:

```bash
cd colabmode_scenario_2
python/python3 main.py libraryName_fuzz ../shared_seeds_queue
```

The steps for processing the results are similar to [Single-Process Testing](#1-single-process-testing), in which the processed file will be taken from the process that obtained the highest final coverage.

We can also use ```timeout``` to limit the testing time.

## 3. Scientific Publication

```GRFuzz``` was published in the IEEE IRI 2025 conference.

## Citation