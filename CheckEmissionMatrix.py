import numpy as np
emission = np.load("EmissionMatrix.npy")
print(emission)
print("emission matrix shows b_j(v_k) = P(o_t=v_k|q_t=j)")
print("where o_t is observation at time t")
print("where q_t is state at time t")
print("row B state sum:",np.sum(emission[0]))
print("row E state sum:",np.sum(emission[1]))
print("row M state sum:",np.sum(emission[2]))
print("row S state sum:",np.sum(emission[3]))

