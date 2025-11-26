from operator import itemgetter

import requests

from plotly.graph_objs import Bar
from plotly import offline

# Make an API call and store the response.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process information about each submission.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
    # Make a seqparate API call for each submission.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f'id: {submission_id}\tstatus: {r.status_code}')
    response_dict = r.json()

    # Build a  dictionary for each article.
    submission_dict = {
        'title': response_dict['title'],
        'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
        'comments': response_dict['descendants'],     
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                            reverse=True)

submission_links, comments, labels = [],[],[]
for submission_dict in submission_dicts:
    labels.append(f"\nTitle: {submission_dict['title']}")
    submission_link = f"<a href='http://news.ycombinator.com/item?id='>{repo_name}</a>"
    submission_links.append(submission_dict['hn_link'])
    comments.append(submission_dict['comments'])

# Make visualization.
data = [{
    'type': 'bar',
    'x': submission_links,
    'y': comments,
    'hovertext': labels,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity':0.6,
}]
my_layout = {
    'title': {
        'text': 'Most Commented Post on Hacker News',
        'font': {'size': 28},
    },
    'xaxis': {
        'title': {
            'text':'Posts',
            'font': {'size': 24},
        },
        'tickfont': {'size': 14},
    },
    'yaxis': {
        'title': {
            'text': 'Comments',
            'font': {'size': 14},
        },
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='hacker_news_comments.html')