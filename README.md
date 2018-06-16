# Facebook Sentiments Analysis Using Natural Language Processing#

Disclaimer: Most of the sentiment analysis code is based on [Jiayu Yi](https://medium.com/google-cloud/sentiment-analysis-of-comments-on-lhls-facebook-page-9db8b3a60eb3). I work on integrating it with telegram.

## A telegram bot for user's to paste facebook's post URLs and the bot will return the statistics of the sentiment analysis.

- This bot require users to input their facebook access token to allow searching of posts. Note that some post may not be assessible by users and will throw an error while using the bot.
- Based on the URL, the bot will attempt to decipher both user-id/organisation-id of the original poster, and the post id provided by facebook. This was done pretty hackishly and hence is extremely unstable.
- To save on processing power, each comment will only be analyzed based on the top 50 posts. 
- Each comment will be sorted into four basic categories based on Google Cloud Natural Language API
  - Positive
  - Negative
  - Neutral
  - Failed.

## Images

![Screen Shot 2018-06-16 at 11.42.35 PM](/Users/weineng/Desktop/Screen Shot 2018-06-16 at 11.42.35 PM.png)

## Issues 

All pull request to improve this code will be greatly appreciated.

- Corner cases of facebook link
  - "fb.com/..."
  - "https://mtouch.facebook.com/"
- Difficultly in accurately determining facebook post id as param's might be included in the link.
  - https://mtouch.facebook.com/story.php?story_fbid=10212364495898709&id=1569406240



## Contact

I can be contacted by email: weineng.a@gmail.com

