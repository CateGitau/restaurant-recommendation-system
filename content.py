import numpy as np
import pandas as pd 
import sklearn
import streamlit as st

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

#path to data
toronto_URL= "/home/cate/Cate/restaurant-recommendation-system/data/new_toronto_data.csv"

#function to load in the data
@st.cache(persist=True, allow_output_mutation=True)
def load_data(url):
    data = pd.read_csv(url)
    return data

toronto_data = load_data(toronto_URL)

# Combining the text in Keywords and categories columns
#toronto_data['All_Keywords'] = toronto_data['categories'].str.cat(toronto_data['Keywords'],sep=", ")

# Formating the All_Keywords Column
toronto_data['All_Keywords'] = toronto_data['All_Keywords'].map(lambda x: str(x))
toronto_data['All_Keywords'] = toronto_data['All_Keywords'].map(lambda x: x.lower())

# Adding and Grouping Rows together by Restaurant Name
toronto_final = toronto_data.groupby('name')['All_Keywords'].sum()
toronto_final = toronto_final.to_frame(name = 'sum').reset_index()

# Getting a list of Unique Keywords per Restaurant

toronto_final['sum'] = toronto_final['sum'].map(lambda x: x.replace(", ","', '"))
toronto_final['sum'] = toronto_final['sum'].map(lambda x: str("'") + x + str("'"))
f = lambda x: x["sum"].split(", ")
toronto_final['sum'] = toronto_final.apply(f, axis=1)
toronto_final['sum'] = toronto_final['sum'].map(lambda x: set(x))
toronto_final.set_index('name', inplace = True)

# Creating Bag of Words
toronto_final['bag_of_words'] = ''
columns = toronto_final.columns
for index, row in toronto_final.iterrows():
    words = ''
    for col in columns:
            words = words + ' '.join(row[col])+ ' '
    row['bag_of_words'] = words
    
toronto_final.drop(columns = [col for col in toronto_final.columns if col!= 'bag_of_words'], inplace = True)

# Remove quotation marks
toronto_final['bag_of_words'] = toronto_final['bag_of_words'].map(lambda x: x.replace("'", ""))

# instantiating and generating the count matrix
count = CountVectorizer()
count_matrix = count.fit_transform(toronto_final['bag_of_words'])

# creating a Series for the restaurant names so they are associated to an ordered numerical
# list I will use later to match the indexes
indices = pd.Series(toronto_final.index)

# generating the cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# function that takes in restaurant name as input and returns the top 10 recommended restaurants
def content_based_recommendations(name, cosine_sim = cosine_sim):
    
    recommended_restaurants = []
    
    # gettin the index of the movie that matches the title
    idx = indices[indices == name].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        recommended_restaurants.append(list(toronto_final.index)[i])
        
    return recommended_restaurants