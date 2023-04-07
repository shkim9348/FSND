# Pybo Board

PYBO is a notice board web application built using Next.js framework.

It allows users to create and answer questions, and upvote answers. The app uses a custom REST API for data storage and retrieval.

## Installation

To install the project, clone the repository and run the following commands:

```
npm install
npm run dev
```

- This will install the necessary dependencies and start a development server at http://localhost:3000.

## Features

- Create and view notices
- Leave comments on notices
- Ask and answer questionsUser authentication and authorizationEdit and delete notices, comments, and answers
- Technologies used Next.js

## Project Structure

The project structure is as follows:

```
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
