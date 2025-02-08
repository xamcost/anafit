import matplotlib.pyplot as plt
import numpy as np

import anafit

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
(my_line,) = ax.plot(
    np.arange(0, 100, 1),
    np.arange(50, 250, 2) + 10 * (np.random.rand(100) - 1 / 2),
    "+",
)
ax.plot(
    np.arange(0, 100, 1),
    np.arange(0, 300, 3) + 30 * (np.random.rand(100) - 1 / 2),
    "x",
)
ax.plot(
    np.arange(0, 100, 1),
    np.square(np.arange(0, 10, 0.1)) + 5 * (np.random.rand(100) - 1 / 2),
    ".",
)
ana = anafit.Figure(fig)
plt.show(block=True)
