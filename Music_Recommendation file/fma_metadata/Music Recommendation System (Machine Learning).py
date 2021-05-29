#!/usr/bin/env python
# coding: utf-8

# ## Music Recommendation System (Machine Learning)

# This project is aimed upon building a music recommendation system that gives the user recommendations on music based on his music taste by analysing his previously heard music and playlist. This project is done in two ways, using 'User - to - User Recommendation' and 'Item - to - Item Recommendation'. Birch, MiniBatchKMeans and KMeans algorithms are being used along with 'Surprise' module to compute the similarity between recommendations and user's already existing playlist for evaluation

# ### Obtaining Data

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


final = pd.read_csv('datasets/final/final.csv')
metadata = pd.read_csv('datasets/final/metadata.csv')


# ### Model Selection - K Means Algorithm

# In[3]:


from sklearn.cluster import KMeans
from sklearn.utils import shuffle


# In[4]:


final = shuffle(final)


# In[5]:


X = final.loc[[i for i in range(0, 6000)]]
Y = final.loc[[i for i in range(6000, final.shape[0])]]


# In[6]:


X = shuffle(X)
Y = shuffle(Y)


# In[7]:


metadata.head()


# In[8]:


metadata = metadata.set_index('track_id')


# In[9]:


# X.drop(['label'], axis= 1, inplace= True)


# In[10]:


kmeans = KMeans(n_clusters=6)


# In[11]:


# data['Cluster'] = kmeans.labels_
# data['Cluster'].sample(n=10)


# In[12]:


Y.head()


# In[13]:


def fit(df, algo, flag=0):
    if flag:
        algo.fit(df)
    else:
         algo.partial_fit(df)          
    df['label'] = algo.labels_
    return (df, algo)


# In[14]:


def predict(t, Y):
    y_pred = t[1].predict(Y)
    mode = pd.Series(y_pred).mode()
    return t[0][t[0]['label'] == mode.loc[0]]


# In[15]:


def recommend(recommendations, meta, Y):
    dat = []
    for i in Y['track_id']:
        dat.append(i)
    genre_mode = meta.loc[dat]['genre'].mode()
    artist_mode = meta.loc[dat]['artist_name'].mode()
    return meta[meta['genre'] == genre_mode.iloc[0]], meta[meta['artist_name'] == artist_mode.iloc[0]], meta.loc[recommendations['track_id']]


# In[16]:


t = fit(X, kmeans, 1)


# In[17]:


recommendations = predict(t, Y)


# In[18]:


output = recommend(recommendations, metadata, Y)
output


# In[19]:


genre_recommend, artist_name_recommend, mixed_recommend = output[0], output[1], output[2]


# In[20]:


genre_recommend.shape


# In[21]:


artist_name_recommend.shape


# In[22]:


mixed_recommend.shape


# In[23]:


# Genre wise recommendations
genre_recommend.head()


# In[24]:


# Artist wise recommendations
artist_name_recommend.head()


# In[25]:


# Mixed Recommendations
mixed_recommend.head()


# In[26]:


recommendations.head()


# In[27]:


artist_name_recommend['artist_name'].value_counts()


# In[28]:


genre_recommend['genre'].value_counts()


# In[29]:


genre_recommend['artist_name'].value_counts()


# #### Testing

# In[30]:


testing = Y.iloc[6:12]['track_id']


# In[31]:


testing


# In[32]:


ids = testing.loc[testing.index]


# In[33]:


songs = metadata.loc[testing.loc[list(testing.index)]]


# In[34]:


songs


# In[35]:


re = predict(t, Y.iloc[6:12])


# In[36]:


output = recommend(re, metadata, Y.iloc[6:12])


# In[37]:


ge_re, ge_ar, ge_mix = output[0], output[1], output[2]


# In[38]:


ge_re.head()


# In[39]:


ge_ar.head(10)


# In[40]:


ge_mix.head(10)


# In[41]:


ge_re.shape


# In[42]:


ge_ar.shape


# In[43]:


ge_mix.shape


# ### Model Selection - MiniBatchKMeans

# In[44]:


from sklearn.cluster import MiniBatchKMeans


# In[45]:


mini = MiniBatchKMeans(n_clusters = 6)


# In[46]:


X.drop('label', axis=1, inplace=True)


# In[47]:


# Let's divide the intital dataset into pieces to demonstrate online learning
part_1, part_2, part_3 = X.iloc[0: 2000], X.iloc[2000:4000], X.iloc[4000:6000]


# In[48]:


for i in [part_1, part_2, part_3]:
    t = fit(i, mini)
    mini = t[1]
    i = t[0]


# In[49]:


X = pd.concat([part_1, part_2, part_3])


# In[50]:


X.columns


# In[51]:


X.head(3)


# In[52]:


X['label'].value_counts()


# In[53]:


recommendations = predict((X, mini), Y)


# In[54]:


output = recommend(recommendations, metadata, Y)


# In[55]:


genre_recommend_mini, artist_name_recommend_mini, mixed_mini = output[0], output[1], output[2]


# In[56]:


genre_recommend_mini.shape


# In[57]:


artist_name_recommend_mini.shape


# In[58]:


# Genre wise recommendations
genre_recommend_mini.head()


# In[59]:


# Artist wise recommendations
artist_name_recommend_mini.head()


# In[60]:


# Mixed Recommendations
mixed_mini.head()


# ### Model Selection - Birch

# In[61]:


from sklearn.cluster import Birch


# In[62]:


birch = Birch(n_clusters = 6)


# In[63]:


X.drop('label', axis=1, inplace=True)


# In[64]:


# Let's divide the intital dataset into pieces to demonstrate online learning
part_1, part_2, part_3 = X.iloc[0: 2000], X.iloc[2000:4000], X.iloc[4000:6000]


# In[65]:


for i in [part_1, part_2, part_3]:
    t = fit(i, birch)
    mini = t[1]
    i = t[0]


# In[66]:


X = pd.concat([part_1, part_2, part_3])


# In[67]:


X.columns


# In[68]:


X.head(3)


# In[69]:


X['label'].value_counts()


# In[70]:


recommendations = predict((X, birch), Y)


# In[71]:


output = recommend(recommendations, metadata, Y)


# In[72]:


genre_recommend_birch, artist_name_recommend_birch, mixed_birch = output[0], output[1], output[2]


# In[73]:


genre_recommend_birch.shape


# In[74]:


artist_name_recommend_birch.shape


# In[75]:


# Genre wise recommendations
genre_recommend_birch.head()


# In[76]:


# Artist wise recommendations
artist_name_recommend_birch.head()


# In[77]:


# Mixed Recommendations
mixed_birch.head()

