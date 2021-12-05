import pandas as pd
import re
import os

#text = 'Bagaimanapun, firma-firma penyelidikan optimis dengan prospek jangka panjang sektor ini terutama didorong dengan pembukaan semula ekonomi meskipun mengambil pendekatan berhati-hati.'

def count(text):
    """
    Simple syllable counting
    """

    # read file
    file = 'malay_syllable.csv'
    cur_path = os.path.dirname(os.path.realpath(__file__))
    spache_path = os.path.join(cur_path, file)
    df=pd.read_csv(spache_path)
    
    word = re.sub("[^\w]", " ",  text).split()
    lis = df['Word'].values.tolist()
    
    count = 0
    count2 = 0

    for w in word:
        w = w.lower()
        if w in lis:
            syl = df.loc[df.Word==w].values[0, 1]
            count += syl

        else:
            w = re.sub('(?:[^laeiouy]es|[^laeiouy]e)$', '', w) # removed ed|
            w = re.sub('^y', '', w)
            matches = re.findall('[aeiouy]{1,2}', w)
            count2 += len(matches)

    return count + count2

#print(count(text))

