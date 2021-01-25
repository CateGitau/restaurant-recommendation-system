import numpy as np
import pandas as pd 
import sklearn
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

# Importing scipy Packages
from scipy.sparse.linalg import svds

SC = __import__("super_score")

#path to data
toronto_URL= "/home/cate/Cate/recommender_system/data/new_toronto_data.csv"

#function to load in the data
@st.cache(persist=True)
def load_data(url):
    data = pd.read_csv(url)
    return data

@st.cache(persist=True)
def mean_center_rows(df):
    return (df.T - df.mean(axis = 1)).T

@st.cache(persist=True)
def cos_matrix(data):
    # Combining the text in Keywords and categories columns
    # data['All_Keywords'] = data['categories'].str.cat(data['Keywords'],sep=", ")

    # Creating the Matrix by using the Pivot Table Function
    toronto_restaurant_rating = data.pivot_table(index = 'user_id', columns = 'name', values = 'super_score')

    # Normalizing the Rating Scores
    toronto_restaurant_rating = mean_center_rows(toronto_restaurant_rating)

    # Filling all Null Values with 0.0
    toronto_restaurant_rating = toronto_restaurant_rating.fillna(0)

    #cosine similarity

    # List of first 10 Yelp Customer User_ids in the Matrix
    user_ids = list(toronto_restaurant_rating.index)

    # Converting the Matrix DataFrame into a NumPy array
    toronto_matrix = toronto_restaurant_rating.to_numpy()

    # Applying Singular Value Decomposition (SVD)
    #The number of factors to factor the user-item matrix.
    NUMBER_OF_FACTORS_MF = 15

    #Performs matrix factorization of the original user item matrix
    U, sigma, Vt = svds(toronto_matrix, k = NUMBER_OF_FACTORS_MF)

    sigma = np.diag(sigma)

    # Overview of user ratings across all Restaurants in Toronto
    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) 

    # Converting the reconstructed matrix back to a Pandas dataframe
    cf_preds_df = pd.DataFrame(all_user_predicted_ratings, columns = toronto_restaurant_rating.columns, index=user_ids).transpose()

    return cf_preds_df

@st.cache(persist=True)
def item_matrix()):
    # Creating Item-Item Matrix based on Cosine Similarity
    item_item_matrix = cosine_similarity(cf_preds_df)
    item_item_matrix= pd.DataFrame(item_item_matrix, columns=cf_preds_df.index, index = cf_preds_df.index)

    return item_item_matrix

toronto_data = load_data(toronto_URL)
cf_preds_df = cos_matrix(toronto_data)
item_item_matrix = item_matrix()


# Creating Collaborative Filtering Function for Restaurant-Restaurant Recommendation System
def cf_recommender(restaurant):
    
    """Getting the correlation of a specific restaurant with other Toronto Restaurants"""
    restaurant_ratings = cf_preds_df.T[restaurant]
    similar_restaurant_ratings = cf_preds_df.T.corrwith(restaurant_ratings)
    corr_ratings = pd.DataFrame(similar_restaurant_ratings, columns=['Correlation'])
    corr_ratings.dropna(inplace=True)
    
    """Retrieving the Ratings Scores from the Item-Item Matrix"""
    ratings_sim = item_item_matrix[restaurant]
    
    """Filtering for positively correlated restaurants"""
    ratings_sim = ratings_sim[ratings_sim>0]
    
    """Generate Top 10 Recommended Restaurants"""
    """Exclude top row as that will be the same restaurant"""
    return ratings_sim.sort_values(ascending= False).head(11)[1:]