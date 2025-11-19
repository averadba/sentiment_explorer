import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.set_option('deprecation.showPyplotGlobalUse', False)

def sentiment_analysis(comments):
    sentiments = []
    scores = []
    for comment in comments:
        sentiment = TextBlob(comment).sentiment.polarity
        scores.append(sentiment)
        if sentiment > 0:
            sentiment_word = 'Positive'
        elif sentiment == 0:
            sentiment_word = 'Neutral'
        else:
            sentiment_word = 'Negative'
        sentiments.append(sentiment_word)
    return sentiments, scores

def main():
    st.title('Sentiment Analysis')
    st.markdown("*By:* Dr. Alexis Vera - [Contact me](mailto:alexisvera@gmail.com)")
    # Providing a brief description and explanations
    st.write("### Description:")
    st.write("This app performs sentiment analysis on user-provided comments. It analyzes the sentiment of the text and classifies it as Positive, Neutral, or Negative. Additionally, a sentiment score is provided, which gives a numeric representation of the sentiment ranging from -1 to 1.")
    
    st.write("### Note:")
    st.write("The app is designed to work with English text. Using text in other languages may not yield accurate results.")
    
    st.write("### How It Works:")
    st.write("The sentiment analysis is powered by TextBlob. Here's a brief explanation of the classifications and scores:")
    st.markdown("- **Positive:** The comment has a positive sentiment. A sentiment score closer to 1 indicates stronger positive sentiment.")
    st.markdown("- **Neutral:** The comment neither has a positive nor negative sentiment. The sentiment score is around 0.")
    st.markdown("- **Negative:** The comment has a negative sentiment. A sentiment score closer to -1 indicates stronger negative sentiment.")

    # Disclaimer and reference
    st.write("### Disclaimer:")
    st.write("The sentiment analysis results provided by this app are lexicon-based and should be taken with care. They serve as a general guideline, but the actual sentiment of a text can depend heavily on its context. Always consider the broader context and use these results as one of many tools in your analysis.")
    st.markdown("For more information on TextBlob, visit the [TextBlob documentation](https://textblob.readthedocs.io/en/dev/index.html).")

    st.divider()
    file_or_comments = st.selectbox('Select Input Method', ['Upload File', 'Enter Comments'])
    if file_or_comments == 'Upload File':
        file = st.file_uploader('Upload a CSV file with comments', type='csv')
        if file:
            df = pd.read_csv(file)
            col_options = list(df.columns)
            comments_col = st.selectbox('Select the column that contains the comments', col_options)
            try:
                comments = df[comments_col].astype(str)
                sentiments, scores = sentiment_analysis(comments)
                df['sentiment'] = sentiments
                df['sentiment_score'] = scores
            except TypeError:
                st.warning("Please, select a column that contains text.")
                return

            st.write("Results: Based on selected column.")
            st.dataframe(df)

            # Plotting sentiment scores distribution
            st.write("Sentiment Score Distribution:")
            plt.hist(scores, bins=30, edgecolor='k')
            plt.xlabel('Sentiment Score')
            plt.ylabel('Frequency')
            plt.title('Distribution of Sentiment Scores')
            st.pyplot()

            st.write("Sentiment Summary")
            sentiments_count = df['sentiment'].value_counts()
            st.bar_chart(sentiments_count)
            sentiments_count_table = pd.DataFrame({'sentiment': sentiments_count.index,'frequency': sentiments_count.values, 'percentage': (sentiments_count.values/df.shape[0])*100})
            st.table(sentiments_count_table)
            if st.button('Download Results'):
                st.markdown('**Downloading Results**')
                df.to_csv('sentiment_results.csv', index=False)
                st.markdown('**Results Downloaded.** Please check in your current working directory or your default directory for downloads.')
    else:
        comments = st.text_area('Enter comments, one line per comment')
        comments = comments.split('\n')
        comments = list(filter(None, comments))
        sentiments, scores = sentiment_analysis(comments)
        df = pd.DataFrame({'comments': comments, 'sentiment': sentiments, 'sentiment_score': scores})
        st.table(df)

        # Plotting sentiment scores distribution
        st.write("Sentiment Score Distribution")
        plt.hist(scores, bins=30, edgecolor='k')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        plt.title('Distribution of Sentiment Scores')
        st.pyplot()

        st.write("Sentiment Summary")
        sentiments_count = df['sentiment'].value_counts()
        st.bar_chart(sentiments_count)
        sentiments_count_table = pd.DataFrame({'sentiment': sentiments_count.index,'frequency': sentiments_count.values, 'percentage': (sentiments_count.values/df.shape[0])*100})
        st.table(sentiments_count_table)
        if st.button('Download Results'):
            st.markdown('Downloading Results')
            df.to_csv('sentiment_results.csv', index=False)
            st.markdown('**Results Downloaded.** Please check in your current working directory or your default directory for downloads.')

if __name__== '__main__':
    main()
