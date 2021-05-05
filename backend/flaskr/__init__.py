import os
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
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={'/': {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories', methods= ['GET'])
  def get_categories():

      page = request.args.get('page', 1, type=int)
      start = (page-1)*10
      end = start + 10 
      categories = Category.query.all()
      formatted_categories = [category.format() for  category in categories ]
      
        # abort 404 if no questions
      if (len(formatted_categories) == 0):
          abort(404)

        # return data to view
      return jsonify({
          'success': True,
          'categories': formatted_categories
        })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''  
  @app.route('/questions', methods= ['GET'])
  def get_questions():
      page = request.args.get('page', 1, type=int)
      start = (page-1)*10
      end = start + 10 
      questions = Question.query.all()
      formatted_questions = [question.format() for  question in questions ]
      total_questions = len(formatted_questions)
      # current_questions = paginate_questions(request, selection)

      # get all categories and add to dict
      categories = Category.query.all()
      categories_dict = {}
      for category in categories:
          categories_dict[category.id] = category.type

        # abort 404 if no questions
      if (len(formatted_questions) == 0):
          abort(404)

        # return data to view
      return jsonify({
          'success': True,
          'questions': formatted_questions[start:end],
          'total_questions': total_questions,
          'categories': categories_dict
        })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 

  '''
  @app.route('/question/<int:id>', methods=['DELETE'])
  def delete_question(id):
      try:
          question = Question.query.filter_by(id=id).one_or_none()

          if question is None:
              abort(404)
          
          question.delete()

          return jsonify({
              'success': True,
              'delete': id
          })
      except:
          abort(422)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/question', methods=['POST'])
  def create_book():
      body = request.get_json()


      if (body.get('searchTerm')):
          search_term = body.get('searchTerm')

          selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

          formatted_questions = [question.format() for  question in selection ]

          return jsonify({
              'success': True,
              'questions': formatted_questions,
              'total_questions': len(Question.query.all())
          })    
      else:
         new_question=body.get('question', None)
         new_answer=body.get('answer', None)
         new_category=body.get('category', None)
         new_difficulty=body.get('difficulty', None)
        
         try:
             question=Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
             question.insert()

             selection = Question.query.all()
             formatted_questions = [question.format() for  question in questions]

             return jsonify({
                 'success': True,
                 'questions': formatted_questions
             })

         except:
             abort(422)



  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_category(id):
      page = request.args.get('page', 1, type=int)
      start = (page-1)*10
      end = start + 10 
      category = Category.query.filter_by(id=id).one_or_none()
      questions = Question.query.filter_by(category=category.id).all()
      formatted_questions = [question.format() for  question in questions ]
      total_questions = len(formatted_questions)

      if (len(formatted_questions) == 0):
          abort(404)

      return jsonify({
          'success': True,
          'questions': formatted_questions
      })



  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():

        body = request.get_json()
        pre_question = body.get('previous_questions')
        category = body.get('quiz_category')

        if ((category is None) or (pre_question is None)):
            abort(400)

        if (category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category['id']).all()

        total = len(questions)

        def get_random_question():
            return questions[random.randrange(0, len(questions))]

        # checks to see if question has already been used
        def check_previous(question):
            is_used = False
            for ques in pre_question:
                if (ques == question.id):
                    is_used = True

            return used

        # get random question
        question = get_random_question()

        # check if used, execute until unused question found
        while (check_previous(question)):
            question = get_random_question()

            if (len(pre_question) == total):
                return jsonify({
                    'success': True
                })

        # return the question
        return jsonify({
            'success': True,
            'question': question.format()
        })



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": MESSAGE_NOT_FOUND
      }), 404


  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": MESSAGE_UNPROCESSABLE
      }), 422






  
  return app



