import circuit

class QaoaAnsatz:
    def __init__(self, hamiltonian, step=1, init_circuit=None):
        self.hamiltonian = hamiltonian
        self.step = step
        self.n_qubits = max(max(self.hamiltonian))
        if init_circuit:
            self.init_circuit = init_circuit
            if init_circuit.n_qubits > self.n_qubits:
                self.n_qubits = init_circuit.n_qubits
        else:
            self.init_circuit = circuit.Circuit(self.n_qubits).h[:]
        self.init_circuit.run() # To make a cache.

    def n_params(self):
        return self.step * 2

    def get_circuit(self):
        c = self.init_circuit.copy()
        # TODO: implement

    def get_objective(self, params):
        pass
        # TODO: implement
