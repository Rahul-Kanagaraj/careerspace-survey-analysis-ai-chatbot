### Scripts in Power BI
## 3. What suggestions do they have for services we don’t currently offer?
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: Clean input
dataset = dataset.dropna(subset=['Response'])
dataset = dataset[dataset['Question_id'] == 'Q28']
dataset['Response'] = dataset['Response'].astype(str)

# Step 2: TF-IDF vectorization for unigrams, bigrams, trigrams
vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english', max_features=1000)
X = vectorizer.fit_transform(dataset['Response'])

# Step 3: TF-IDF value DataFrame
token_array = X.toarray()
token_labels = vectorizer.get_feature_names_out()
token_scores = token_array.sum(axis=0)

df = pd.DataFrame({
    'Token': token_labels,
    'TFIDF_Score': token_scores
})

# Step 4: Detect token type
df['Token_Type'] = df['Token'].apply(lambda x: 'Unigram' if len(x.split()) == 1 
                                     else 'Bigram' if len(x.split()) == 2 
                                     else 'Trigram')

# Step 5: Sort and return
result = df[['Token', 'Token_Type', 'TFIDF_Score']].sort_values(by='TFIDF_Score', ascending=False)


## Question 4 : What are key issues faced by students and how can we better support them?

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: Clean input
dataset = dataset.dropna(subset=['Response'])
comment_ids = ['Q15', 'Q15_8_TEXT', 'Q16', 'Q80', 'Q80_4_TEXT','Q89','Q89_6_TEXT','Q31','Q65', 'Q68', 'Q44', 
'Q46', 'Q48']
dataset = dataset[dataset['Question_id'].isin(comment_ids)].dropna(subset=['Response'])
dataset['Response'] = dataset['Response'].astype(str)

# Step 2: TF-IDF Vectorization for unigrams, bigrams, trigrams
vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english', max_features=1000)
X = vectorizer.fit_transform(dataset['Response'])

# Step 3: TF-IDF score DataFrame
token_array = X.toarray()
token_labels = vectorizer.get_feature_names_out()
token_scores = token_array.sum(axis=0)  # sum TF-IDF scores across all documents

df = pd.DataFrame({
    'Token': token_labels,
    'TFIDF_Score': token_scores
})

# Step 4: Detect token type
df['Token_Type'] = df['Token'].apply(lambda x: 'Unigram' if len(x.split()) == 1 
                                     else 'Bigram' if len(x.split()) == 2 
                                     else 'Trigram')

# Step 5: Sort and return
result = df[['Token', 'Token_Type', 'TFIDF_Score']].sort_values(by='TFIDF_Score', ascending=False)


# 9. What are they most interested in learning about?

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: Clean input
dataset = dataset.dropna(subset=['Response'])
comment_ids = ['Q30']
dataset = dataset[dataset['Question_id'].isin(comment_ids)].dropna(subset=['Response'])
dataset['Response'] = dataset['Response'].astype(str)

# Step 2: TF-IDF Vectorization (unigrams, bigrams, trigrams)
vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english', max_features=1000)
X = vectorizer.fit_transform(dataset['Response'])

# Step 3: Create DataFrame with TF-IDF scores
token_array = X.toarray()
token_labels = vectorizer.get_feature_names_out()
token_scores = token_array.sum(axis=0)  # sum of TF-IDF across all docs

df = pd.DataFrame({
    'Token': token_labels,
    'TFIDF_Score': token_scores
})

# Step 4: Detect token type
df['Token_Type'] = df['Token'].apply(lambda x: 'Unigram' if len(x.split()) == 1 
                                     else 'Bigram' if len(x.split()) == 2 
                                     else 'Trigram')

# Step 5: Sort and return
result = df[['Token', 'Token_Type', 'TFIDF_Score']].sort_values(by='TFIDF_Score', ascending=False)

## What features do they want our Job Board to have?

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: Clean input
dataset = dataset.dropna(subset=['Response'])
comment_ids = ['Q28','Q72']
dataset = dataset[dataset['Question_id'].isin(comment_ids)].dropna(subset=['Response'])
dataset['Response'] = dataset['Response'].astype(str)

# Step 2: TF-IDF Vectorization for unigrams, bigrams, trigrams
vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english', max_features=1000)
X = vectorizer.fit_transform(dataset['Response'])

# Step 3: TF-IDF score DataFrame
token_array = X.toarray()
token_labels = vectorizer.get_feature_names_out()
token_scores = token_array.sum(axis=0)  # sum TF-IDF scores across all documents

df = pd.DataFrame({
    'Token': token_labels,
    'TFIDF_Score': token_scores
})

# Step 4: Detect token type
df['Token_Type'] = df['Token'].apply(lambda x: 'Unigram' if len(x.split()) == 1 
                                     else 'Bigram' if len(x.split()) == 2 
                                     else 'Trigram')

# Step 5: Sort and return
result = df[['Token', 'Token_Type', 'TFIDF_Score']].sort_values(by='TFIDF_Score', ascending=False)
 