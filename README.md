# restaurant recommendation system

This project is my Capstone project for the DSI 2020 training. The aim of the project is to create a restaurant recommender system that will be able to give suggestions of restaurants to users based on the restaurants reviews and previous restaurants the user has been to. 

There are three product features/ models for the system:
- Location based recommender system
- Content based recommender system
- Collaborative filtering recommender system



## Summary

 - [Getting Started](#getting-started)
 - [Deployment](#deployment)
 - [Challenges](#Challenges)
 - [Authors](#authors)
 - [License](#license)
 - [Acknowledgments](#acknowledgments)


### Getting Started
 To get this project up and running in your machine, follow the steps below:

 - Clone this repository to your local machine by opening your terminal and typing:
 ```
 git clone https://github.com/CateGitau/restaurant-recommendation-system
 ```

 - install the required packages:
 ```
 pip3 install -r requirements.txt
 ```

 - Run the app.py file to get the project running in your local machine using Streamlit
 ```
 streamlit run app.py
 ```

 ### Deployment
 We used [streamlit sharing](https://www.streamlit.io/sharing) to deploy the application. All you have to do is send a request to get an invite so that you start sharing the app then follow the instructions given.

 ### Challenges
 The operations that are being done when the `app.py` is run takes up a lot of RAM therefore could not accommodate both content and collaborative models, if you find a fix for this please feel free to send in a PR.

 ### Authors
 - [Catherine Gitau](https://github.com/CateGitau)

 ### License
 [MIT](https://mit-license.org/)

 ### acknowledgements
  We'd like to thank [Evandar Nyoni](https://github.com/Evandernyoni) who was my Tutor for the duration of this project.