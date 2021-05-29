#!/usr/bin/env python
# coding: utf-8

# ## Music Recommendation System (Data Processing and Analysis)

# ### Framing the Problem

# This project is aimed upon building a music recommendation system that gives the user recommendations on music based on his music taste by analysing his previously heard music and playlist. This project is done in two ways, using 'User - to - User Recommendation' and 'Item - to - Item Recommendation'. Birch, MiniBatchKMeans and KMeans algorithms are being used along with 'Surprise' module to compute the similarity between recommendations and user's already existing playlist for evaluation

# ### Obtaining Data

# In[1]:


# pip install missingno


# In[2]:


import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import seaborn as sns
import math
import missingno as ms
# %matplotlib inline


# In[3]:


pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 2000)


# In[4]:


echonest = pd.read_csv('echonest.csv')
features = pd.read_csv('features.csv')
genres = pd.read_csv('genres.csv')
tracks = pd.read_csv('tracks.csv')


# In[5]:


tracks.head()


# In[6]:


echonest.head()


# In[7]:


genres.head()


# In[8]:


features.head()


# ### Working with 'Echonest' dataset

# #### Analysing Data

# In[9]:


echonest.info()


# In[10]:


features.info()


# In[11]:


genres.info()


# In[12]:


tracks.info()


# In[13]:


echonest.head(10)


# #### Feature Engineering

# In[14]:


ms.matrix(echonest)


# In[15]:


echonest.drop(['echonest.8', 'echonest.9', 'echonest.15', 'echonest.16', 'echonest.17', 'echonest.18', 'echonest.19'], axis=1, inplace=True)


# In[16]:


echonest.tail(15)


# In[17]:


ms.matrix(echonest.iloc[:, 0:15])


# In[18]:


echonest.drop(['echonest.10', 'echonest.11', 'echonest.12'], axis=1, inplace=True)


# In[19]:


ms.matrix(echonest)


# In[20]:


echonest.head(10)


# In[21]:


echonest.drop(0, axis=0, inplace=True)


# In[22]:


echonest.iloc[0, 0]


# In[23]:


echonest.iloc[1, 0]


# In[24]:


echonest.iloc[0, 0] = echonest.iloc[1, 0]


# In[25]:


echonest.head()


# In[26]:


echonest.drop(2, axis=0, inplace=True)


# In[27]:


echonest.columns = echonest.iloc[0]


# In[28]:


echonest.head()


# In[29]:


echonest.drop(1, axis=0, inplace=True)


# In[30]:


echonest.head()


# In[31]:


echonest.reset_index(inplace=True)


# In[32]:


echonest.drop('index', inplace=True, axis=1)


# In[33]:


echonest.head()


# In[34]:


type(echonest['acousticness'][0])


# In[35]:


def convert_to_float(df, columns):
    for i in columns:
        df[i] = df[i].astype('float')
    return df


# In[36]:


echonest = convert_to_float(echonest, set(echonest.columns) - set(['track_id', 'artist_name', 'release']))


# In[37]:


echonest.head()


# In[38]:


echonest.info()


# ### Working with 'Features' dataset

# #### Analysing Data

# In[39]:


features.info()


# In[40]:


features.head(10)


# In[41]:


ms.matrix(features.iloc[:, 21:40])


# #### Feature Engineering

# In[42]:


features.iloc[0,0] = features.iloc[2, 0]


# In[43]:


features.head(3)


# In[44]:


features.drop(2, inplace=True)


# In[45]:


len(features.columns)


# In[46]:


len(features.iloc[0])


# In[47]:


def combine_two_rows(df):
    columns = list(df.columns)
    for i in range(0, 519):
        columns[i] = columns[i] + " " + df.iloc[0, i]
    return columns


# In[48]:


features.columns = combine_two_rows(features)


# In[49]:


features.drop([0, 1], inplace=True)


# In[50]:


features.reset_index(inplace=True)


# In[51]:


features.drop('index', axis=1, inplace=True)


# In[52]:


features.head()


# In[53]:


features = features.astype(dtype='float')
features['feature track_id'] = features['feature track_id'].astype('int')


# In[54]:


ms.matrix(features)


# In[55]:


features.head(3)


# ### Working with 'Tracks' dataset

# #### Analysing Data

# In[56]:


tracks.info()


# In[57]:


tracks.head()


# In[58]:


tracks.iloc[0,0] = tracks.iloc[1, 0]


# In[59]:


tracks.drop(1, axis=0, inplace=True)


# In[60]:


tracks.head()


# #### Feature Engineering

# In[61]:


len(tracks.columns)


# In[62]:


def combine_one_row(df):
    columns = list(df.columns)
    for i in range(0, 53):
        if i == 0:
            columns[i] = df.iloc[0, i]
        else:
            columns[i] = columns[i] + " " + df.iloc[0, i]
    return columns


# In[63]:


tracks.columns = combine_one_row(tracks)


# In[64]:


tracks.drop(0, inplace=True)


# In[65]:


tracks.reset_index(inplace=True)


# In[66]:


tracks.drop(['index'], axis=1, inplace=True)


# In[67]:


ms.matrix(tracks.iloc[0: 10])


# In[68]:


tracks.head()


# In[69]:


tracks['track.7 genre_top'].value_counts()


# In[70]:


track_title = pd.DataFrame(tracks['track.19 title'])


# In[71]:


track_title['track_id'] = tracks['track_id']


# In[72]:


track_title.head()


# In[73]:


track_title.tail()


# In[74]:


track_title.shape


# In[75]:


tracks.drop(['album comments','album.1 date_created', 
             'album.2 date_released', 'album.11 tracks', 
             'album.9 tags', 'album.8 producer', 'album.3 engineer', 'album.6 information',
             'artist active_year_begin', 'artist.1 active_year_end', 'artist.2 associated_labels',
             'artist.3 bio','artist.4 comments','artist.5 date_created', 'artist.7 id',
             'artist.8 latitude','artist.9 location','artist.10 longitude', 'artist.11 members',
             'artist.13 related_projects', 'artist.14 tags','artist.15 website','artist.16 wikipedia_page',
             'set.1 subset', 'track.1 comments', 'track.2 composer', 'track.3 date_created', 'track.4 date_recorded',
             'track.10 information', 'track.13 license', 'track.15 lyricist', 'track.17 publisher', 'track.18 tags',
             'track.19 title'], axis=1, inplace=True)


# In[76]:


tracks.info()


# In[77]:


ms.matrix(tracks)


# In[78]:


tracks['album.12 type'].value_counts()


# In[79]:


tracks['album.10 title'].value_counts()


# In[80]:


tracks['album.10 title'].fillna(method='ffill', inplace=True)


# In[81]:


tracks.drop(['track.12 language_code', 'album.12 type'], axis=1, inplace=True)


# In[82]:


tracks.drop('track.9 genres_all', axis=1, inplace=True)


# In[83]:


ms.matrix(tracks)


# In[84]:


tracks['track.8 genres'].unique()


# In[85]:


genres.info()


# In[86]:


type(tracks['track.7 genre_top'].iloc[27])


# In[87]:


def getList(cd):
    return cd[1:-1].split(',')


# In[88]:


for i in range(0, 106574):
    if type(tracks['track.7 genre_top'][i]) == float:
        genre_list = getList(str(tracks['track.8 genres'][i]))
        count = len(genre_list)
        title = ""
        for j in range(0, count):
            title = title + str(genres['title'][j]) + str('|')
        tracks['track.7 genre_top'][i] = title


# ### Working with 'Genre' dataset

# #### Analysing Data

# In[89]:


genres.info()


# In[90]:


ms.matrix(genres)


# In[91]:


genres.head()


# #### Feature Engineering

# Nothing to engineer!

# ### Combining all datasets into a single entity

# #### Analysing Data

# In[92]:


echonest.info()


# In[93]:


tracks.info()


# In[94]:


tracks.head()


# In[95]:


echonest.head()


# In[96]:


genres.info()


# In[97]:


features.info()


# #### Feature Engineering

# In[98]:


features.columns = ['track_id'] + list(features.columns[1:])


# In[99]:


features.head()


# In[100]:


type(echonest['track_id'].iloc[0])


# In[101]:


echonest['track_id'] = echonest['track_id'].astype('int')
tracks['track_id'] = tracks['track_id'].astype('int')


# In[102]:


features.sort_values(by='track_id', inplace=True)
tracks.sort_values(by='track_id', inplace=True)
echonest.sort_values(by='track_id', inplace=True)


# In[103]:


features.head()


# In[104]:


tracks.head()


# In[105]:


count = 0
for i in range(0, 106574):
    if features['track_id'][i] == tracks['track_id'][i]:
        count += 1
    else:
        print(features['track_id'][i], tracks['track_id'][i])


# In[106]:


final = pd.concat([features, tracks.drop('track_id', axis=1)], axis=1)


# In[107]:


final.shape


# In[108]:


final.head()


# In[109]:


echonest.tail(3)


# In[110]:


echonest.drop(['artist_name', 'release'], axis=1, inplace=True)


# In[111]:


tracks.tail(3)


# In[112]:


features.head(1)


# In[113]:


final = echonest.merge(final, on='track_id')


# In[114]:


final.shape


# In[115]:


ms.matrix(final)


# ### Analysing Data

# In[116]:


final.head()


# In[117]:


final.shape


# In[118]:


final.info()


# In[119]:


final.drop('track.8 genres', axis=1, inplace=True)


# In[120]:


final.shape


# In[121]:


final.head()


# In[122]:


final['track.7 genre_top'].value_counts()


# ### Feature Engineering

# In[123]:


def format_strings(x):
    if '-' in x:
        return ''.join(x.split('-'))
    if x.find('/'):
        return '|'.join(x.split('/'))
    return x


# In[124]:


def modifyString(serie, val):
    for i in range(0, val):
        if serie[i] == 'Old-Time / Historic':
            serie[i] = 'OldTime|Historic'
    return serie


# In[125]:


final['track.7 genre_top'] = modifyString(final['track.7 genre_top'], 13129)


# In[126]:


final['track.7 genre_top'] = final['track.7 genre_top'].apply(format_strings)


# In[127]:


final['track.7 genre_top'].value_counts()


# In[128]:


final.head()


# In[129]:


metadata = pd.DataFrame()


# In[130]:


metadata['track_id'] = final['track_id']


# In[131]:


metadata.shape


# In[132]:


track_title.shape


# In[133]:


track_title = track_title.set_index('track_id')


# In[134]:


track_title.head()


# In[135]:


track_title.index = [int(i) for i in track_title.index]


# In[136]:


track_title.head()


# In[137]:


metadata.head()


# In[138]:


metadata['album_title'] = final['album.10 title']


# In[139]:


metadata['artist_name'] = final['artist.12 name']


# In[140]:


metadata['genre'] = final['track.7 genre_top']


# In[141]:


metadata = metadata.set_index('track_id')


# In[142]:


metadata.tail()


# In[143]:


metadata.head()


# In[144]:


metadata['track_title'] = track_title.loc[metadata.index]['track.19 title']


# In[145]:


metadata.tail()


# In[146]:


metadata.head()


# In[147]:


len(metadata[metadata['genre'].isnull()])


# In[148]:


final.drop('album.10 title', axis=1, inplace=True)


# In[149]:


final.head()


# In[150]:


final.info()


# In[151]:


final.drop('artist.12 name', axis=1, inplace=True)


# In[152]:


final.info()


# In[153]:


final.head()


# In[154]:


k = final # Restore point # Removed Label Encoding


# In[155]:


final.head()


# In[156]:


final.drop('set split', axis=1, inplace=True)


# In[157]:


final.info()


# In[158]:


final.info()


# In[159]:


genres['title'].count()


# In[160]:


genre_dummy = pd.DataFrame(data= np.zeros((13129, 163)), columns= list(genres['title'].unique()))


# In[161]:


genre_dummy.head()


# In[162]:


genre_list = pd.Series(data= genre_dummy.columns)


# In[163]:


genre_list = modifyString(genre_list, 163)


# In[164]:


genre_list = genre_list.apply(format_strings)


# In[165]:


genre_dummy.columns= genre_list


# In[166]:


# columns converted successfully


# In[167]:


genre_list = list(genre_list)


# In[168]:


final


# In[169]:


for i in range(0, 13129):
    if '|' in final['track.7 genre_top'][i]:
        divided_list = str(final['track.7 genre_top'][i]).split('|')
        count = len(divided_list)
        for j in range(0, count):
            if divided_list[j] in genre_list:
                location = genre_list.index(divided_list[j])
                genre_dummy.iloc[i, location] = 1
    else:
        location = genre_list.index(final['track.7 genre_top'][i])
        genre_dummy.iloc[i, location] = 1


# In[170]:


genre_list.index(final['track.7 genre_top'][0])


# In[171]:


final.drop(['track.7 genre_top'], axis= 1, inplace= True)


# In[172]:


final = pd.concat([final, genre_dummy], axis= 1)


# In[173]:


final.head()


# ### Writing final data to .csv files

# In[174]:


import os

if not os.path.isdir(os.path.join('datasets','final')):
    os.makedirs(os.path.join('datasets','final'))
    
metadata.to_csv('datasets/final/metadata.csv')
final.to_csv('datasets/final/final.csv')


# In[ ]:




