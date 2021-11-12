# Asignment3
원티드x위코드 백엔드 프리온보딩 과제4
- 과제 출제 기업 정보
  - 기업명 : 8퍼센트
  
## Members
|이름   |Github                   |Blog|
|-------|-------------------------|--------------------|
|이태성 |[yotae07](https://github.com/yotae07)     | 추가   |
|임유선 |[YusunL](https://github.com/YusunL)   | 추가   |
|윤현묵 |[fall031-muk](https://github.com/fall031-muk) | https://velog.io/@fall031   |
|김정수 |[hollibleling](https://github.com/hollibleling) | https://velog.io/@hollibleling  |
|최현수 |[filola](https://github.com/filola) | https://velog.io/@chs_0303 |

## 과제 내용

계좌 거래 API를 구현해주세요. API는 3가지가 구현되어야 합니다.
  - 거래 내역 조회 API
  - 입금 API
  - 출금 API

</aside>

### [필수 포함 사항]
- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

### [주요 고려 사항]
- 계좌의 잔액을 별도로 관리, 잔액과 거래내역의 잔액의 무결성의 보장
- DB를 설계 할때 각 컬럼의 타입과 제약
- 테스트 편의성을 위해 sqlite를 사용

✔️ **API 상세설명**
---

- 거래내역 조회 API
    - 계좌의 소유주만 요청 가능
    - 거래일시에 대한 필터링 가능
    - 출금, 입금 필터링
    - Pagination 구현
    - 필수 데이터
      - 거래 일시
      - 거래 금액
      - 잔액
      - 거래 종류(출금/입금)
      - 적요 
- 입금 API
    - 계좌의 소유주만 요청 가능
- 출금 API
    - 계좌의 소유주만 요청 가능
    - 계좌 잔액 내에서만 출금 가능 (에러처리 필요)  
  
## 구현 기능
### 회사명 자동완성
- 내용추가

### 회사 이름으로 회사 검색
- header의 x-wanted-language 언어값에 따라 해당 언어로 회사명 검색하여 출력
- 출력에 "company_name", "tags" 포함
- 검색된 회사가 없는경우 404를 리턴

### 새로운 회사 추가
- header의 x-wanted-language 언어값에 따라 해당 언어로 입력값 리턴
- 새로운 언어로 데이터가 추가되면 기존의 데이터베이스에 새로 언어를 생성하고 데이터를 추가
- company_name이나 tag를 입력하지 않을 시 Key_error 

## 기술 스택
- Back-End : python, django-rest-framework, sqlite3
- Tool     : Git, Github, slack, postman

## API

## 실행 방법(endpoint 호출방법)

### ENDPOINT

| Method | endpoint | Request Header | Request Body | Remark |
|:------:|-------------|-----|------|--------|
|GET|/companies/\<str:name\>/|x-wanted-language||회사 이름으로 회사 검색|
|GET|/search/?query=\<str\>|x-wanted-language||회사 검색시 자동 완성|
|POST|/companies|x-wanted-language|company_name,tag_name, language|회사 추가 기능|




## API 명세(request/response)
  
  [Postman link](https://documenter.getpostman.com/view/17228945/UVC5FTD6)

## 폴더 구조
```
├── company
│   ├── __init__.py
│   ├── migrations           
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── pytest.ini
├── requirements.txt
├── README.md
├── test_app.py
└── wanted
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py


```

# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 원티드랩에서 출제한 과제를 기반으로 만들었습니다.
