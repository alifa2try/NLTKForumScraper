from sklearn.feature_extraction.text import CountVectorizer


def vectorizeMessage(forumMessages):
    
    # Initialise the skit counting vector. It counts word frequencies
    vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
    
    forumMessagesFeatures = vectorizer.fit_transform(forumMessages)
    
    # Convert to a numpy array
    forumMessagesFeatures = forumMessagesFeatures.toarray()    
    
    print(vectorizer.get_feature_names())
    
    return forumMessagesFeatures

