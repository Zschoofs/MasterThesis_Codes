import matplotlib.pyplot as plt
import pandas as pd


#var = pd.read_excel("onecornertwomotions.xlsx") # -> 0.63, 0.12
#var = pd.read_excel("onlyonesidetwomotions.xlsx") # -> 0.0, 0.02
#var = pd.read_excel("crossingtwomotions.xlsx") # -> 0.6, 0.45
#var = pd.read_excel("twopersoncrossing.xlsx") # -> 1.0 , 1.0
#var = pd.read_excel("twopersononlyone.xlsx") # -> 0.15 , 1.0
#var = pd.read_excel("twopersononeside.xlsx") # -> 1.0 , 0.52
var = pd.read_excel("test.xlsx") # ->

print(var['Motion1'].corr(var['Motion2']))

y = list(var['Motion1'].fillna(0))
y2 = list(var['Motion2'].fillna(0))


x = list(var['Seconds'])
count1 = 0 #number of time that mot2 actvate after mot1
mot1 = 0 #number of mot1 activate
count2 = 0 #number of time mot1 activate after mot2
mot2 =0 #number of mot2 activation
prob1=0 #prob that mot 2 is in the same room as mot1
prob2=0  #prof that mot 1 is in the same room as mot2

tresh=14 #number of seconds to cross the room (adjusted to have better proba)
i=0
#probability that motion 2 is activated after mot1
while i < len(x) :
    if y[i] > 0 : #detection on motion1
        mot1 = mot1+1
        j=0
        while j < tresh and i+j < len(x) :
            if y2[i+j]> 0 :
                count1= count1 +1
                i=i+j
                break
            j=j+1
    i = i +1

k=0
#probability that motion 1 is activate after mot2
while k < len(x) :
    if y2[k] > 0 : #detection on motion2
        mot2= mot2+1
        j = 0
        while j < tresh and k+j < len(x):
            if y[k+j] > 0 :
                count2 = count2 +1
                k=k+j
                break
            j=j+1
    k = k+1

prob1=count1/mot1
prob2=count2/mot2
#print(mot1)
#print(count1)
#print(mot2)
#print(count2)
print(prob1)
print(prob2)