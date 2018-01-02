
import matplotlib.pyplot as plt

# squares = [1, 4, 6, 6, 6, 45]
# plt.plot(squares, linewidth=7)
# plt.title("matplotlib", fontsize=23)
# plt.xlabel('x轴', fontsize=23)
# plt.xlabel('y轴', fontsize=23)
# plt.tick_params(axis='both', labelsize=23)
# plt.show()

import re

res1 = re.compile("[a-zA-Z]+://[\S]*[.com|.cn]").findall('https://www.cnblogs.com/dreamer-fish/p/5282679.html')
print(res1)