import numpy as np
import random

class tpm:
    def __init__(self, N, K, L):
        self.N, self.K, self.L = N, K, L
        self.weights1 = None
        self.weights2 = None
        self.inputs = None
        self.output = None

    def randomWeights(self):
        """Generates random weights for the tree parity machine"""
        random.seed()
        self.weights = np.array([random.randint(-self.L, self.L)
                                for x in range(self.N*self.K)])

    def randomInputs(self):
        """Generates random inputs for the tree parity machine"""
        random.seed()
        self.inputs = np.array([random.randint(-1, 1)
                               for x in range(self.N*self.K)])

    def signum(self, x):
        """Activation function for hidden layer neurons"""
        if x > 0:
            return 1
        return -1

    def calcWeights2(self):
        """Calculates the inputs to the output neuron"""
        self.weights2 = [self.signum(np.dot(
            self.weights[x*self.N:x*self.N+self.N], self.inputs[x*self.N:x*self.N+self.N])) for x in range(self.K)]

    def tow(self):
        """Activation function for the output neuron"""
        self.output = 1
        for x in self.weights2:
            self.output *= x

    def theta(self, a, b):
        if a != b:
            return 0
        return 1

    def HebbianLearning(self, aout, bout):
        """Modified Hebbian Learning algorithm for updating weights"""
        for x in range(self.N*self.K):
            self.weights[x] += self.weights2[int(x/self.N)]*self.inputs[x]*self.theta(
                self.weights2[int(x/self.N)], aout)*self.theta(aout, bout)

            if self.weights[x] > self.L:
                self.weights[x] = self.L
            elif self.weights[x] < -self.L:
                self.weights[x] = -self.L

# def big_theta(a, b):
# 	if(a == b):
# 		return 1
# 	else:
# 		return 0

# class TPM:

# 	def __init__(self, input_num, hidden_node_num, weight_range):
# 		self.input_num = input_num
# 		self.weight_range = weight_range
# 		self.hidden_node_num = hidden_node_num
# 		random.seed()
# 		self.weights = []
# 		self.step2_arr = []
# 		for x in range(input_num):  # Creates initial weights for the TPM randomly.
# 			self.weights.append(random.randint(-weight_range, weight_range))

# 	def fullcopy(self, new):
# 		new.input_num = self.input_num
# 		new.weight_range = self.weight_range
# 		new.hidden_node_num = self.hidden_node_num
# 		new.weights = []
# 		new.step2_arr = []

# 		for x in range(new.input_num):
# 			test = self.weights[x]
# 			new.weights.append(test)
# 		for y in range(new.hidden_node_num):
# 			test = self.step2_arr[y]
# 			new.step2_arr.append(y)

# 	#Calculates the output of the TPM on a given input vector
# 	def output(self, input_arr):
# 		self.step2_arr = []
# 		step_sum = 0
# 		result = 1
# 		for x in range(len(input_arr)):
# 			step_sum += input_arr[x] * self.weights[x]
# 			if x % (self.input_num/self.hidden_node_num) != 0:
# 				if step_sum > 0:
# 					self.step2_arr.append(1)
# 				elif step_sum == 0:
# 					self.step2_arr.append(0)
# 				else:
# 					self.step2_arr.append(-1)
# 				step_sum = 0

# 		for y in self.step2_arr:
# 			result *= y

# 		if result == 0:
# 			result = -1

# 		return result

# 	def hebbian_learning_rule(self, inputs, out1, out2):
# 		for x in range(self.input_num):
# 			self.weights[x] += self.step2_arr[x/self.hidden_node_num]*inputs[x]*big_theta(self.step2_arr[x/self.hidden_node_num],out1)*big_theta(out1, out2)

# 			if self.weights[x] > self.weight_range:
# 				self.weights[x] = self.weight_range

# 			if self.weights[x] < -self.weight_range:
# 				self.weights[x] = -self.weight_range

# 	def anti_hebbian_learning_rule(self, inputs, out1, out2):
# 		for x in range(self.input_num):
# 			self.weights[x] -= self.step2_arr[x/self.hidden_node_num]*inputs[x] * \
# 				big_theta(self.step2_arr[x/self.hidden_node_num],
# 				          out1)*big_theta(out1, out2)

# 			if self.weights[x] > self.weight_range:
# 				self.weights[x] = self.weight_range

# 			if self.weights[x] < -self.weight_range:
# 				self.weights[x] = -self.weight_range

# 	def random_walk(self, inputs, out1, out2):
# 		for x in range(self.input_num):
# 			self.weights[x] += inputs[x] * \
# 				big_theta(self.step2_arr[x/self.hidden_node_num],
# 				          out1)*big_theta(out1, out2)

# 			if self.weights[x] > self.weight_range:
# 				self.weights[x] = self.weight_range

# 			if self.weights[x] < -self.weight_range:
# 				self.weights[x] = -self.weight_range

# 	def print_weights(self):
# 		for x in self.weights:
# 			print(x)
