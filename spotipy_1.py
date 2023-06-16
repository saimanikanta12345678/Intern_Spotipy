import streamlit as st
from IPython.display import HTML
import base64
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime
st.set_page_config(layout="wide")


st.markdown('<p class="head">Music is Everything and Everywhere</p>', unsafe_allow_html=True)

color='#f0f0f0'
# container = st.container()
#
# # Add a heading to the container
# container.markdown('<p class="head">Music is Everything and Everywhere</p>',unsafe_allow_html=True)
# st.markdown()
st.markdown("""
<style>
    .melody{
font-size:45px !important;
# font-family:sans-serif;
color:white;
text-align:left;
}
.greet1{
font-size:45px !important;
font-family:Comic Sans MS;
color:blue;
text-align:left;
}
.greet2{
font-size:45px !important;
font-family:Comic Sans MS;
color:purple;
text-align:left;
}
.greet3{
font-size:45px !important;
font-family:Comic Sans MS;
color:orange;
text-align:left;
}
.greet4{
font-size:45px !important;
font-family:Comic Sans MS;
color:black;
text-align:left;
}
.head{
font-size:65px !important;
font-family:times new roman;
position: sticky;
top: 0;
z-index: 999;
color:black;
text-align:center;
font-weight:bold;
}
</style>
""",unsafe_allow_html=True)

def get_weather_report(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()

    # Extract relevant information
    weather_main = weather_data.get('weather', [{}])[0].get('main', '')
    temperature = weather_data.get('main', {}).get('temp', None)

    return weather_main, temperature-273.15

# Determine the time of day
def get_time_of_day():
    current_time = datetime.datetime.now().time()
    hour = current_time.hour

    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 16:
        return "Afternoon"
    elif 16 <= hour < 22:
        return "Evening"
    else:
        return "Night"

api_key = "2144ee2e1866a91955950d7c1e4f7d5b"

default_city='mumbai'
city=st.sidebar.text_input("Enter City Name",value=default_city)
rain,temp=get_weather_report(api_key,city)

time=get_time_of_day()

time1="Good "+time
if time=='Morning':
    st.markdown('<p class="greet1">Good Morning!</p>',unsafe_allow_html=True)
elif time=='Afternoon':
    st.markdown('<p class="greet2">Good Afternoon!</p>',unsafe_allow_html=True)
elif time=='Evening':
    st.markdown('<p class="greet3">Good Evening!</p>',unsafe_allow_html=True)
else:
    st.markdown('<p class="greet4">Good Evening!</p>',unsafe_allow_html=True)


raining_status = 1 if rain.lower() == 'rain' else 0

st.sidebar.write(f"Raining: {'Yes' if raining_status else 'No'}")
st.sidebar.write(f"Temperature: {temp:.2f}°C")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )

chat_enabled = st.sidebar.checkbox("Enable Chat Bot")

melody=0
romantic=0
devotion=0
dance=0
rock=0
brake=0

if chat_enabled:
    chat = 1
else:
    chat = 0

if chat==1:
    def chatbot():
        answers = []  # List to store user answers

        # Chatbot greetings
        st.sidebar.write("Bot: Hi! How are you today?")
        answers.append(st.sidebar.text_input("Question 1:", key="user1"))  # Store user's answer

        st.sidebar.write("Bot: Is everything going well?")
        answers.append(st.sidebar.text_input("Question 2:", key="user2"))  # Store user's answer

        st.sidebar.write("Bot: What did you do today?")
        answers.append(st.sidebar.text_input("Question 3:", key="user3"))  # Store user's answer

        st.sidebar.write("Bot: Tell me about your plans for tomorrow.")
        answers.append(st.sidebar.text_input("Question 4:", key="user4"))  # Store user's answer

        st.sidebar.write("Bot: Does this brings you joy")
        answers.append(st.sidebar.text_input("Question 5:", key="user5"))


        return answers


    # Example usage
if chat==1:
    # st.sidebar.write("Bot: Thank you for sharing! Have a great day!")
    user_answers = chatbot()

    def sentiment():
        global melody,rock,romantic,devotion,dance,brake
        sid = SentimentIntensityAnalyzer()
        positive = 0
        negative = 0
        neutral = 0
        for statement in user_answers:
            scores = sid.polarity_scores(statement)
            sentiment = scores["compound"]

            if sentiment>0.05:
                positive=positive+1
            elif sentiment<-0.05:
                negative=negative+1
            else:
                neutral=neutral+1
        if positive>negative and positive>neutral:
            st.write("Seems you are in Good mood")
            dance=1
            rock=1
        elif neutral>positive and neutral>negative:
            st.write("Seems you are not in good mood I will help with good music")
            melody=1
            romantic=1
        elif negative>positive and negative>neutral:
            st.write("Don't worry, Here is the music to enjoy")
            brake=1

    sentiment()

    devotion_words=['pooja','puja','ritual','festival','temple','divine','spiritual']
    for i in user_answers:
        for j in devotion_words:
            if j in i.lower():
                devotion=1
                break


options = ["MELODY", "DEVOTIONAL", "ROMANTIC", "FOLK", "DANCE", "BREAKUP", "RAIN", "ROCK", "POPULAR PICKS"]

# default_option = "RAIN" if raining_status == 1 else "POPULAR PICKS"
if chat_enabled==0:
    default_option="POPULAR PICKS"
if raining_status == 1:
    default_option = "RAIN"
elif melody==1:
    default_option="MELODY"
elif dance==1:
    default_option="DANCE"
elif devotion==1:
    default_option="DEVOTIONAL"
elif brake==1:
    default_option="BREAKUP"


clicked = st.sidebar.selectbox("Select a Genre", options, index=options.index(default_option))


num_columns = [4,4,4,4]  # Specify the number of columns for each row

# Calculate the total number of rows
num_rows = len(num_columns)

if melody==1 or clicked=='MELODY':
    # st.write(melody)

    # add_bg_from_local(r"D:\INTERNSHIP_CK\m3.jpg")

    st.markdown('<p class="melody">Forget Yourself and swim in the Ocean of Melody</p>',unsafe_allow_html=True)

    melody_spotify_urls = ['spotify:track:7qiZfU4dY1lWllzX7mPBI3',
 'spotify:track:7s2yiftmEe1c5Q1wqIPsqr',
 'spotify:track:72zHuDxFQTjbL51qJQSA7j',
 'spotify:track:3k0DJq2HdWJqnqor8NX0ac',
 'spotify:track:08Zh9GFP2TKItpgcfRSHUV',
 'spotify:track:6FjbAnaPRPwiP3sciEYctO',
 'spotify:track:61fXT6uwJ2THPkbmxa65OI',
 'spotify:track:6bdpj89aYEBjhpsenXAsmO',
 'spotify:track:5FXMRdJjKq1BIX4e8Eg9mK',
 'spotify:track:1UWacd8x8tPPwmrPB1MoBI',
 'spotify:track:4blqlsA1uf2d2I40E90EUC',
 'spotify:track:4KDq9bn0wdEbIFQDi1CGgj',
 'spotify:track:2LcXJP95e4HKydTZ2mYfrx',
 'spotify:track:15tihU7QrnhaBvE7hXGDwa',
'spotify:track:59eeV0SIeyd431uyjAWCRe',
'spotify:track:7I6mwEFQwpTu5ciVZWFpd4']



# Iterate over the number of rows
    for row in range(num_rows):
    # Create the columns for the current row
        columns = st.columns(num_columns[row])

    # Iterate over the columns and display the Spotify player
        for i, column in enumerate(columns):
            index = row * num_columns[row] + i
            if index < len(melody_spotify_urls):
                url = melody_spotify_urls[index]
                track_id = url.split(':')[-1]

                spotify_embed_code = f"""
            <iframe src="https://open.spotify.com/embed/track/{track_id}" width="200" height="300" frameborder="0" allowtransparency="true" allow="encrypted-media" autoplay></iframe>
            """

                column.markdown(spotify_embed_code, unsafe_allow_html=True)



elif devotion==1 or clicked=='DEVOTIONAL':

    # add_bg_from_local(r"D:\INTERNSHIP_CK\devotional.png")

    st.subheader('Let Devotional Vibes Hit You')

    devotional_spotify_urls=['spotify:track:2dyMDwv6YPA15ROQIHh6ov',
 'spotify:track:0pMyxDrMTbAvJv8I0hdgKR',
'spotify:track:2NL9fVWfOs0uXVEaAAxeee',
'spotify:track:1Wqmm0hgWFJtMSxD3uErqx',
 'spotify:track:1XH6oGxbuVkjd5up4FgCYQ',
 'spotify:track:2F3ezB4GmccqvhU0syjeNI',
 'spotify:track:4jeNzToNz1lWTy1SLPQf9K',
 'spotify:track:7sB18S2Ae8Aye4n9s9LZNj',
 'spotify:track:1qWBWMCMNd7wIXaknViBvc',
 'spotify:track:5pkaQ5pS44JGsA8chmUQzk',
 'spotify:track:6MZp3NHVahSX2TpxvREIGv',
 'spotify:track:0LnXmqfordOmvU2zXXVbKf',
 'spotify:track:1BqjKWtv2ipp2eF0MgVLeI',
 'spotify:track:0xeTu8dm7tQPZ7wPSUB36J',
 'spotify:track:6lyXMQRRnHzQa7Y3zqKxAy']

    for row in range(num_rows):
    # Create the columns for the current row
        columns = st.columns(num_columns[row])

    # Iterate over the columns and display the Spotify player
        for i, column in enumerate(columns):
            index = row * num_columns[row] + i
            if index < len(devotional_spotify_urls):
                url = devotional_spotify_urls[index]
                track_id = url.split(':')[-1]

                spotify_embed_code = f"""
            <iframe src="https://open.spotify.com/embed/track/{track_id}" width="200" height="300" frameborder="0" allowtransparency="true" allow="encrypted-media" autoplay></iframe>
            """

                column.markdown(spotify_embed_code, unsafe_allow_html=True)


elif romantic==1 or clicked=='ROMANTIC':
    # st.write(romantic)

    # add_bg_from_local(r"D:\INTERNSHIP_CK\Romantic.jpg")

    st.subheader('Lets Dive into Some Romantic Cloud')

    romantic_song_urls=['spotify:track:2rDPTKSWgUbFuV1jFzPqvE',
 'spotify:track:08Zh9GFP2TKItpgcfRSHUV',
 'spotify:track:5T2ZZiBMDGh3TZDUbxg4rV',
 'spotify:track:2rOnSn2piaqLAlYjtfUBlY',
 'spotify:track:4bD9z9qa4qg9BhryvYWB7c',
 'spotify:track:5O932cZmzOZGOGZz9RHx20',
 'spotify:track:5wdlz4N7s1Xyr4y4RXhZJM',
 'spotify:track:6bdpj89aYEBjhpsenXAsmO',
 'spotify:track:1y1rQTkWmrZdJmjwuK07GC',
 'spotify:track:2rU33n6Fhd6G1MzYhUj6C5',
 'spotify:track:1hQia6rxgfM1ly2hE3StWp',
 'spotify:track:64r6z0P3RnhpTGdkA7p5Os',
 'spotify:track:5GhNEr3AQtMhHGYLRgCSV5',
 'spotify:track:3uL1IBFhg52VcQqOwAG01E',
 'spotify:track:6vhvtHO8e57meVNp8yKzdV']

    for row in range(num_rows):
    # Create the columns for the current row
        columns = st.columns(num_columns[row])

    # Iterate over the columns and display the Spotify player
        for i, column in enumerate(columns):
            index = row * num_columns[row] + i
            if index < len(romantic_song_urls):
                url = romantic_song_urls[index]
                track_id = url.split(':')[-1]

                spotify_embed_code = f"""
            <iframe src="https://open.spotify.com/embed/track/{track_id}" width="200" height="300" frameborder="0" allowtransparency="true" allow="encrypted-media" autoplay></iframe>
            """

                column.markdown(spotify_embed_code, unsafe_allow_html=True)



elif clicked=='POPULAR PICKS':
    st.subheader('Popular Pics.........')
    popular_song_url=['spotify:track:7qiZfU4dY1lWllzX7mPBI3',
 'spotify:track:6n2P81rPk2RTzwnNNgFOdb',
 'spotify:track:1HNkqx9Ahdgi1Ixy2xkKkL',
 'spotify:track:1418IuVKQPTYqt7QNJ9RXN',
 'spotify:track:0wHFktze2PHC5jDt3B17DC',
 'spotify:track:73K33p4Vyz9koXGqmL5eFs',
 'spotify:track:6FAYpZ4jve8vpvTwUvjK6H',
 'spotify:track:6C1RD7YQVvt3YQj0CmuTeu',
 'spotify:track:0puf9yIluy9W0vpMEUoAnN',
 'spotify:track:4blqlsA1uf2d2I40E90EUC',
 'spotify:track:72zHuDxFQTjbL51qJQSA7j',
 'spotify:track:3k0DJq2HdWJqnqor8NX0ac',
 'spotify:track:4UMIv5jd9gK98a39BQRD9X',
 'spotify:track:3hkC9EHFZNQPXrtl8WPHnX',
 'spotify:track:2rOnSn2piaqLAlYjtfUBlY']

    for row in range(num_rows):
    # Create the columns for the current row
        columns = st.columns(num_columns[row])

    # Iterate over the columns and display the Spotify player
        for i, column in enumerate(columns):
            index = row * num_columns[row] + i
            if index < len(popular_song_url):
                url = popular_song_url[index]
                track_id = url.split(':')[-1]

                spotify_embed_code = f"""
            <iframe src="https://open.spotify.com/embed/track/{track_id}" width="200" height="300" frameborder="0" allowtransparency="true" allow="encrypted-media" autoplay></iframe>
            """

                column.markdown(spotify_embed_code, unsafe_allow_html=True)



elif clicked=='FOLK':
    st.subheader('Lets Dance to our Own Folk Songs')
    folk_song_url=[
 'spotify:track:48CzymfD7NHtc78cwVkbtD',
 'spotify:track:3IPxJQjgMLU8MFYY8gzDhC',
 'spotify:track:2edUZOGNahVUdZtToxRHvv',
 'spotify:track:1uJ2czshFLqimctgvsxfv2',
 'spotify:track:4oBhE31sIakxf8bSPHuRT1',
 'spotify:track:74IQCxI4nws964fic1Q4pv',
 'spotify:track:2x2W7PnBelMmLZBV6YqRFQ',
 'spotify:track:1lrgvbZzsjatMee0Uk8o0P',
 'spotify:track:1VIaSk3fxqHAqsl25142Z6',
 'spotify:track:7Do3XWnRkEkyspwibizaBa']

    for row in range(num_rows):
    # Create the columns for the current row
        columns = st.columns(num_columns[row])

    # Iterate over the columns and display the Spotify player
        for i, column in enumerate(columns):
            index = row * num_columns[row] + i
            if index < len(folk_song_url):
                url = folk_song_url[index]
                track_id = url.split(':')[-1]

                spotify_embed_code = f"""
            <iframe src="https://open.spotify.com/embed/track/{track_id}" width="200" height="300" frameborder="0" allowtransparency="true" allow="encrypted-media" autoplay></iframe>
            """

                column.markdown(spotify_embed_code, unsafe_allow_html=True)




elif dance==1 or clicked=='DANCE':
    # st.write(dance)
    st.subheader('Songs that Make You Dance.........')
    dance_song_url=['spotify:track:5fl5pJKjWwJgRkbZfZzyGw',
 'spotify:track:0VcO1SA3oUKl1qHSUc6LxQ',
 'spotify:track:1pApNS3ybh1Qq3O3sq6cZs',
 'spotify:track:7fUMIEn7H6OYDOMQRMm1at',
 'spotify:track:28veUNu4veN0LOBVa0nFw8',
 'spotify:track:1zfS3EZFRA6oTSu49VFaGW',
 'spotify:track:0DpBhHvxAOZUhaRh33dIUK',
 'spotify:track:3InIAYQyi22mfV4g1T9Jkc',
 'spotify:track:6Xi9JEXpj9CmvGqKUJ3P2D',
 'spotify:track:4GSd2iZ83kVU6jwxdvJ0iC',
 'spotify:track:4AoQVhME8Ko6LNm4lV2wwQ',
 'spotify:track:4iKGu3xtvm90eBw0EIPWJP',
 'spotify:track:5VayHAvzwBx4i87c1twFjS',
 'spotify:track:0Le2pspvNVZRNfHW5Edn3E',
 'spotify:track:3szxldqiYs7nkvtmooRod8']

    for row in range(num_rows):
    # Create the columns for the current row
        columns = st.columns(num_columns[row])

    # Iterate over the columns and display the Spotify player
        for i, column in enumerate(columns):
            index = row * num_columns[row] + i
            if index < len(dance_song_url):
                url = dance_song_url[index]
                track_id = url.split(':')[-1]

                spotify_embed_code = f"""
            <iframe src="https://open.spotify.com/embed/track/{track_id}" width="200" height="300" frameborder="0" allowtransparency="true" allow="encrypted-media" autoplay></iframe>
            """

                column.markdown(spotify_embed_code, unsafe_allow_html=True)


elif clicked=='BREAKUP':

    # add_bg_from_local(r"D:\INTERNSHIP_CK\breakup.jpg")

    st.subheader('Every Ending has a new Beginning For now listen this and forget that unluckiest Person in your Life.........')
    breakup_song_url=['spotify:track:1UWacd8x8tPPwmrPB1MoBI',
 'spotify:track:29ffQxBUZLJdN3kiPndB9n',
 'spotify:track:6jUscicoyUljrPOdQCfhnd',
 'spotify:track:0xNiDPK4YdZ51ALxSid0QV',
 'spotify:track:3SqPUWhZXHujSXRShyAybX',
 'spotify:track:5bf5PpAQmxCbXBcRQa5R3C',
 'spotify:track:14M1StehpwsydSGGy8z9eq',
 'spotify:track:63NdWczrPCYGWKY1RV4Zbh',
 'spotify:track:3YB09zhSWO8mmESr8NUV0n',
 'spotify:track:3hXX5v2JaVqDR3aeQcPAU9',
 'spotify:track:1feANd8EfcDP5UqSvbheM3',
 'spotify:track:0DpBhHvxAOZUhaRh33dIUK',
 'spotify:track:0fb1PMDfxtOdU0tMD4JlRg',
 'spotify:track:0anBHV3eP4hiHsLQR5AZsm',
 'spotify:track:07D0H4cb2rlE0BDhvRtnhP']

    for row in range(num_rows):
    # Create the columns for the current row
        columns = st.columns(num_columns[row])

    # Iterate over the columns and display the Spotify player
        for i, column in enumerate(columns):
            index = row * num_columns[row] + i
            if index < len(breakup_song_url):
                url = breakup_song_url[index]
                track_id = url.split(':')[-1]

                spotify_embed_code = f"""
            <iframe src="https://open.spotify.com/embed/track/{track_id}" width="200" height="300" frameborder="0" allowtransparency="true" allow="encrypted-media" autoplay></iframe>
            """

                column.markdown(spotify_embed_code, unsafe_allow_html=True)


elif clicked=='RAIN':
    st.subheader('Brought to You Thundering Songs that makes your rainy day as Memorable day')
    rain_song_url=['spotify:track:0l6g8Z8mqGbGXFOjigYetD',
 'spotify:track:7c1Iv5AxpebPJGD5CXl0yJ',
 'spotify:track:2DDOQBKGmkv7bPoYF1bELz',
 'spotify:track:32DWojMZeZebVrfBkhAkKy',
 'spotify:track:62UqZv8jJwfXpKENrnk8OJ',
 'spotify:track:3NF3c438tAguEcWvU4b5iA',
 'spotify:track:548VhmAhtRb8g4agXrqvCM',
 'spotify:track:1JLtM0dEzGsytDmvfzLAue',
 'spotify:track:1JGqtoauAg8VvcaCziht76',
 'spotify:track:3Me6pWpYVzmSEk9uS1JURe',
 'spotify:track:5NSXAVJqe7Zh66PlRhgRvw',
 'spotify:track:4Bb4Vgzp1kAebqI7KnDFPn',
 'spotify:track:01bhNo46PTQxTYLWAnRzIz',
 'spotify:track:275eks4WjWsfozalBGY2e5',
 'spotify:track:6xC4vXywS1p8zFL8KKgKCQ']

    for row in range(num_rows):
    # Create the columns for the current row
        columns = st.columns(num_columns[row])

    # Iterate over the columns and display the Spotify player
        for i, column in enumerate(columns):
            index = row * num_columns[row] + i
            if index < len(rain_song_url):
                url = rain_song_url[index]
                track_id = url.split(':')[-1]

                spotify_embed_code = f"""
            <iframe src="https://open.spotify.com/embed/track/{track_id}" width="250" height="300" frameborder="0" allowtransparency="true" allow="encrypted-media" autoplay></iframe>
            """

                column.markdown(spotify_embed_code, unsafe_allow_html=True)



elif rock==1 or clicked=='ROCK':
    # st.write(rock)

    # add_bg_from_local(r"D:\INTERNSHIP_CK\Rock.jpg")

    st.subheader('Lets Rock with some Mass Songs')
    rock_song_url=['spotify:track:6FAYpZ4jve8vpvTwUvjK6H',
 'spotify:track:2BcPFQ7nrtUObgAs72xaac',
 'spotify:track:7w4kFO2slzHCu1qEOMaPkl',
 'spotify:track:3oLSlzMt3SD5PYSMf1Aqo0',
 'spotify:track:1LbBOhicFmu7ktJqIHCELt',
 'spotify:track:57bRQzh6XEfIU4uGXz1p5j',
 'spotify:track:1t39FBb0zsKv5krZaqZKCB',
 'spotify:track:6yvxu91deFKt3X1QoV6qMv',
 'spotify:track:4jy2ORlpTbFqI07KO3LgWI',
 'spotify:track:2vkNA9I029dTwX0y6d59Sc',
 'spotify:track:4uXJADmybUHUgycBWFHeq6',
 'spotify:track:6FQQiTpYnfc5803p84bQp1',
 'spotify:track:40NRm1ZLvZpUSCUXAGGZ8J',
 'spotify:track:4eu27jAU2bbnyHUC3G75U8',
 'spotify:track:4sJ9X27MSCue4d0t48MXwe']

    for row in range(num_rows):
    # Create the columns for the current row
        columns = st.columns(num_columns[row])

    # Iterate over the columns and display the Spotify player
        for i, column in enumerate(columns):
            index = row * num_columns[row] + i
            if index < len(rock_song_url):
                url = rock_song_url[index]
                track_id = url.split(':')[-1]

                spotify_embed_code = f"""
            <iframe src="https://open.spotify.com/embed/track/{track_id}" width="200" height="300" frameborder="0" allowtransparency="true" allow="encrypted-media" autoplay></iframe>
            """

                column.markdown(spotify_embed_code, unsafe_allow_html=True)


