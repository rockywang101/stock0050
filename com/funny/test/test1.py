'''



Created on 2017年12月14日
@author: rocky.wang
'''

#FV-年金終值 、PV-年金現值、i-利率、n-期數

#FV= PV x {[ (1+ i ) ^n - 1 ] / i }

i = 0.12
n = 50
pv = 12 * 10000

v = pow(1+i, n) - 1
print(format(v, ".2f"))
v = v / i
print(format(v, ".2f"))
v = pv * v
print(format(v, ".2f"))


print()
i = 0.01
n = 120
pv = 10000

v = pow(1+i, n) - 1
print(format(v, ".2f"))
v = v / i
print(format(v, ".2f"))
v = pv * v
print(format(v, ".2f"))


"""
你的投資到期總金額為：2240359元
投資成本為：1212000元
投資獲利為：1028359元
"""


