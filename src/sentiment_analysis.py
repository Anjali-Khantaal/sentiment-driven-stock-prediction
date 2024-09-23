import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from config import NEWS_DATA_FILE, MAX_SEQ_LENGTH

def load_news_data():
    news_df = pd.read_csv(NEWS_DATA_FILE, parse_dates=['publishedAt'], date_parser=lambda x: pd.to_datetime(x, utc=True))
    return news_df

def analyze_sentiment_batch(text_list):
    tokenizer = AutoTokenizer.from_pretrained('yiyanghkust/finbert-tone')
    model = AutoModelForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')

    # Ensure model is in evaluation mode
    model.eval()

    sentiments = []
    sentiment_scores = []

    # Label mapping
    id2label = {0: 'positive', 1: 'neutral', 2: 'negative'}

    # Process in batches to handle large datasets
    batch_size = 16
    for i in range(0, len(text_list), batch_size):
        batch_texts = text_list[i:i+batch_size]
        inputs = tokenizer(
            batch_texts,
            add_special_tokens=True,
            max_length=MAX_SEQ_LENGTH,
            truncation=True,
            padding=True,
            return_tensors='pt'
        )
        with torch.no_grad():
            outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiments_batch = torch.argmax(probs, dim=1).numpy()
        sentiment_labels = [id2label[s] for s in sentiments_batch]
        sentiment_scores_batch = probs.numpy().tolist()

        sentiments.extend(sentiment_labels)
        sentiment_scores.extend(sentiment_scores_batch)

    return sentiments, sentiment_scores

def main():
    news_df = load_news_data()

    print("Performing sentiment analysis...")
    sentiments, sentiment_scores = analyze_sentiment_batch(news_df['title'].tolist())
    news_df['sentiment'] = sentiments
    news_df['sentiment_score'] = [score[id2label_rev[label]] for score, label in zip(sentiment_scores, sentiments)]

    # Save the updated dataframe
    news_df.to_csv(NEWS_DATA_FILE, index=False)
    print(f"Sentiment analysis completed and saved to {NEWS_DATA_FILE}")

# Reverse mapping for sentiment scores
id2label_rev = {'positive': 0, 'neutral': 1, 'negative': 2}

if __name__ == "__main__":
    main()
