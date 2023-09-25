#Install Google play scraper: https://github.com/JoMingyu/google-play-scraper
#!pip install google_play_scraper

import json
import pandas as pd
from tqdm import tqdm

import seaborn as sns
import matplotlib.pyplot as plt

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from google_play_scraper import Sort, reviews, app

#%matplotlib inline
#%config InlineBackend.figure_format='retina'

sns.set(style='whitegrid', palette='muted', font_scale=1.2)

apps_ids = ['br.com.brainweb.ifood', 
            'com.cerveceriamodelo.modelonow',
            'com.mcdo.mcdonalds',
            'habibs.alphacode.com.br',
            'com.xiaojukeji.didi.brazil.customer',
            'com.ubercab.eats',
            'com.grability.rappi',
            'burgerking.com.br.appandroid',
            'br.com.alphacode.madero',
            'com.vanuatu.aiqfome']

app_infos = []

for ap in tqdm(apps_ids):
    info = app(ap, lang='en', country='us')
    del info['comments']
    app_infos.append(info)

app_infos_df = pd.DataFrame(app_infos)
app_infos_df.head(2)

app_reviews = []

for ap in tqdm(apps_ids):
    for score in list(range(1, 6)):
        for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
            rvs, _ = reviews(
                ap,
                lang='pt',
                country='br',
                sort=sort_order,
                count= 400 if score == 3 else 200,
                filter_score_with=score
            )
            for r in rvs:
                r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
                r['appId'] = ap
            app_reviews.extend(rvs)

df = pd.DataFrame(app_reviews)

sns.countplot(x=df["score"])
plt.xlabel('review score')

def to_sentiment(rating):
  rating = int(rating)
  if rating <= 2:
    return 0
  elif rating == 5:
    return 2
  else: 
    return 1

df['sentiment'] = df["score"].apply(to_sentiment)

class_names = ['negative', 'neutral', 'positive']

ax = sns.countplot(x=df["sentiment"])
plt.xlabel('review sentiment')
ax.set_xticklabels(class_names)

df.to_csv('reviews.csv', index=None, header=True)