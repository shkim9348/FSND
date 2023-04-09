# Pybo Board

frontend : next.js, react-bootstrap
backend : flask, sqlalchemy
python v3.10.10

### Project structure
```
├── README.md
├── backend
│   ├── README.md
│   ├── config.py
│   ├── migrations
│   │   ├── README
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   ├── package-lock.json
│   ├── package.json
│   ├── pybo
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── models.py
│   │   └── views.py
│   ├── pybo.db
│   └── requirements-dev.txt
└── frontend
    ├── README.md
    ├── components
    │   ├── answerForm.js
    │   ├── formError.js
    │   ├── navbar.js
    │   ├── pagination.js
    │   └── questionForm.js
    ├── contexts
    │   └── context.js
    ├── jsconfig.json
    ├── lib
    │   └── models.js
    ├── next.config.js
    ├── package-lock.json
    ├── package.json
    ├── pages
    │   ├── _app.js
    │   ├── _document.js
    │   ├── answer
    │   │   └── modify.js
    │   ├── index.js
    │   ├── question
    │   │   ├── create.js
    │   │   └── modify.js
    │   └── question.js
    ├── public
    │   ├── favicon.ico
    │   ├── next.svg
    │   ├── thirteen.svg
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

---

### Frontend

```bash
npm install
npm run dev
```

### API info
forntend(cdn)
`udacity-shkim.stage.ver.team`  
backend (api server reverse proxy)  
`shkim-api.ver.team/question`  
- api server ip: 115.68.17.216  
- api server test: http://115.68.17.216:5001/
