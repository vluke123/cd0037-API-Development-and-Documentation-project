import os
from sre_parse import CATEGORIES
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start =  (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response


    @app.route('/questions', methods=["GET"])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories_selection = Category.query.all()
        formatted_categories = [category.format() for category in categories_selection]

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': formatted_categories
        })
    

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
        
            return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
            })
        
        except:
            abort(404)


    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()

        new_question = body.get('question', None) 
        new_category = body.get('category', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        search = body.get('search', None)

        try:    
            if search:
                selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search))
                )

                current_questions = paginate_questions(request, selection)
                if current_questions:
                    return jsonify({
                        'success': True,
                        'questions': current_questions,
                        'total_questions': len(Question.query.all()),
                        })
                else:
                    return jsonify({
                        'success': True,
                        'questions': 'No questions found with search term',
                        })
                    
            if new_question:
                new_insert = Question(
                    question = new_question,
                    category = new_category,
                    difficulty = new_difficulty,
                    answer = new_answer
                )
                new_insert.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                'success': True,
                'inserted question': new_insert.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
                })

            else:
                abort()

        except:
            abort(422)


    @app.route('/categories', methods=['GET'])
    def get_category():
        categories_selection = Category.query.all()
        formatted_categories = [category.format() for category in categories_selection]

        return jsonify({
            'success': True,
            'categories': formatted_categories,
            })


    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def question_based_on_category(category_id):
        try:
            questions = Question.query.filter(Question.category == category_id)
            questions_formatted = [question.format() for question in questions]
            
            if not questions_formatted:
                abort(404)

            return jsonify({
            'success': True,
            'questions': questions_formatted,
            'total_questions': len(questions_formatted)
            })

        except:
            abort(404)


    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json(force=True)

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('category', None)

        try:
            if quiz_category:
                selection = Question.query.filter(Question.category == quiz_category)
                questions_formatted = [question.format() for question in selection]
                quiz_question = random.choice(questions_formatted)

                if previous_questions:
                    while quiz_question['id'] in previous_questions:
                        quiz_question = random.choice(questions_formatted)

                return jsonify({
                'success': True,
                'question': quiz_question,
                })

            selection = Question.query.order_by(Question.id).all()
            questions_formatted = [question.format() for question in selection]
            quiz_question = random.choice(questions_formatted)

            if previous_questions:
                while quiz_question['id'] in previous_questions:
                    quiz_question = random.choice(questions_formatted)

            return jsonify({
                'success': True,
                'question': quiz_question
                })

        except:
            abort(400)
        

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Your requested resource was not found"
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Your request was not processable"
        }), 422


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Server cannot or will not process the request due to client-side error"
        }), 400


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error experienced"
        }), 500

    return app

