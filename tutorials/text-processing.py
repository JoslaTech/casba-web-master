# Simple Bag of Word model for Sentiment Analysis on a Single tweet
tweet='Ok'
print tweet

print len(tweet)

## Create dictionary for linguistic query
positive_words=['awesome','good','nice','super','fun']
positive_words.append('delightful')
print positive_words

negative_words=['awful','lame','horrible','bad']
print negative_words

emotional_words=negative_words+positive_words
print emotional_words

## Split tweet string into list (Bag of words)
words = tweet.split()
print words

## Decriptive stat
len(words)

for word in words:
    print words

for word in words:
    if word in positive_words:
        print word+'  is a positive word'

for word in words:
    if word in negative_words:
        print word+'  is a negative word'

for word in words:
    if word in positive_words:
        print word+'  is a positive word'
    elif word in negative_words:
        print word+'  is a negative word'
    else:
        print word+'  is a neutral word'


# Preprocessing
## convert o lower case
tweet_lowercase = tweet.lower()
print tweet_lowercase

for word in words:
    if word.lower() in positive_words:
        print word.lower()+'  is a positive word'

## remove punctuations
tweet_nopunc=tweet.replace('!','').replace('.','')
print tweet_nopunc

## create bag of words after preprocess tweets to lower case and punctuation into one preprocessing function
words = tweet.replace('!','').replace('.','').lower().split()
print words

## improting punctuations
from string import punctuation
print punctuation

## improving on removing punctuation
