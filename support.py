import re
from typing import Counter
import emoji
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
from nltk.sentiment.vader import SentimentIntensityAnalyzer
extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    emojis = []
    # for message in df['message']:
    #     emoji.extend(emojis.get(message))

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    number_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), number_media_msg, len(links), len(emojis)


def most_active_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percentage'})
    return x, df


def create_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def emoji_rank(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # emojis_ranking = []
    # for message in df['message']:
    #     emojis_ranking.extend(
    #         [c for c in message if c in emoji.UNICODE_EMOJI['en']])
    # emoji_df = pd.DataFrame(
    #     Counter(emojis_ranking).most_common(len(Counter(emojis_ranking))))

    df2 = df.copy()

    # Count the number of emoji
    emoji_ctr = Counter()
    emojis_list = map(lambda x: ''.join(x.split()),
                      emoji.UNICODE_EMOJI['en'].keys())  # UNICODE_EMOJI class have a thee emoji code inside
    r = re.compile('|'.join(re.escape(p) for p in emojis_list))
    for idx, row in df2.iterrows():
        emojis_found = r.findall(row["message"])  # The findall() is a functions for regex that help to find a matches
        for emoji_found in emojis_found:
            emoji_ctr[emoji_found] += 1

    emojis_df = pd.DataFrame()  # The reason to use pd.dataframe is we want to put the emojis_df into the dataframe tables
    emojis_df['emoji'] = [''] * 10
    emojis_df['number_of_Emoji'] = [0] * 10

    i = 0
    for item in emoji_ctr.most_common(10):
        emojis_df.emoji[i] = item[0]
        emojis_df.number_of_Emoji[i] = int(item[1])
        i += 1

    return emojis_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def sentiment(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    data = df.dropna()
    sentiments = SentimentIntensityAnalyzer()
    data["Positive"] = [sentiments.polarity_scores(i)["pos"]for i in data['message']]
    data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data['message']]
    data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data['message']]
    # new_data = pd.DataFrame({'Name':['Positive','Negative','Neutral'],
    #                          'Scroe':[{data['Positive'].sum()},{data['Negative'].sum()},{data['Neutral'].sum()}]})

    return data