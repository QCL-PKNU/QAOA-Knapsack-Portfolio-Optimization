
# Empirical Analysis of Quantum Approximate Optimization Algorithm for Knapsack-based Financial Portfolio Optimization


## Installation
To install the required packages, run the following command:

```
    pip install -r requirement.txt 
```



## Project Structure

Below is an overview of the project files and their purpose:

- `mv.py`: Contains a class to calculate that is used to calculated expected return of Portfolio based on Markowitz model.

- `circuits.py`: Defines the quantum circuit required to construct the QAOA algorithm, including all necessary components and feasible oracles.

- `knapsack.py`: Implements the knapsack problem based on expected return.

- `main.py`: The entry point of the application. This script runs the QAOA algorithm to find the probability distribution of the optimal solution.

- `plot.py`: Provides a class to plot the probability distribution and calculate the approximation ratio.

- `qaoa.py`: Defines the QAOA algorithm, building upon the circuits defined in `circuits.py`.

- `utils.py`: Includes utility functions required for calculating QAOA parameters and parsing results.

- `expected_return.ipynb`: Includes the expected_return of Portfolio from a various cases of experiment.

## Usage

 1.  To obtain the expected_returns run `expected_return.ipynb`
 2.  To run the QAOA algorithm in order to get the approximation ratio, run the following command:
 

```
   python main.py
```
## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your proposed changes.

## Acknowledgments

This repository includes code that is based in part on the work of Jan Rasmus Holst, developed during his Bachelor’s thesis:

**J. R. Holst**, *“Quantum Approximate Optimization Algorithm for the Knapsack Problem,”* Bachelor’s thesis, Institut für Theoretische Physik, Leibniz Universität Hannover, 2023.  
Available at: [https://www.itp.uni-hannover.de/fileadmin/itp/qinfo/Team_Tobias_Osborne/Bachelors_Theses/Jan_Rasmus_Holst_Bachelors_Thesis.pdf](https://www.itp.uni-hannover.de/fileadmin/itp/qinfo/Team_Tobias_Osborne/Bachelors_Theses/Jan_Rasmus_Holst_Bachelors_Thesis.pdf)

Parts of the implementation in this repository were inspired by and adapted from Mr. Holst’s publicly available code, which is licensed under the BSD 3-Clause License:  
[https://github.com/rhlst/qaoa-for-the-knapsack-problem](https://github.com/rhlst/qaoa-for-the-knapsack-problem)

We gratefully acknowledge Mr. Holst’s prior work and the valuable discussions that took place before the preparation of the related publications.  
All reused code components are used in compliance with the terms of the BSD 3-Clause License.


