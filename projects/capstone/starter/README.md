# nano degree

frontend : next.js, react-bootstrap
backend : flask, sqlalchemy
python v3.10.10

project 구조
```
├── README.md
├── backend
│   ├── README.md
│   ├── config.py
│   ├── pybo
│   │   ├── __init__.py
│   │   ├── auth
│   │   │   ├── __init__.py
│   │   │   └── auth.py
│   │   ├── database
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   └── views
│   │       └── main_views.py
│   ├── pybo.db
│   └── pybo_test.db
└── frontend
    └── pybo
        ├── README.md
        ├── components
        ├── package-lock.json
        ├── package.json
        ├── pages
        │   ├── _app.js
        │   └── index.js
        ├── public
        │   ├── favicon.ico
        │   └── vercel.svg
        └── styles
            ├── Home.module.css
            └── globals.css
```

### Backend

```bash
pip install Flask
pip install flask-migrate
pip install black
pip install Flask-Cors
pip install python-jose requests
```

```
export FLASK_APP=pybo
export FLASK_ENV=development
# testing
# export FLASK_ENV="testing"
# product
# export FLASK_ENV="product"
export FLASK_DEBUG=true
flask run
```


curl 테스트

```bash
curl -X GET http://127.0.0.1:5000/api/board
```

게시판 데이터 udactiypartner 활용

```bash
https://api.udacitypartner.com/api/v1/information/notice/
```

[https://auth0.com/](https://auth0.com/)에서 pybo 설정

---

### Frontend

pybo frontend 설치

```bash
npm install
npm run dev
```

![Untitled](nano%20degree%202203bfca063c47e78473ba0b1fd73864/Untitled.png)
