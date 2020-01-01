import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from chatspace import ChatSpace
import re
from konlpy.tag import Okt

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

def load_embedding(embeddingname):
    with open(embeddingname, 'rb') as f:
        embedding = pickle.load(f)
    return embedding

def load_model(modelname):
    with open(modelname, 'rb') as f:
        model = pickle.load(f)
    return model

def check_input_pkl(text):
    while True:
        name = input('Input \'{}\': '.format(text))
        if '.pkl' not in name:
            print('파일 확장자 명: \'*.pkl\'. 다시 입력해주세요.')
            continue
        else:
            break
    return name

def plot_res(text, embedding, model, spacer=None, o=True, cmap='Spectral'):
    if o:
        t = embedding.transform([spacer.space(re.sub('[ㄱ-ㅎㅏ-ㅣ가힣]', ' ', text))])
    else:
        t = embedding.transform([text])
    d = model.predict_proba(t)
    print('\nProbability Distribution:\n', d[0])
    print('\n{}'.format(i2senti[d[0].argmax()].upper()))
    data_color = d[0][np.argsort(d[0])]
    my_cmap = plt.cm.get_cmap(cmap)
    colors = my_cmap(data_color)

    plt.barh(np.arange(8), d[0][np.argsort(d[0])], color=colors, edgecolor='k')
    plt.yticks(np.arange(8),
               np.array(['Joy', 'Interest',
                         'Anger', 'Admiration',
                         'Sadness', 'Surprise',
                         'Fear', 'Disgust'])[np.argsort(d[0])])
    plt.show()

def isyes(text):
    if text.lower() in ['y', 'yes']:
        return True
    else:
        return False

def isno(text):
    if text.lower() in ['n', 'no']:
        return True
    else:
        return False

def main():
    spacer = ChatSpace()
    # embeddingname = check_input_pkl('embeddingname')
    # modelname = check_input_pkl('modelname')
    embeddingname = 'tfidf_20191112.pkl'
    modelname = 'gnb_clf_tfidf_20191112.pkl'

    embedding = load_embedding('../model/' + embeddingname)
    model = load_model('../model/' + modelname)

    while True:
        text = input('감정을 알고싶은 Text를 입력해주세요. ')
        plot_res(text, embedding, model, spacer)
        while True:
            answer = input('더 분석하시겠습니까? (Yes/No): ')
            if not (isyes(answer) | isno(answer)):
                print('Yes와 No로 답변해주세요.')
                continue
            else:
                break
        if isno(answer):
            break
    print('종료.')

if __name__ == '__main__':
    main()
