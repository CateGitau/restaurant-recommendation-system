def score(data):
    # Computing Super-Score Rating for Reviews
    data['super_score'] = data['polarity'] *  data['compound']
    data['super_score'] = data['super_score'] + data['stars']

    return data