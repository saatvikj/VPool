# libraries
import numpy as np
import matplotlib.pyplot as plt
 
# width of the bars
barWidth = 0.3
 
# Choose the height of the blue bars
bars1 = [1.77496038, 2.124198641, 2.662490211]
 
# Choose the height of the cyan bars
bars2 = [1.776367962,2.128067485,2.679697352]
 
 
# The x position of bars
r1 = np.arange(len(bars1))
r2 = [x + barWidth for x in r1]
 
# Create blue bars
plt.bar(r1, bars1, width = barWidth, label='WVC', edgecolor = 'black', color='#5975A4')
 
# Create cyan bars
plt.bar(r2, bars2, width = barWidth, label='Standard Coloring', edgecolor = 'black', color='#CD8964')
 
# general layout
plt.xticks([r + barWidth for r in range(len(bars1))], ['Size 100','Size 200','Size 500'])
plt.ylabel('Average Occupants per Vehicle')
plt.legend()

# Show graphic
plt.show()