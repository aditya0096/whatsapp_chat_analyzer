import streamlit as st
import preprocessor
import support
import matplotlib.pyplot as plt
import plotly.express as px

st.sidebar.title("Import Chat ")
st.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # fetch users
    user_list = df['user'].unique().tolist()
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
            st.header("Total Media send")
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
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = support.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = support.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
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
            fig = px.pie(emoji_df.head(), values='number_of_Emoji', names='emoji',
                         title='Emoji percentage used in chat group')
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)
