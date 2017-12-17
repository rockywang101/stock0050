'''
Created on 2017年12月15日
@author: rocky.wang
'''

# library & dataset
import seaborn as sns
import matplotlib

df = sns.load_dataset('iris')

print(df)
 
# Make default density plot
sns.kdeplot(df['sepal_length'])

matplotlib.pyplot.show()
