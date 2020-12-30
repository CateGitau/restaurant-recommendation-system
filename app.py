import streamlit as st
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
pd.set_option('display.max_columns', 50)

# Importing Plotly Packages

import plotly 
import plotly.offline as py
import plotly.graph_objs as go
import plotly_express as px

#importing python scripts
KM = __import__("cluster")
COL = __import__("recommender")
#CONT = __import__("content")


st.title("Toronto Restaurant Recommendation platform")
st.markdown("This application is for recommending restaurants to visit for users in Toronto  🍔🍕🍹🍺")


st.sidebar.title("Toronto Restaurant Recommendation platform")
st.sidebar.subheader("Africa DSI Capstone Project")
st.sidebar.markdown("By: Catherine Gitau")
st.sidebar.markdown("This application is for recommending restaurants to visit for users in Toronto  🍔🍕🍹🍺")

business_URL= "/home/cate/Cate/recommender_system/business_final.csv"
final_URL="/home/cate/Cate/recommender_system/final_reviews.csv"

@st.cache(persist=True)
def load_data(url):
    data = pd.read_csv(url)
    return data

def main():

    st.sidebar.markdown("### Recommendation type")
    section = st.sidebar.selectbox('choose recommendation type', ['Pick a Value', 'Location based', 'Collaborative Filtering', 'Content-based'], key= 1)

    #fig.update_layout(mapbox_style="dark")
    #fig.show()

    if section == "Pick a Value":
        st.markdown("## How to get the most out of this platform")
        st.markdown("- If you're a new user of this platform or in this city and you have never tried any restaurant around toronto, please select the **location based** recommender on the sidebar to get recommended top restaurants around where you are.")
        st.markdown("- If you know exactly what kind of restaurant you would like to visit please select **content based** recommendation type.")
        st.markdown("- If this isn't your first time using this platform and would like to get recommendations based on previous restaurants you have visited please select the **collaborative filtering** option on the sidebar.")


        st.subheader("Graphical Overview of Restaurants in Toronto City")
        px.set_mapbox_access_token("pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w")
        fig = px.scatter_mapbox(load_data(business_URL), lat="latitude", lon="longitude", color="stars", size='review_count',
                        size_max=15, zoom=10, width=1000, height=700)
        st.plotly_chart(fig)

    if section == "Location based":
        st.subheader('Location Based Recommendation System')

        st.markdown("please enter your longitude and latitude")
        latitude = st.text_area('Input your latitude here')
        longitude = st.text_area('Input your longitude here')
        

        if latitude and longitude:
            df = KM.location_based_recommendation(business_URL, latitude, longitude)
            st.write(df)

            st.markdown("## Geographical Plot of Nearby Recommended Restaurants from Royal Ontario Museum")
            px.set_mapbox_access_token("pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w")
            fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",  
                            zoom=10, width=1000, height=700, hover_data= ['name', 'latitude', 'longitude', 'categories', 'stars', 'review_count'])
            fig.add_scattermapbox(lat=[latitude], lon=[longitude]).update_traces(dict(mode='markers', marker = dict(size = 15)))
            fig.update_layout(mapbox_style="dark")
            st.plotly_chart(fig)

    if section == 'Collaborative Filtering':
        st.subheader("Collaborative Filtering Recommendation System")

        st.markdown("please select a restaurant you've visited before")
        restaurant = st.selectbox('select restaurant', ['Pai Northern Thai Kitchen', 'Sabor Del Pacifico'])

        if restaurant:
            restaurant_recommendations = COL.cf_recommender(restaurant)
            restaurant_recommendations = pd.DataFrame(data = restaurant_recommendations)

            st.write(restaurant_recommendations)

    if section == 'Content-based Recommendation System':
        st.subheader('Content based recommendation system')
        st.markdown("please select a restaurant similar to the one you'd like to visit")
        restaurant = st.selectbox('select restaurant', ['Pai Northern Thai Kitchen', 'Sidewalk'])

        # if restaurant:
        #     restaurant_recommendations = content_based_recommendations(restaurant)
        #     restaurant_recommendations = pd.DataFrame(data = restaurant_recommendations)

        #     st.write(restaurant_recommendations)

if __name__ == "__main__":
    main()
