import streamlit as st
import pandas as pd
from textblob import TextBlob

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.set_option('deprecation.showPyplotGlobalUse', False)

def sentiment_analysis(comments):
    sentiments = []
    for comment in comments:
        sentiment = TextBlob(comment).sentiment.polarity
        if sentiment > 0:
            sentiment_word = 'Positive'
        elif sentiment == 0:
            sentiment_word = 'Neutral'
        else:
            sentiment_word = 'Negative'
        sentiments.append(sentiment_word)
    return sentiments

def main():
    st.title('Sentiment Analysis')
    st.write("*By:* A. Vera")
    file_or_comments = st.selectbox('Select Input Method', ['Upload File', 'Enter Comments'])
    if file_or_comments == 'Upload File':
        file = st.file_uploader('Upload a CSV file with comments', type='csv')
        if file:
            df = pd.read_csv(file)
            col_options = list(df.columns)
            comments_col = st.selectbox('Select the column that contains the comments', col_options)
            comments = df[comments_col]
            sentiments = sentiment_analysis(comments)
            df['sentiment'] = sentiments
            st.table(df)
            st.write("Sentiment Summary")
            sentiments_count = df['sentiment'].value_counts()
            st.bar_chart(sentiments_count)
            sentiments_count_table = pd.DataFrame({'sentiment': sentiments_count.index,'frequency': sentiments_count.values, 'percentage': (sentiments_count.values/df.shape[0])*100})
            st.table(sentiments_count_table)
            if st.button('Download Results'):
                st.markdown('**Downloading Results**')
                df.to_csv('sentiment_results.csv', index=False)
                st.markdown('**Results Downloaded**')
    else:
        comments = st.text_area('Enter comments, one line per comment')
        comments = comments.split('\n')
        comments = list(filter(None, comments))
        sentiments = sentiment_analysis(comments)
        df = pd.DataFrame({'comments': comments, 'sentiment': sentiments})
        st.table(df)
        st.write("Sentiment Summary")
        sentiments_count = df['sentiment'].value_counts()
        st.bar_chart(sentiments_count)
        sentiments_count_table = pd.DataFrame({'sentiment': sentiments_count.index,'frequency': sentiments_count.values, 'percentage': (sentiments_count.values/df.shape[0])*100})
        st.table(sentiments_count_table)
        if st.button('Download Results'):
            st.markdown('Downloading Results')
            df.to_csv('sentiment_results.csv', index=False)
            st.markdown('Results Downloaded')

if __name__== '__main__':
    main()