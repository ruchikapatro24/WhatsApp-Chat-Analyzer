from urlextract import URLExtract
from wordcloud import WordCloud

import pandas as pd
from collections import Counter

from textblob import TextBlob

extract = URLExtract()    #urlextrac's object

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df=df[df['user'] == selected_user]

        #fetch the number of messages
    num_messages = df.shape[0]
        # return df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
            # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words),num_media_messages,len(links)

#

#
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df =round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df



#wordcloud
def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

#
#

#

def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df



# def create_wordcloud1(selected_user, df):
#     f = open('stop_hinglish.txt', 'r')
#     stop_words = f.read().splitlines()
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     temp = df[df['user'] != 'group_notification']
#     # temp = temp[temp['message'] != '<Media omitted>\n']
#     temp = temp[~temp['message'].str.contains("Media omitted", case=False, na=False)]
#     def remove_stop_words(message):
#         y = []
#         for word in message.lower().split():
#             if word not in stop_words:
#                 y.append(word)
#         return " ".join(y)
#
#     wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
#     temp['message'] = temp['message'].apply(remove_stop_words)
#     df_wc2 = wc.generate(df['message'].str.cat(sep=" "))
#     return df_wc2


def create_wordcloud1(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']

    # Remove messages that contain "Media omitted" (accounting for possible extra spaces/newlines)
    temp = temp[~temp['message'].str.contains("Media omitted", case=False, na=False)]

    def remove_stop_words(message):
        # Split the message into words, remove stop words, and return the cleaned message
        words = message.lower().split()
        cleaned_message = " ".join([word for word in words if word not in stop_words])
        return cleaned_message

    # Apply the stop word removal function to each message
    temp['message'] = temp['message'].apply(remove_stop_words)

    # Create the word cloud after stop word removal
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc2 = wc.generate(
        temp['message'].str.cat(sep=" "))  # Combine all messages into a single string for the word cloud
    return df_wc2


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
#
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
#
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline
#
def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

#HeatMap
def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap= df.pivot_table(index='day_name',columns='period' , values='message',aggfunc='count').fillna(0)
    return user_heatmap

# SENTIMENTS ANALYSIS
# from textblob import TextBlob

def analyze_sentiment(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Analyze sentiment for each message
    sentiments = df['message'].apply(lambda msg: TextBlob(msg).sentiment.polarity)
    df['Sentiment'] = sentiments.apply(
        lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')
    )

    # Count sentiment categories
    sentiment_counts = df['Sentiment'].value_counts()

    return sentiment_counts, df[['message', 'Sentiment']]


