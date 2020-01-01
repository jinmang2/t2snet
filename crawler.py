#-*- coding:utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup

def getMovieCodebyDate(sel, date, tg=0, page=1):
    """
    *------------------------DESRIPTION-----------------------*
    네이버 영화 코드를 얻기 위한 크롤러
    NAVER 영화랭킹에서 코드를 추출하며 sel, date, tg, page의
    query를 argument로 받아 결과를 리턴한다.
    *------------------------PARAMETER------------------------*
    sel  : 조회순 | 평점순(현재상영영화) | 평점순(모든영화)
           cnt    | cur                  | pnt
    date : 조회할 날짜
           ex) '20190930'
    tg   : 장르, cnt, pnt만 존재
           ex)
               <value="1">  드라마
               <value="2">  판타지
               <value="4">  공포
               <value="5">  멜로/애정/로맨스
               <value="6">  모험
               <value="7">  스릴러
               <value="8">  느와르
               <value="10"> 다큐멘터리
               <value="11"> 코미디
               <value="12"> 가족
               <value="13"> 미스터리
               <value="14"> 전쟁
               <value="15"> 애니메이션
               <value="16"> 범죄
               <value="17"> 뮤지컬
               <value="18"> SF
               <value="19"> 액션
    page : 평점순(모든영화)일 경우 유효, 1~40 (2000개의 영화)
    *------------------------USAGE----------------------------*
    [Input] 
            res = []
            for i in range(1, 4):
              res.extend(getMovieCodebyDate('pnt', '20190929', page=i)
    
            res[::50]
    [Output]
            [('182699', '사랑의 선물', 9.67),
             ('19079', '굿 윌 헌팅', 9.33),
             ('10021', '록키', 9.28),
             ('109193', '드래곤 길들이기 3', 9.25),
             ('17903', '아름다운 비행', 9.21),
             ('10047', '스팅', 9.18),
             ('34497', '하치 이야기', 9.13),
             ('17327', '히트', 9.1),
             ('36944', '올드보이', 9.06),
             ('17265', '이연걸의 정무문', 9.02),
             ('146512', '스플릿', 9.0),
             ('10751', '블루 라군', 8.97),
             ('44728', '오만과 편견', 8.93),
             ('91031', '신세계', 8.9),
             ('98276', '굿모닝 맨하탄', 8.86),
             ('115240', '10분', 8.84),
             ('158610', '쓰리 빌보드', 8.81),
             ('76560', '극장판 도라에몽: 진구와 철인군단 날아라 천사들', 8.78),
             ('36950', '도그빌', 8.74),
             ('73411', '쿵푸 팬더 2', 8.72),
             ('44981', '보이 A', 8.69),
             ('137281', '짱구는 못말려 극장판: 나의 이사 이야기 선인장 대습격', 8.66),
             ('37073', '고양이의 보은', 8.62),
             ('134963', '라라랜드', 8.59),
             ('18015', '단테스 피크', 8.56),
             ('149757', '윈드 리버', 8.52),
             ('62167', '식객', 8.48),
             ('140695', '럭키', 8.45),
             ('63515', '파프리카', 8.41),
             ('47425', '드림업', 8.38),
             ('151153', '아쿠아맨', 8.35),
             ('167105', '암수살인', 8.32),
             ('76439', '킹스 스피치', 8.29),
             ('127866', '구스범스', 8.26),
             ('90885', '나의 PS 파트너', 8.22),
             ('65242', '페넬로피', 8.2),
             ('33837', '바람의 파이터', 8.16),
             ('50903', '해피 플라이트', 8.13),
             ('87716', '모모와 다락방의 수상한 요괴들', 8.09),
             ('75395', '의뢰인', 8.05)]
    *---------------------------------------------------------*
    """
    # query text 작성
    query_text = 'sel={sel}&tg={tg}&date={date}&page={page}'.format(
        sel=sel, tg=tg, date=date, page=page)
    # requests로 html source code를 얻고 이를 bs4로 parsing
    req = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?' + query_text)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    # tit3 : cnt, tit5 : cur, pnt
    titnum = 3 if sel == 'cnt' else 5
    # 영화의 code값과 타이틀 명을 list 형태로 저장
    res = [(content['href'].split('code=')[-1], content['title']) 
               for content in soup.select('div.tit{} > a'.format(titnum))]
    # cur, pnt의 경우 평점(point)가 존재. 이를 영화 code값, 타이틀 명과 함께 저장
    if soup.select('td.point') != []:
        res = [(*i, float(j.text)) for i, j in zip(res, soup.select('td.point'))]
    # 결과값을 return
    return res

def getNaverMovieReviewbyCode(moviecode, pages, newest=True):
    # 영화 리뷰를 얻기 위해 네이버 영화 평점 창으로 이동 후 html parsing
    req = requests.get('https://movie.naver.com/movie/bi/mi/point.nhn?code=' + moviecode)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.select('p.info_spec > span > a') == []:
        print('{:>6} : PASS... HuhHuhHuh...'.format(moviecode))
        return None
    # 영화 정보
    Year, MonthDay, Type = soup.select('p.info_spec > span > a')[:5][-3:]
    # 영화 이름
    moviename = soup2.select('meta[property="me2:category2"]')[0]['content']
    
    # 데이터 결과값을 받을 dictionary 객체 생성
    res = {'MovieName':[], 'MovieCode':[], 'MovieComeOut':[], 'MovieType':[],
           'ReviewCreateTime':[], 'author':[], 'point':[], 'sympathy':[], 'notsympathy':[], 'review':[]}
    order = '&order=newest' if newest else ''
    navermovielink = 'https://movie.naver.com' + soup.select('iframe')[0]['src'] + order
    buffer = None
    for page in range(pages):
        # 영화 평점에 관한 문서는 다른 page link로 넘어감. 새로 받아서 html parsing
        q_page = '&page={}'.format(page)
        movie_review_doclink = navermovielink + q_page
        req = requests.get(movie_review_doclink)
        soup = BeautifulSoup(req.text, 'html.parser')
        # 영화 리뷰, 마지막 페이지 판별을 위해 buffer에 저장 후 비교
        review = [i.text.strip() for i in soup.select('div.score_reple > p')]
        if review == buffer:
            break
        else:
            buffer = [i.text.strip() for i in soup.select('div.score_reple > p')]
        # 영화 정보 입력
        res['MovieName'].extend([moviename] * len(review))
        res['MovieCode'].extend([moviecode] * len(review))
        res['MovieComeOut'].extend([Year.text + MonthDay.text] * len(review))
        res['MovieType'].extend([Type.text] * len(review))
        # 영화 리뷰
        review = [s[:s.find('\udc3d')] +  s[s.find('\udc3d') + len('\udc3d'):] 
                    if '\udc3d' in s else s for s in review]
        res['review'].extend(review)
        # 영화 평점
        res['point'].extend([float(i.text) for i in soup.select('div.star_score > em')])
        # 해당 리뷰에 대한 공감
        res['sympathy'].extend([int(i.text) for i in soup.select('div.btn_area > strong > span')][::2])
        # 해당 리뷰에 대한 비공감
        res['notsympathy'].extend([int(i.text) for i in soup.select('div.btn_area > strong > span')][1::2])
        # 해당 리뷰 작성자
        res['author'].extend([i.text for i in soup.select('div.score_reple > dl > dt > em > a > span')])
        # 리뷰 작성 일자 및 시각
        res['ReviewCreateTime'].extend([i.text for i in soup.select('div.score_reple > dl > dt > em:nth-of-type(2)')])
    print('{:>6} : {:>03}'.format(moviecode, page), 'page is final. Done', end='')
    return res

def getMemUsage(dict_list_obj):
    res = 0
    for value in dict_list_obj.values():
        res += sum([sys.getsizeof(i) for i in value])
    return res / 1024 / 1024
   
  
CrawledData = {'MovieName':[], 'MovieCode':[], 'MovieComeOut':[], 'MovieType':[],
               'ReviewCreateTime':[], 'author':[], 'point':[], 'sympathy':[], 'notsympathy':[], 'review':[]}
               
for ind, (moviecode, moviename, moviepoint) in enumerate(res[:]):
    r = getNaverMovieReviewbyCode(moviecode, 500)
    if not r: continue
    for key, value in r.items():
        CrawledData[key].extend(value)
    memusage = getMemUsage(CrawledData)
    print('\t/\tmemusage : {:>7.2f}MB'.format(memusage))
    if memusage > 1024 / 2:
        time = nowtime()
        print('512MB 초과, 중간 저장합니다. 현재까지 진행경과 내역\n\t{} / {}'.format(ind+0, len(res)), end='')
        with open('d:/naver_review/CrawledData_{}_{}.json'.format(time), 'w', encoding='utf-8') as make_file:
            json.dump(CrawledData, make_file, ensure_ascii=False, indent="\t")
        print('\t파일 이름: {}으로 저장합니다.'.format('CrawledData_{}.json'.format(time)))
        print('*----데이터 초기화---*')
        CrawledData = {'MovieName':[], 'MovieCode':[], 'MovieComeOut':[], 'MovieType':[],
           'ReviewCreateTime':[], 'author':[], 'point':[], 'sympathy':[], 'notsympathy':[], 'review':[]}