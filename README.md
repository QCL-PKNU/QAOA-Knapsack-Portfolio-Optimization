
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

Thank you to all contributors and researchers in the quantum computing field who have provided the foundation for this work.





