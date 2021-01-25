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

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap


from plotly.subplots import make_subplots
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

#importing python scripts
KM = __import__("cluster")
LOC= __import__("location")
CT = __import__("content")
#CF = __import__("collaborate")


st.title("Toronto Restaurant Recommendation platform")
st.markdown("This application is for recommending restaurants to visit for users in Toronto  🍔🍕🍹🍺")


st.sidebar.title("Toronto Restaurant Recommendation platform")
st.sidebar.subheader("Africa DSI Capstone Project")
st.sidebar.markdown("By: Catherine Gitau")
st.sidebar.markdown("This application is for recommending restaurants to visit for users in Toronto  🍔🍕🍹🍺")

business_URL= "/home/cate/Cate/restaurant-recommendation-system/data/business_final.csv"
final_URL="/home/cate/Cate/restaurant-recommendation-system/data/final_reviews.csv"
toronto_URL= "/home/cate/Cate/restaurant-recommendation-system/data/new_toronto_data.csv"


@st.cache(persist=True, allow_output_mutation=True)
def load_data(url):
    data = pd.read_csv(url)
    return data

def clean(data):
    data.drop(['Unnamed: 0'], axis=1, inplace = True)
    data['business_id'] = data['business_id ']
    data = data[['business_id', 'name', 'categories','stars','review_count','latitude','longitude','postal_code']]
    return data

business_data = load_data(business_URL)
toronto_data = load_data(toronto_URL)
final_reviews = load_data(final_URL)

# st.write(all_data.head())

# create a list of our conditions
toronto_data['super_score'] = toronto_data['super_score'].round(0)
conditions = [
    (toronto_data['super_score'] <=2),
    (toronto_data['super_score'] == 3),
    (toronto_data['super_score'] >= 4)
    ]

# create a list of the values we want to assign for each condition
values = ['negative', 'neutral', 'positive']

# create a new column and use np.select to assign values to it using our lists as arguments
toronto_data['sentiment'] = np.select(conditions, values)

@st.cache(persist=True)
def plot_sentiment(restaurant):
    df = toronto_data[toronto_data['name']==restaurant]
    count = df['sentiment'].value_counts()
    count = pd.DataFrame({'Sentiment':count.index, 'text':count.values.flatten()})
    return count

def main():
    st.sidebar.markdown("### Recommendation type")
    section = st.sidebar.selectbox('choose recommendation type', ['Pick a Value', 'Location based', 'Content based', 'Collaborative Filtering'], key= 1)

    #fig.update_layout(mapbox_style="dark")
    #fig.show()
    # 
        

    if section == "Pick a Value":
        st.markdown("## How to get the most out of this platform")
        st.markdown('This platform contains 3 recommendation system models to recommend to you restaurants based on Yelp reviews in Toronto city')
        st.markdown("- If you're a new user of this platform or in this city and you have never tried any restaurant around toronto, please select the **location based** recommender on the sidebar to get recommended top restaurants around where you are.")
        st.markdown("- If you want recommendations of restaurants similar to one you have previously visited and liked, please select **content-based** on the sidebar.")
        st.markdown("- If this isn't your first time using this platform and would like to get recommendations based on previous restaurants you have visited and rated please select the **collaborative filtering** option on the sidebar.")
        #st.markdown("- If you just want to compare the ratings of different restaurants you have in mind, please select **Restaurant Analytics** on the sidebar.")


        st.subheader("Graphical Overview of Restaurants in Toronto City")
        px.set_mapbox_access_token("pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w")
        fig = px.scatter_mapbox(business_data, lat="latitude", lon="longitude", color="stars", size='review_count',
                        size_max=15, zoom=10, width=1000, height=700)
        st.plotly_chart(fig)

    if section == "Location based":

        st.subheader('Location Based Recommendation System')

        st.markdown("please enter your location")
        location = st.text_area('Input your location here')

        if location:
            URL = "https://geocode.search.hereapi.com/v1/geocode"
            api_key = 'ODfYgIX45wrL41qboC3F_z2hg8e5_ABJYi71Pu6o948' # Acquire from developer.here.com
            PARAMS = {'apikey':api_key,'q':location}

            lat_long = LOC.get_location(URL, PARAMS)
            latitude = lat_long[0]
            longitude = lat_long[1]
            df = KM.location_based_recommendation(business_data, latitude, longitude)

            if st.sidebar.checkbox("Show data", False):
                st.write(df)

            st.markdown("## Geographical Plot of Nearby Recommended Restaurants from "+ location)
            px.set_mapbox_access_token("pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w")
            fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",  
                            zoom=10, width=1000, height=700, hover_data= ['name', 'latitude', 'longitude', 'categories', 'stars', 'review_count'])
            fig.add_scattermapbox(lat=[latitude], lon=[longitude]).update_traces(dict(mode='markers', marker = dict(size = 15)))
            fig.update_layout(mapbox_style="dark")
            st.plotly_chart(fig)
    
    if section == 'Content based':
        st.subheader('Content based recommendation system')
        st.markdown("please select a restaurant similar to the one you'd like to visit")
        restaurant = st.selectbox('select restaurant',toronto_data['name'].unique())

        if restaurant:
            restaurant_recommendations = CT.content_based_recommendations(restaurant)
            restaurant1 = toronto_data[toronto_data['name'] == restaurant_recommendations[0]][['name','categories','super_score']].groupby(['name', 'categories'], as_index=False).mean()
            restaurant2 = toronto_data[toronto_data['name'] == restaurant_recommendations[1]][['name','categories','super_score']].groupby(['name', 'categories'], as_index=False).mean()
            restaurant3 = toronto_data[toronto_data['name'] == restaurant_recommendations[2]][['name','categories','super_score']].groupby(['name', 'categories'], as_index=False).mean()
            restaurant4 = toronto_data[toronto_data['name'] == restaurant_recommendations[3]][['name','categories','super_score']].groupby(['name', 'categories'], as_index=False).mean()
            restaurant5 = toronto_data[toronto_data['name'] == restaurant_recommendations[4]][['name','categories','super_score']].groupby(['name', 'categories'], as_index=False).mean()


            rest_merged = pd.concat([restaurant1.head(1), restaurant2.head(1), restaurant3.head(1), restaurant4.head(1), restaurant5.head(1)])
            st.write(rest_merged)

        # st.subheader('Collaborative Filtering recommendation system')

        # if restaurant:
        #     collab_recommendations = content_based_recommendations(restaurant)
        #     collab_recommendations = pd.DataFrame(data = restaurant_recommendations)

        #     st.write(restaurant_recommendations)


        if section != 'Pick a Value':
            if st.sidebar.checkbox("Compare restaurants by sentiments", False):
                choice = st.sidebar.multiselect('Pick restaurants', toronto_data['name'].unique())
                if len(choice) > 0:
                    st.subheader("Breakdown restaurant by sentiment")
                    fig_3 = make_subplots(rows=1, cols=len(choice), subplot_titles=choice)
                    for i in range(1):
                        for j in range(len(choice)):
                            fig_3.add_trace(
                                go.Bar(x=plot_sentiment(choice[j]).Sentiment, y=plot_sentiment(choice[j]).text, showlegend=False),
                                row=i+1, col=j+1
                            )
                    fig_3.update_layout(height=600, width=800)
                    st.plotly_chart(fig_3)

                # st.write(toronot_data.head())
                # st.sidebar.header("Word Cloud")
                # word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))
                # if not st.sidebar.checkbox("Close", True, key='3'):
                #     st.subheader('Word cloud for %s sentiment' % (word_sentiment))
                #     df = toronto_data[toronto_data['sentiment']==word_sentiment]
                #     words = ' '.join(df['text'])
                #     processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
                #     wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
                #     plt.imshow(wordcloud)
                #     plt.xticks([])
                #     plt.yticks([])
                #     st.pyplot()
           

    # if section == 'Collaborative Filtering':
    #     st.subheader("Collaborative Filtering Recommendation System")

    #     st.markdown("please select a restaurant you've visited before")
    #     restaurant = st.selectbox('select restaurant', ['Pai Northern Thai Kitchen', 'Sabor Del Pacifico'])


        
   

if __name__ == "__main__":
    main()
