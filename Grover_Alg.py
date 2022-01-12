#+++++++++++++++++++++++++++++ Grover's Algorithm +++++++++++++++++++++++++++++++
#
# @Date = 20/12/2021 07:03:21
#
# @Author = Mohamed CHERRADI (Engineer and Ph.D. in computer science)
#
# @Email = m.cherradi@uae.ac.ma
#
# @Github = https://github.com/cherradii
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from qiskit.quantum_info import Operator
from qiskit import QuantumCircuit
from qiskit import BasicAer, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np

n=5
qc = QuantumCircuit(n)
qc.x(1)
qc.ccx(0,1,3)
qc.ccx(2,3,4)
qc.ccx(0,1,3)
qc.x(1)
qc.draw('mpl')

def phase_oracle(n,name = 'Uf'):
    qc = QuantumCircuit(n, name=name)
    qc.x(1)
    qc.ccx(0,1,3)
    qc.ccx(2,3,4)
    qc.ccx(0,1,3)
    qc.x(1)
    
    return qc
    
n=5
qc = QuantumCircuit(n)
for i in range(n-2):
    qc.x(i)
qc.ccx(0,1,3)
qc.ccx(2,3,4)
qc.ccx(0,1,3)
for i in range(n-2):
    qc.x(i)
qc.draw('mpl')

def diffuser(n, name='V'):
    qc = QuantumCircuit(n, name=name)
    
    for qb in range(n-2): #first layer of Hadamards in diffuser
        qc.h(qb)
   
    for i in range(n-2):
        qc.x(i)
    qc.ccx(0,1,3)
    qc.ccx(2,3,4)
    qc.ccx(0,1,3)
    for i in range(n-2):
        qc.x(i)
    
    for qb in range(n-2): #second layer of Hadamards in diffuser
        qc.h(qb)
        
    return qc
    
n=5
gr = QuantumCircuit(n, n-2)
nsol=1 #number of solutions

r = int(np.floor(np.pi/4*np.sqrt(2**(n-2)/nsol))) # Determine r
    
gr.h(range(n-2))    # step 1: apply Hadamard gates on all working qubits

# put ancilla in state |->
gr.x(n-1)
gr.h(n-1)
    
# step 2: apply r rounds of the phase oracle and the diffuser
for j in range(r):
    gr.append(phase_oracle(n), range(n))
    gr.append(diffuser(n), range(n))
        
gr.measure(range(n-2), range(n-2))    # step 3: measure all qubits
    
gr.draw('mpl')

simulator = Aer.get_backend('qasm_simulator')
job = execute(gr, backend=simulator, shots=1000)
counts = job.result().get_counts()

# plot_histogram(counts, title="Accuracy Grover's Algorithm", color='midnightblue')
plot_histogram(counts, title="Results after two iterations, executed on ibmq_qasm_simulator", color='midnightblue')
plt.savefig('grover_accuracy_result.eps')
