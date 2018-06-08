ES_HOST = {
    "host": "localhost",
    "port": 9200
}

#from elasticsearch import Elasticsearch
from worldcupleadertweets import *
from translatationToJSON import translateTweetsJson
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import json

# create ES client, create index
#es = Elasticsearch (hosts=[ES_HOST])

# def lookup_leader(screen_name):
#     print("searching...")
#     doc = translateTweetsJson(screen_name, quant=25)
#     # print (doc[1]["content"])
#     res = es.search (body={
#         'query': {
#             'match': {
#                 'content': doc[1]["content"] ,
#             }
#         }
#     })
#     print ("Max score: ", res["hits"]["max_score"])
#     i = 0
#     while (res["hits"]["hits"][i]):
#         print (res["hits"]["hits"][i]["_score"])
#         i = i + 1
#     return res


def get_terms_weights(content):
    leaders_content = []
    tfidf_vectorizer = TfidfVectorizer (max_df=0.85, min_df=2, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform (leaders_content)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names ()


def compute_idf():
    tfidf_vect = TfidfVectorizer()
    for name in screen_names:
        with open ("JSONs/" + name.lower (), "r") as f:
            for line in f:
                data = json.loads(line)
                # print(data[1]["content"])
                # content.append(data[1]["content"])
            tfidf = tfidf_vect.fit([data[1]['content']])
            pickle.dump(tfidf, open('pickle/' + name.lower(), "wb"))


# def compute_idf():
    #initialize an empty vectorizer
    # tfidf_vect = TfidfVectorizer (max_df=0.85, min_df=2, stop_words='english')

    # list_of_strings = make_tweet_json()
    #compute idf values for each world leader (list_of_strings has length 32)

    # print (tfidf.get_feature_names())
  #save the fitted vectorizer to use later
    # pickle.dump(tfidf, open("some_file_name", "wb"))

# tfidf_vect = pickle.load("some_file_name")

def score_user(screen_name):
    user_tweets = translateTweetsJson(screen_name, False, False, False, 25)[1]["content"]
    words = user_tweets.split(" ")
    #words = words[:500]
    print("NUM WORDS = " + str(len(words)))
    print(user_tweets)
    word_scores = []
    scores = {}
    minimum = float("inf")
    maximum = float("inf")
    sum = float(0)
    for name in screen_names:
        tfidf_vect = pickle.load (open("pickle/"+name.lower(), "rb"))
        total_score = 0
        setHere = set(words)
        # for unique_word in set(user_tweets.split(" ")):
        for unique_word in setHere:

            #is the word in idf dictionary?
            # print (tfidf_vect.get_feature_names())
            #print (unique_word)
            if unique_word in tfidf_vect.get_feature_names():
              #word importance weight

              idf_index = tfidf_vect.get_feature_names().index(unique_word)
              idf_score = tfidf_vect.idf_[idf_index]
              word_score = user_tweets.count(unique_word) * idf_score
              total_score += word_score
              word_scores.append((word_score,unique_word))
        myScore = total_score/len(words)
        minimum = min(minimum, myScore)
        maximum = max(maximum, myScore)
        sum += float(myScore)
        scores[name] = myScore
        print(name+" DIVIDED = " + str(total_score/len(words)))

    
    avg = float(sum) / float(len(screen_names))

    # print("MAX: " + str(maximum))
    # print("MIN: " + str(minimum))
    # print("AVG: " + str(avg))
    
    range = maximum - minimum
    avg_high = avg + range
    avg_low = avg - range

    return word_scores


#compute_idf()
print(score_user("jc_varela"))
# print(score_user("realdonaldtrump"))
# print(score_user("gudlaugurthor"))

# translateTweetsJson("realdonalTrump", False, False, False, 25)[1]["content"]




