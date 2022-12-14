# -*- coding: utf-8 -*-
"""лаба 4

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c0lpOYj55CQ0G1YvGzVeRao-z5kaTEQD
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl


import pandas as pd
import pathlib
from pathlib import Path

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

ave_file = "/content/titanic2.csv"

df = pd.read_csv(ave_file, sep=',')
#print(df.head())
df.head()

df#вывод всей таблицы

print(df.info())#вывод столбцов

male=df[(df['Sex'] == 'male')]#количество выживших и умерших мужчин
res1 = male.groupby(['Survived'])['Survived'].count()
plt.pie(res1, labels=res1.index)
plt.title('Die and life male')
plt.show()
print(res1)

female=df[(df['Sex'] == 'female')]#количество выживших и умерших женщин
res2 = female.groupby(['Survived'])['Survived'].count()
plt.pie(res2, labels=res2.index)
plt.title('Die and life female')
plt.show()
print(res2)

die=df[(df['Survived'] == 0) ]
non_die=df[(df['Survived'] == 1)]

res7 = die.groupby(['Pclass'])['Pclass'].count()
res8 = non_die.groupby(['Pclass'])['Pclass'].count()

plt.pie(res7, labels=res7.index)
plt.title ('die')
plt.legend()
plt.show()
print(res7)

die.hist(column='Pclass')
plt.title ('die')
plt.xlabel('Pclass')
plt.ylabel('number')

plt.pie(res8, labels=res8.index)
plt.title ('life')
plt.legend()
print(res8)