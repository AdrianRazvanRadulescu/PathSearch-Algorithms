# pentru variantele de le glds si Beam 50 pe easy timp rulare

import numpy as np
import matplotlib.pyplot as plt

data_1 = []



fig = plt.figure(figsize =(10, 7))


# Creating axes instance
ax = fig.add_axes([0, 0, 1, 1])

# Creating plot
bp = ax.boxplot(data)

# show plot
plt.show()