# API Documentation

## Introduction
This is project is a quiz API. It's a simple API that allows you to select questions from a list of categories and produce quiz games. Users are able to add their own questions as well as delete plus play a quiz game of selected categories.

### Frontend

The frontend directory contains a complete React frontend to consume the data from the Flask server.

### Backend

The backend directory contains a completed Flask and SQLAlchemy server.

## Getting Started

Users should ensure that all of the initial requirements are installed from the `requirements.txt` file. Without these dependencies the backend will not be able to function correctly. You can easily install the requirements by performing the python command:

```bash
pip install -r requirements.txt
```

The original database used is within the `trivial.psql` file; users need to ensure that their PostgreSQL server is already setup. With Postgres running, create a trivia database:

```powershell
createbd trivia
```

To login via Windows you'll need to execute the psql.exe application via the cmd line:

```powershell
C:\"Program Files"\PostgreSQL\14\bin\psql.exe -d postgres -U postgres
```

You'll also need to add the bin files as a system variable within the Windows Environment to execute commands from the cmd line.

Populate the database using the trivia.psql file provided. From the backend folder in terminal run:

```powershell
psql trivia < trivia.psql
```

You also need to start the postgresql server itself:

```powershell
C:\"Program Files"\PostgreSQL\14\bin\pg_ctl.exe -D "C:\Program Files\PostgreSQL\14\data" start
```

To run the server, execute:

```powershell
flask run
```

## Endpoints

### GET /questions

This is the most basic endpoint that allows you to pull *all* questions from the API as well as display a list of all categories available. The expected response will always be in the following format:

```json
'questions': [
    {
      'id': 'integer',
      'question': 'the question',
      'answer': 'the answer',
      'difficulty': 'level of difficulty for the question out of 5',
      'category': 'category id'
  }
],
'total_questions': number of questions
'categories': categories
```

Each return will be paginated with 10 questions per page plus the additional returns of ```total_questions``` and ```categories```. You can request the second page of your results by adding in a standard query onto the end of your request such as:

```bash
GET '/questions?page=${integer}'
```

Here, `{integer}` is replaced with the page number that you wish to request. 

### GET /categories

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category. It will return an object with a single key of `categories` which contains:

```json
{
    'categories': { 
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" 
    }
}
```

### GET /categories/${id}/questions

Fetches questions for a category specified by id request argument where `{id}` will be the category id. This will then return an object with a list of questions that have been assigned the requested category id number. The total number of questions for this category will also be displayed, an example response is below:

```json
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

### DELETE /questions/${id}

Deletes a specified question where the `{id}` is the question id you wish to delete. If successful it will return a `200` HTTP status code or a `404` if the specific id is not available.

### POST /questions

#### Create Question

If sending a post request to the route `/questions`, the API will attempt to create a question from the `arguments` inputted or expect a `search` term. The arguments expected from the server are as follows for creating a question:

```json
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
```

If the POST request is successful, no return will be given other than a `200` HTTP code.

#### Search term

A secondary POST request that can be made to `/questions` is the use of the `search` argument. The search argument should be a particular word or phrase that is in one of the questions within the SQL database. The expected return will be:

```json

{
    'success': True,
    'questions': 'list of questions - paginated',
    'total_questions': 'total questions',
}
```

If there are no questions returned, the server will return a `Success: 'True'` value still but state that `'questions': 'No questions found with search term'`.

### POST /quizzes

This is the primary function to play a quiz game. The API will return a question at random unless the question has been returned previously. The expected arguments are:

```json
'previous_questions' = 'list of question ids already asked'
'category' = 'if selecting a specfic category'
```

A successful return is still given even if these arguments are not given to the API. Should a category be given in the argument, then the return will only include questions from that particular category. The expected return is as follow:

```json
'success': True,
'question': quiz_question
```

where `quiz_question` is the full question, answer, id and category as expected similar to a return from `GET /questions`. The question.

### Errors

All errors are returned in the same format should the API not be able process a request for a given reason:

```json
"success": True or False,
"error": HTTP Error Code,
"message": "message for particular code"
```

The expected messages are as follow for certain HTTP status codes

#### 400

```json
"message": "Server cannot or will not process the request due to client-side error"
```

#### 404

```json
"message": "Your requested resource was not found"
```

#### 422

```json
"message": "Your request was not processable"
```

#### 500

```json
"message": "Internal server error experienced"
```