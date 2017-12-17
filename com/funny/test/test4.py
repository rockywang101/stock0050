'''
Created on 2017年12月15日

@author: Eit
'''
# Import the necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
tips = sns.load_dataset("tips")

print(tips)

# Create violinplot
sns.violinplot(x="total_bill", data=tips)

# Show the plot
plt.show()