# QC4DB_VQC_Tutorial

A simple example of using a variational quantum circuit (VQC) for quantum machine learning for join order optimization.

## Usage

1. Install requirements  

```
pip install -r requirements.txt 
```

2. Run the code

```
python vqc.py
```

## Quantum machine learning

We use quantum machine learning to select the best join order for a SQL query. For this we train a VQC to predict the expected reward of each possible join order and we choose the order with the highest predicted reward.

- VQC is optimized like a neural network by the Adam optimizer
- Only considers the tables appearing in a query
- Tables are encoded using angle encoding
- Example is implemented for queries with 4 tables
- Reward is calculated as best/chosen and is 0 for cross joins


## Project files

### Data files

-  benchmark.csv: Contains the measured quality of all join orders. A value of -1 indicates that this join order would lead to a cross join and these are not measured. Format:
        
        Col 1: List of tables names seperated by ;
        Col 2-16:   Execution times of the join orders
        Col 17-31:  Number of intermediate results created by the join orders

-  data.csv: Benchmark data prepared for quantum machine learning. Can be created from benchmark.csv by using prepareData.py Format:
        
        Col 1-4: Features representing the features. Created by turning each tablename into an id and mapping them to the interval [0,pi]. Used as angle of the encoding rotation gates
        Col 5-20:   Rewards for the corresponding join orders calculated from the execution times padded to 2^n
        Col 21-36:  Rewards for the corresponding join orders calculated from the number of intermediate results padded to 2^n