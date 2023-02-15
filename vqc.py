from math import pi
import csv
from collections import deque
import random
import numpy as np

# Qiskit Circuit imports
from qiskit.circuit import QuantumCircuit, QuantumRegister, Parameter, ParameterVector, ParameterExpression
from qiskit.circuit.library import TwoLocal

# Qiskit imports
import qiskit as qk
from qiskit.utils import QuantumInstance

# Qiskit Machine Learning imports
from qiskit_machine_learning.neural_networks import CircuitQNN
from qiskit_machine_learning.connectors import TorchConnector

# PyTorch imports
import torch
from torch import Tensor
from torch.optim import Adam

# Define number of qubits
num_qubits = 4

# Create a quantum circuit
qc = qk.QuantumCircuit(num_qubits)

# Parameters for input
x = qk.circuit.ParameterVector('x', num_qubits)
    
# Add encoding layer
for i in range(num_qubits):
    qc.rx(x[i], i)

# Add variational circuit
qc.compose(TwoLocal(num_qubits, ['ry','rz'], 'cx', 'linear',10), inplace=True)

# Draw the circuit 
qc.decompose().draw(output='mpl', filename='VQC.png')

# Extract the parameters to optimize
params = list(qc.parameters)[num_qubits:]

# Select a quantum backend to run the simulation of the quantum circuit
qi = QuantumInstance(qk.Aer.get_backend('aer_simulator_statevector'))

# Create a Quantum Neural Network 
qnn = CircuitQNN(qc, input_params=x, weight_params=params, 
                 quantum_instance = qi)

# Connect to PyTorch
initial_weights = (2*pi*np.random.rand(qnn.num_weights) - pi)
quantum_nn = TorchConnector(qnn, initial_weights)

# Define layer which scales values to the interval [0,1]
class NormLayer(torch.nn.Module):        
    def forward(self, x):
        result = x/x.max()
        return result

# Create a sequential model from the qantum network and the classical norm layer
model = torch.nn.Sequential(quantum_nn, NormLayer())

# Load data 
with open('data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC))
       
# Use the adam optimizer    
optimizer = Adam(model.parameters(), lr=0.005)

# Buffer for the last 40 rewards
rewards = deque(maxlen=40)

# Train the model
for episode in range(30):

    # Choose a random data entry
    entry = random.choice(data)

    # Predict rewards from the features
    prediction = model(Tensor(entry[0:4]))

    # Choose join order with highest predicted reward
    selected = prediction.argmax()
    
    # Store the real reward this selection would give
    rewards.append(entry[4+selected])

    # Calculate loss as sum of the squared errors
    loss = 0
    for i in range(0, len(prediction)):
        loss+= (prediction[i] - entry[4+i])**2

    # Show quality of current episode
    print("Episode: {}, loss: {:.3f}, Reward : {:.3f}".format(episode, loss.item(),sum(rewards)/len(rewards) ), end="\n")

    # Optimize using backpropagation
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()









