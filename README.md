# Text2SentiNet

## Version 0.0
![title](https://github.com/jinmang2/t2snet/blob/master/img/t2snet.PNG?raw=true)
- Author
  - [MyungHoon Jin](https://github.com/jinmang2) / [Hohyun-Kim](https://github.com/Hohyun-Kim)
- [Presentation](https://github.com/jinmang2/t2snet/blob/master/etc/%EC%84%9C%EC%9A%B8%EB%B0%98_%EA%B5%AD%EB%82%B4%EC%B5%9C%EC%B4%88%EB%8B%A4%EC%A4%91%EA%B0%90%EC%A0%95%EB%B6%84%EB%A5%98%EA%B8%B0_%ED%8E%98%EB%A5%B4%EC%86%8C%EB%82%98%EC%8B%9C%EC%8A%A4%ED%85%9C.pdf)
- Preprocessing
  - `py-hanshell`
  - `chatspace`
  - stopwords, 한국어 이외 문자 제거
- Labeling
  - `SentimentLDA`
  - `KSenticNet`
  - CBOW
- Modeling
  - `Gaussian Naive Bayse`

## To be continued...
- JST + KorBERT + WAEs(Wasserstein AutoEncoder) + Sentiment Dictionary + System Link on website
- 목적: 문맥과 의도를 파악하는 빠른 감정 군집화 알고리즘 생성
