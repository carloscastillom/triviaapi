import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','sdvsf1989','localhost:5432', database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res=self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success', True])
        self.assertTrue(len(data['categories']))

    def test_get_question(self):
        res=self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success', True])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_beyond_valid_page(self):
        res=self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_question(self):
        question = Question.query.order_by(self.db.desc(Question.id)).first()
        self.assertNotEqual(question, None)
        question_id =question.id
        res = self.client().delete('/questions/'+str(question_id))
        data = json.loads(res.data)
        question = Question.query.get(question_id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question, None)
    
    def test_delete_question_not_processable(self):
        res = self.client().delete('/questions/111111')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
 

    def test_create_question(self):

        new_question = {'question':"new question" , 'answer':'answer' , 'difficulty':1, 'category':1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        #get the last inserted question 
        inserted_question = Question.query.order_by(self.db.desc(Question.id)).first()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], inserted_question.id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    
    def test_create_question_wo_q(self):
        new_question = {'answer':'answer' , 'difficulty':1, 'category':1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_create_question_wo_a(self):
        new_question = {'question':'new question' , 'difficulty':1, 'category':1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_create_question_wo_d(self):
        new_question = {'answer':'answer' , 'question':'new question', 'category':1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_create_question_wo_c(self):
        new_question = {'answer':'answer' , 'difficulty':1, 'question':'new question'}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'],1)

    def test_get_questions_by_category_unvalida(self):
        res = self.client().get('/categories/11111111/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_post_quiz_questions_byCategory(self):
        #get the total number of questions
        res = self.client().get('/questions')
        data = json.loads(res.data)
        total_number =  data['total_questions']

        res = self.client().post('/quizzes', json={'previous_questions':[] , 'quiz_category':{'id':1}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['total_questions'] , total_number)
        self.assertTrue(data['question'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()