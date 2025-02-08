import matplotlib.pyplot as plt
import numpy as np

import anafit

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
x = np.arange(0.1, 100, 0.1)
(my_line,) = ax.loglog(x, x**2, "+")
ax.loglog(x, (x * (1 + np.random.rand(999) - 1 / 2)) ** 3.5, "+")
ax.loglog(x, (x * (1 + np.random.rand(999) - 1 / 2)) ** (-1), "+")
ana = anafit.Figure(fig)
plt.show(block=True)
