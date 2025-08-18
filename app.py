import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("WhatsApp Chat Analyzer")


uploaded_file = st.sidebar.file_uploader("Choose a file")
# uploaded_file =

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)


    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
         num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user, df)
         st.title("Top Statistics")
         col1, col2, col3, col4 = st.columns(4)

         with col1:
            st.header("Total Messages")
            st.title(num_messages)
         with col2:
            st.header("Total words")
            st.title(words)
         with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
         with col4:
            st.header("Links Shared")
            st.title(num_links)
    #
        #finding the busiest users in the group(Group Level)
    if selected_user == 'Overall':
        st.title('Most Busy Users')
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)
    #
        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

        #Wordcloud
        st.title("Wordcloud1")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Wordcloud2")
        df_wc2 = helper.create_wordcloud1(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc2)
        st.pyplot(fig)
    #
        # most common words
        most_common_df = helper.most_common_words(selected_user, df)
        st.dataframe(most_common_df)
        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
    #
        st.title('Most commmon words')
        st.pyplot(fig)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


  # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            busy_day.index = busy_day.index.astype(str)
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            busy_day.index = busy_day.index.astype(str)
            ax.bar(busy_month.index, busy_month.values, color='Orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


# SENTIMENTS ANALYSIS
if st.sidebar.button("Show sentiments",key = "analysis_2"):
    # Sentiment Analysis Section
    st.title("Sentiment Analysis")
    sentiment_counts, sentiment_df = helper.analyze_sentiment(df, selected_user)

    col1, col2 = st.columns(2)

    with col1:
        st.header("Sentiment Distribution")
        fig, ax = plt.subplots()
        ax.bar(sentiment_counts.index, sentiment_counts.values, color=['green', 'red', 'blue'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.header("Messages with Sentiment")
        st.dataframe(sentiment_df)


