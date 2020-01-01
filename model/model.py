import pickle
from collections import defaultdict
from collections import Counter
from konlpy.tag import Okt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

okt = Okt()
def tokenizer_morphs(doc):
    return okt.morphs(doc)

# 전역 사전 설정
i2senti = {0 : 'joy', 
           1 : 'interest', 
           2 : 'anger', 
           3 : 'admiration',
           4 : 'sadness', 
           5 : 'surprise', 
           6 : 'fear', 
           7 : 'disgust'}

def load_processed_data():
    path = '../preprocess/'
    return pd.read_csv(path + 'spacing_nsmc_data.csv')

def load_JSTLabel(filename):
    with open('../labeling/' + filename, 'rb') as f:
        JST = pickle.load(f)
    return JST

def check_input_pkl(text):
    while True:
        name = input('Input \'{}\': '.format(text))
        if '.pkl' not in name:
            print('파일 확장자 명: \'*.pkl\'. 다시 입력해주세요.')
            continue
        else:
            break
    return name
            
def main():
    JSTname       = check_input_pkl('JSTname')
    Embeddingname = check_input_pkl('Embeddingname')
    modelname     = check_input_pkl('modelname')
    
    JST = load_JSTLabel(JSTname)
    
    res = defaultdict(list)
    for i, j in JST.sentiments.items():
        res[i[0]].append(j)
    res = {i : Counter(j) for i, j in res.items()}
    
    processed_data = load_processed_data()
    senti_label_each_review = [[] for _ in range(len(processed_data))]
    for i in range(len(processed_data)):
        if res.get(i):
            for j in res.get(i).most_common(2):
                senti_label_each_review[i].append(i2senti[j[0]])
        else:
            senti_label_each_review[i].append(['neutral'])
    X_train = processed_data['review'].copy()
    y_train = senti_label_each_review
    
    X_train2 = np.array(X_train.values)
    y_train2 = np.array([i[0] for i in y_train])

    y_label = np.zeros((len(y_train), len(i2senti.values())))
    senti2i = {j : i for i, j in i2senti.items()}
    for ix, contents in enumerate(y_train):
        for j in contents:
            if j == ['neutral']:
                continue
            if y_label[ix, senti2i[j]] == 0:
                y_label[ix, senti2i[j]] += 1
    ind = np.where(y_label.sum(axis=1) != 0)
    
    X_train2 = X_train2[ind]
    y_label = y_label[ind]
    y_train2 = y_train2[ind]
    
    tfidf = TfidfVectorizer(tokenizer=tokenizer_morphs, max_features=50000)
    %time tfidf_x_train2 = tfidf.fit_transform(X_train2[:500000])
    
    multi_nbc = MultinomialNB()
    y_train2 = list(map(lambda x : senti2i[x], y_train2[:500000]))
    multi_nbc.fit(tfidf_x_train2, y_train2)
    
    with open(Embeddingname, 'wb') as f:
        pickle.dump(tfidf, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open(modelname, 'wb') as f:
        pickle.dump(multi_nbc, f, protocol=pickle.HIGHEST_PROTOCOL)
        
if __name__ == '__main__':
    main()