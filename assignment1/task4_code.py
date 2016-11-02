import random
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
a = []
SIN = []
COSIN = []
for i in xrange(10):
    a.append('%04.3f' % random.uniform(0,90))
for item in a:
	COSIN.append(math.cos(float(item)))
	SIN.append(math.sin(float(item)))
plt.plot(SIN,'-b', label='Sin')
plt.plot(COSIN,'-r', label='Cosine')
plt.axis()
plt.ylabel('y axis')
plt.xlabel('x axis')
plt.legend(loc='lower right')
plt.show()