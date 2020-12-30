import numpy as np
import pandas as pd 
import sklearn
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

# Importing scipy Packages
from scipy.sparse.linalg import svds

SC = __import__("super_score")

#path to data
business_URL= "/home/cate/Cate/recommender_system/business_final.csv"
reviews_URL = "/home/cate/Cate/recommender_system/final_reviews.csv"

#function to load in the data
@st.cache(persist=True)
def load_data(url):
    data = pd.read_csv(url)
    return data

final_reviews = load_data(reviews_URL)
final_reviews = final_reviews.drop('Unnamed: 0', axis = 1)
business_final = load_data(business_URL)
#add score to dataframe
reviews_df = SC.score(final_reviews)

business_final = business_final.rename(columns = {"business_id ":"business_id"}) 

final_df = reviews_df[['business_id', 'user_id', 'super_score', 'Keywords']]
toronto_restaurant =  business_final[['business_id', 'name', 'categories']]

# Merging Dataframes
toronto_data = pd.merge(final_df, toronto_restaurant, on='business_id')

# Combining the text in Keywords and categories columns
toronto_data['All_Keywords'] = toronto_data['categories'].str.cat(toronto_data['Keywords'],sep=", ")

# Creating the Matrix by using the Pivot Table Function
toronto_restaurant_rating = toronto_data.pivot_table(index = 'user_id', columns = 'name', values = 'super_score')

# Normalizing the Rating Scores
@st.cache(persist=True)
def mean_center_rows(df):
    return (df.T - df.mean(axis = 1)).T

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


# Creating Item-Item Matrix based on Cosine Similarity
item_item_matrix = cosine_similarity(cf_preds_df)
item_item_matrix= pd.DataFrame(item_item_matrix, columns=cf_preds_df.index, index = cf_preds_df.index)

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