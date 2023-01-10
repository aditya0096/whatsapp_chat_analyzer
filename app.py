from ast import Continue
from symbol import continue_stmt
import pandas as pd
import streamlit as st
import preprocessor
import support
import matplotlib.pyplot as plt
import plotly.express as px
import mplcyberpunk
import googletrans
from googletrans import Translator


st.sidebar.title("Import Chat ")
st.title("Social Media Sentiment Analysis")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # fetch users
    user_list = df['user'].unique().tolist()
    if('group_notification' in user_list):
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select users or chat", user_list)

    if st.sidebar.button("Show Analytics"):

        num_messages, words, number_media_msg, links, emoji = support.fetch_stats(
            selected_user, df)
        st.title("Analytics")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media")
            st.title(number_media_msg)

        with col4:
            st.header("Links Shared")
            st.title(links)

        with col5:
            st.header("Emojis Used")
            st.title(emoji)

        st.title("Monthly Timeline")
        timeline = support.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        plt.style.use("cyberpunk")
        # mplcyberpunk.make_lines_glow()
        mplcyberpunk.add_glow_effects(gradient_fill=True)
        st.pyplot(fig)

        # plt.show()

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = support.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.style.use("cyberpunk")
            mplcyberpunk.add_glow_effects()
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = support.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, new_df = support.most_active_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Cloud
        df_wc = support.create_cloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # emojis ranking
        emoji_df = support.emoji_rank(selected_user, df)
        st.title("Emoji Ranking")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            # fig,ax = plt.subplots()
            # ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            # st.pyplot(fig)
            fig = px.pie(emoji_df.head(),
                         values='number_of_Emoji', names='emoji')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)

        # sentiment
        st.title("Sentiment Analysis")
        senti_df = support.sentiment(selected_user, df)
        # st.dataframe(senti_df)
        translator = Translator()
        # deep copy of df
        # translate_df = senti_df.copy()
        # translations = {}
        # for column in translate_df.columns:
        #     # unique elements of the column
        #     unique_elements = translate_df[column].unique()
        #     for element in unique_elements:
        #         # add translation to the dictionary
        #         translations[element] = translator.translate(element).text

        # translate_df.replace(translations, inplace=True)
        # translate_df['translated'] = translate_df['message'].apply(
        #     translator.translate,  dest='en').apply(getattr, args=('text'))
        # st.dataframe(translate_df)

        st.dataframe(senti_df)
        last_3 = senti_df.iloc[:, -3:]
        # st.dataframe(last_3)
        new_data = pd.DataFrame({'Name': ['Positive', 'Negative', 'Neutral'],
                                 'Score': [last_3['Positive'].sum(), last_3['Negative'].sum(),
                                           last_3['Neutral'].sum()]})
        st.dataframe(new_data)
        # fig,ax =new_data.plot.bar(x='Name',y='Scroe',rot=0)
        # st.plotly_chart(fig)
        fig = px.pie(new_data, values='Score', names='Name',
                     title='Pie Chart for sentimental Analysis')
        fig.update_traces(textposition='outside',
                          textinfo='percent+label', textfont_size=14)
        st.plotly_chart(fig)
        # value = senti_df["Positive"].sum()
        # st.text(value)
        #
        # last_3 = senti_df.iloc[:,-3:]
        # # st.dataframe(last_3)
        # new_df = pd.DataFrame({'type': last_3, 'score':last_3.sum()})
        # st.dataframe(new_df)
        # for data in last_3:

        # ax.bar(x.index, x.values)
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)
