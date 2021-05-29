#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install factor_analyzer


# In[2]:


#All the header files required for the code
import numpy as np
import pandas as pd
from factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics
import random


# In[3]:


#Importing both the file using pandas 
data1 = pd.read_csv('movies data.csv')
data2 = pd.read_csv('ratings data.csv')


# In[4]:


#Deleting unnecessary columns
data1 = data1.drop('Unnamed: 0',axis = 1)
data2 = data2.drop(['Unnamed: 0','Timestamp'],axis = 1)


# In[5]:


data1.head()


# In[6]:


data2.head()


# In[7]:


#Merging both the dataframes
data = pd.merge(data2 , data1 , how='outer', on='MovieID')


# In[8]:


data.head()


# In[9]:


# Data Processing
# Converting Genres into different columns 
# Here we just create columns and put there initial value as 0
x = data.Genres
a = list()
for i in x:
    abc = i
    a.append(abc.split('|'))
a = pd.DataFrame(a)   
b = a[0].unique()
for i in b:
    data[i] = 0
data.head(2)


# In[10]:


# we assign 1 to all the columns which are present in the Genres
for i in b:
    data.loc[data['Genres'].str.contains(i), i] = 1


# In[11]:


data.head(2)


# In[12]:


# Now there is no use of genre 
# Since we have movie id so there is no need for movie names as well
data = data.drop(['Genres','Title'],axis =1)
data.head()


# In[13]:


data.columns


# In[14]:


# Because of merging some null values are created
data.isnull().sum()


# In[15]:


#WE simply drop the null values coz the are not treatable
data.dropna(inplace= True )


# In[16]:


data.isnull().sum()


# In[17]:


#By different meathods I found 8 cluster are better 
kmeanModel = KMeans(n_clusters=8)
kmeanModel.fit(data)


# In[18]:


# Creating an extra column in data for storing the cluster values
data['Cluster'] = kmeanModel.labels_
data['Cluster'].sample(n=10)


# In[19]:


data['Cluster'].value_counts()


# In[20]:


data.head()


# In[21]:


# When we merge the dataframe for a single movie multiple rows were created so a single movie is allotted
# to many clusters so here we allot a single cluster to a movie 
# the Cluster which occurs maximum number of times is alloted to the movie  
e = []
def fi(group):
    a = pd.DataFrame(group)
    b = pd.DataFrame(a['Cluster'].value_counts())
    d = a.index 
    c = [a['MovieID'][d[0]],int(b.idxmax())]
    e.append(c)
    


# In[22]:


data.groupby("MovieID").apply(lambda x: fi(x))


# In[23]:


e = pd.DataFrame(e)


# In[24]:


e.head()


# In[25]:


# I Dont know why always the column name shift according to its will :(
# Here just the column names are swapped
e.rename(columns = {0:'MovieID',1:'Cluster'},inplace=True)
e.drop_duplicates(inplace=True)


# In[26]:


e.head(10)


# In[27]:


data1 = pd.read_csv('movies data.csv')
new_data = pd.merge(e , data1 , how='outer', on='MovieID')


# In[28]:


# These were the movies we deleted while merging the file  
new_data.isnull().sum()


# In[29]:


# We can delete the movies but I just label them randomly :)
new_data.fillna(random.randint(0,8),inplace=True)


# In[30]:


new_data.isnull().sum()


# In[31]:


#This function select the cluster for a user according the the user choice
def select_c():
    global l
    print('Select The Movies Id you would like to watch:')
    l=[]
    for i in range(15):
        l.append(random.randint(0,3883))
    for i in l:
        print(new_data['MovieID'][i] , new_data['Title'][i],sep='--->')
    print('--------------------------------------------------------------------')
    l = int(input())
    l = new_data['Cluster'][new_data.MovieID == l]


# In[32]:


# This is the main function which recommend you movies
def main():
    ans = False
    while not ans:
        select_c()
        print(new_data['Title'][new_data.Cluster == int(l)].sample(n=10))
        print('--------------------------------------------------------------------')
        print('Do you like these movies(y/n)')
        abc = input()
        while ((abc =='y') or (abc == 'Y')):          
            print(new_data['Title'][new_data.Cluster == int(l)].sample(n=10))
            print('--------------------------------------------------------------------')
            print('Want more!!!!(y/n)')
            abc = input()
            if ((abc =='N') or (abc == 'n')):
                ans =True


# In[33]:


main()


# In[ ]:




