import os
import catboost
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import pickle
app = Flask(__name__)
api = Api(app)
model = pickle.load(open('./Models/PopovMV_JuniorMLContest2022.model', 'rb'))
class MakePrediction(Resource):
    @staticmethod
    def post():

        posted_data = request.get_json()
        ST_YEAR = posted_data['ST_YEAR']
        SEMESTER = posted_data['SEMESTER']
        DEBT_MEAN = posted_data['DEBT_MEAN']
        DEBT_SUM = posted_data['DEBT_SUM']
        DEBT_COUNT = posted_data['DEBT_COUNT']
        DISC_DEBT_MEAN = posted_data['DISC_DEBT_MEAN']
        DISC_DEBT_SUM = posted_data['DISC_DEBT_SUM']
        DISC_DEBT_COUNT = posted_data['DISC_DEBT_COUNT']
        GENDER = posted_data['GENDER']
        CITIZENSHIP = posted_data['CITIZENSHIP']
        EXAM_TYPE = posted_data['EXAM_TYPE']
        EXAM_SUBJECT_1 = posted_data['EXAM_SUBJECT_1']
        EXAM_SUBJECT_2 = posted_data['EXAM_SUBJECT_2']
        EXAM_SUBJECT_3 = posted_data['EXAM_SUBJECT_3']
        ADMITTED_EXAM_1 = posted_data['ADMITTED_EXAM_1']
        ADMITTED_EXAM_2 = posted_data['ADMITTED_EXAM_2']
        ADMITTED_EXAM_3 = posted_data['ADMITTED_EXAM_3']
        ADMITTED_SUBJECT_PRIZE_LEVEL = posted_data['ADMITTED_SUBJECT_PRIZE_LEVEL']
        REGION_ID = posted_data['REGION_ID']
        TYPE_NAME_diffoffset = posted_data['TYPE_NAME_Дифференцированный зачет']
        TYPE_NAME_offset = posted_data['TYPE_NAME_Зачет']
        TYPE_NAME_coursework = posted_data['TYPE_NAME_Курсовой проект']
        TYPE_NAME_exam = posted_data['TYPE_NAME_Экзамен']
        prediction = model.predict([[ST_YEAR, SEMESTER, DEBT_MEAN, DEBT_SUM, DEBT_COUNT,
       DISC_DEBT_MEAN, DISC_DEBT_SUM, DISC_DEBT_COUNT,
       TYPE_NAME_diffoffset, TYPE_NAME_offset,
       TYPE_NAME_coursework, TYPE_NAME_exam, GENDER,
       CITIZENSHIP, EXAM_TYPE, EXAM_SUBJECT_1, EXAM_SUBJECT_2,
       EXAM_SUBJECT_3, ADMITTED_EXAM_1, ADMITTED_EXAM_2,
       ADMITTED_EXAM_3, ADMITTED_SUBJECT_PRIZE_LEVEL, REGION_ID]])[0]
        if prediction == 0:
            predicted_class = 'Не расслабляйся, но мы считаем, что сессия будет сдана без задолженностей'
        else:
            predicted_class = 'Быстро за учебу! Мы считаем, что у тебя велика вероятность появления долгов'
        return jsonify({
            'Prediction': predicted_class
        })
api.add_resource(MakePrediction, '/predict')
if __name__ == '__main__':
    app.run(debug=True)