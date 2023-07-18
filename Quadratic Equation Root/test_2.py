import matplotlib.pyplot as plt

a=[]
b=[]
# y=0
# x=-50

for x in range(-50,50,1):
    y=x**2+2*x+2
    a.append(x)
    b.append(y)
    #x= x+1

fig= plt.figure()
axes=fig.add_subplot(111)
axes.plot(a,b)
plt.show()