from django import urls
from django.contrib.auth.models import User
from django.forms import fields
from django.contrib.auth.views import LoginView

from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render
from django.http import *
from myapp.forms import *
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from django.urls import reverse_lazy

from django.contrib.auth.forms import UserCreationForm





class CustomLogin(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('show')
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request , 'register.html', {'form' : form })
    



class TwitterSentClass():
    def __init__(self):
        API_key = 'cpmy0HDV7Upq0F0a4frxQni88'
        API_secret = 'Oj1meU0CsfaBErCryvksBkF5Ge3Ob0ZRA91tYGrbATzFNQimYm'
        access_token = '910182886942302208-GNGGzpmZbyKaSeQKmNPVZ3SoHVn7ZJp'
        access_token_secret = '7VkmKxvstRgOaWJ9Jn6wFFalnx9PYYWT8mHdIceLCyh2n'
        try:
            self.auth = OAuthHandler(API_key, 
                                     API_secret)
            self.auth.set_access_token(access_token,
                                       access_token_secret)
            self.api = tweepy.API(self.auth)
            print('Authenticated')
        except:
            print("Sorry! Error in authentication!")
 
    def cleaning_process(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"
                               , " ", tweet).split())
 
    def get_sentiment(self, tweet):
        analysis = TextBlob(self.cleaning_process(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count=1000):
        tweets = []
        try:
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] =self.get_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
 
        except tweepy.TweepError as e:
            print("Error : " + str(e))


@login_required(login_url='login')
def show(request):
    form = TwitterForm()
    return render(request,'index.html',{'ff':form})
    
            
def prediction(request):
    arr_pred = []
    arr_pos_txt = []
    arr_neg_txt = []
    if request.method == 'POST' :
        api = TwitterSentClass()
        t = request.POST['tweeterid']
        tweets = api.get_tweets(query = t, count = 100)

        pos_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        pos = "Positive tweets percentage: {} %".format(100*len(pos_tweets)/len(tweets))

        neg_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        neg="Negative tweets percentage: {}%".format(100*len(neg_tweets)/len(tweets))                
        # adding the percentages to the prediction array to be shown in the html page.
        arr_pred.append(pos)
        arr_pred.append(neg)
        
        # storing first 5 positive tweets
        arr_pos_txt.append("Positive tweets:")
        for tweet in pos_tweets[:5]:
            arr_pos_txt.append(tweet['text'])

        # storing first 5 negative tweets
        arr_neg_txt.append("Negative tweets:")
        for tweet in neg_tweets[:5]:
            arr_neg_txt.append(tweet['text'])
        
        return render(request,'prediction.html',{'arr_pred':arr_pred,'arr_pos_txt':arr_pos_txt,'arr_neg_txt':arr_neg_txt})
        