#-*- coding:utf-8 -*-

from SentimentLDA import *
import pickle

def load_processed_data():
    path = '../preprocess/'
    return pd.read_csv(path + 'spacing_nsmc_data.csv')

def main():
    okt = Okt()
    processed_data = load_processed_data()
    numTopics      = input('Input \'numTopics\': ')
    alpha          = input('Input \'alpha\': ')
    beta           = input('Input \'beta\': ')
    gamma          = input('Input \'gamma\': ')
    numSentiments  = input('Input \'numSentiments\': ')
    maxIters       = input('Input \'maxIters\': ')
    while True:
        filename   = input('Input \'filename\': ')
        if '.pkl' not in filename:
            print('파일 확장자 명: \'*.pkl\'. 다시 입력해주세요.')
            continue
        else:
            break
    JST = SentimentLDAGibbsSampler(numTopics, alpha, beta, gamma, numSentiments)
    processed_reviews = JST.processReviews(processed_data.review.tolist(), okt, 
                                           do_preprocess=True, return_processed_review=True)
    JST.run(processed_reviews, okt, maxIters=maxIters, do_preprocess=False)
    with open(filename, 'wb') as f:
        pickle.dump(JST, f, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    main()