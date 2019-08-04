## Setup:
Python 3 has been used to create the code
conda environment used to install and run gdal version 3.0.1
numpy also installed in conda environment

List of installed packages ./environment.yml


## Running Task1 from top directory
> source setup.sh
> python Task1/run.py --example [1/2]

Argument determines an example original UDM, default set to that in task


## Running Task2 with 'Extra' TIFF output included 
> source setup.sh
> python Task2/run.py Task2/calibration_vector.json

TIFF image found in outputs directory


## Running the testing framework from the top direcory
> source setup.sh
> python Testing/run_tests.py

This will run the test on both tasks
