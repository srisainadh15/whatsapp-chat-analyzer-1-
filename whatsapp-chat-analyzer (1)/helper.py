from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
def fetch_stats(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    # 2. number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # number of media messages
    num_media_msg = df[df['message'] =='<Media omitted>\n'].shape[0]

    #4 .num of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_msg, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    wc = WordCloud(width =500,height =400,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
