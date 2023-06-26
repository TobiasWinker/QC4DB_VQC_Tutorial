# QC4DB_VQC_Tutorial

A simple example of using a variational quantum circuit (VQC) for quantum machine learning for join order optimization.

This tutorial was presented at the SIGMOD conference 2023.

## Material
* [Accompanying slides](SIGMOD_tutorial_slides.pdf)
* [Tutorial website](https://www.helsinki.fi/en/researchgroups/unified-database-management-systems-udbms/sigmod-2023-tutorial)

## Cite

Tobias Winker, Sven Groppe, Valter Uotila, Zhengtong Yan, Jiaheng Lu, Maja
Franz, and Wolfgang Mauerer. 2023. **Quantum Machine Learning: Foundation, New
Techniques, and Opportunities for Database Research**. *In Companion of the 2023
International Conference on Management of Data (SIGMOD/PODS '23)*. Association
for Computing Machinery, New York, NY, USA, 45–52. https://doi.org/10.1145/3555041.3589404

BibTeX entry:

```
@inproceedings{winker:23:sigmodtutorial,
  author = {Winker, Tobias and Groppe, Sven and Uotila, Valter and Yan, Zhengtong and Lu, Jiaheng and Franz, Maja and Mauerer, Wolfgang},
  title = {Quantum Machine Learning: Foundation, New Techniques, and Opportunities for Database Research},
  year = {2023},
  isbn = {9781450395076},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  url = {https://doi.org/10.1145/3555041.3589404},
  doi = {10.1145/3555041.3589404},
  booktitle = {Companion of the 2023 International Conference on Management of Data},
  pages = {45–52},
  numpages = {8},
  keywords = {quantum computing, databases, quantum machine learning},
  location = {Seattle, WA, USA},
  series = {SIGMOD/PODS '23}
}

```

## Setup

### Docker

```
docker build -t sigmod_tutorial_qc4db .
docker run --name qc4db_tutorial -v $PWD:/home/tutorial/tutorial -p 8888:8888 -d sigmod_tutorial_qc4db
```

### Local

```
pip install -r requirements.txt
./run.sh
```

### Start Tutorial
Navigate to http://localhost:8888/notebooks/qc4jo.ipynb in a Browser.


## Quantum machine learning

We use quantum machine learning to select the best join order for a SQL query. For this we train a VQC to predict the expected reward of each possible join order and we choose the order with the highest predicted reward.

- VQC is optimized like a neural network by the Adam optimizer
- Only considers the tables appearing in a query
- Tables are encoded using angle encoding
- Example is implemented for queries with 4 tables
- Reward is calculated as best/chosen and is 0 for cross joins


## Project files

### Data files

-  benchmark.csv: Contains the measured quality of all join orders. A value of -1 indicates that this join order would lead to a cross join and these are not measured. 
Format:
        
        Col 1: List of tables names seperated by ;
        Col 2-16:   Execution times of the join orders
        Col 17-31:  Number of intermediate results created by the join orders

-  data.csv: Benchmark data prepared for quantum machine learning. Can be created from benchmark.csv by using prepareData.py. 
Format:
        
        Col 1-4: Features representing the features. Created by turning each tablename into an id and mapping them to the interval [0,pi]. Used as angle of the encoding rotation gates
        Col 5-20:   Rewards for the corresponding join orders calculated from the execution times padded to 2^n
        Col 21-36:  Rewards for the corresponding join orders calculated from the number of intermediate results padded to 2^n
