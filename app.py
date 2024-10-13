from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib

app = Flask(__name__, static_folder='static', template_folder='templates')

# تحميل النموذج المدرب
model = joblib.load('depression_model.pkl')
@app.route('/result/<depression_percentage>')
def result(depression_percentage):
    return render_template('result.html', depression_percentage=depression_percentage)

# دالة لتحويل الإدخالات إلى شكل يناسب النموذج
def encode_input(age, gender, profession, marital_status,
                 satisfied_life, dropped_activities, feel_life_empty,
                 bored, feel_helpless, afraid_bad_happening,
                 hopeful_about_future, spend_time_happily,
                 feel_energy, prefer_stay_home, avoiding_social_gatherings,
                 memory_loss, consider_worthless, cry_most_of_the_time,
                 sleep_well, feeling_reduce_appetite, situation_hopeless,
                 people_better_than_you, feel_bad_and_guilty,
                 others_would_better_you_died):

    # ترميز الميزات
    gender_encoded = 0 if gender == 'Male' else 1
    profession_encoded = {'Student': 0, 'Employee': 1, 'Others': 2}.get(profession, 2)
    marital_status_encoded = {'Single': 0, 'Married': 1, 'Divorced': 2}.get(marital_status, 0)

    binary_features = [1 if x == 'Yes' else 0 for x in [
        satisfied_life, dropped_activities, feel_life_empty, bored,
        feel_helpless, afraid_bad_happening, hopeful_about_future,
        spend_time_happily, feel_energy, prefer_stay_home, 
        memory_loss, consider_worthless, cry_most_of_the_time,
        feeling_reduce_appetite, situation_hopeless, 
        people_better_than_you, others_would_better_you_died
    ]]

    # ترميز AvoidingSocialGatherings و SleepWell و FeelBadAndGuilty
    avoiding_social_gatherings_encoded = {
        'Most of The Time': 2,
        'Sometimes': 1,
        'Not at All': 0
    }.get(avoiding_social_gatherings, 0)

    sleep_well_encoded = {
        'Most of The Time': 2,
        'Sometimes': 1,
        'Not at All': 0
    }.get(sleep_well, 0)

    feel_bad_and_guilty_encoded = {
        'Most of The Time': 2,
        'Sometimes': 1,
        'Not at All': 0
    }.get(feel_bad_and_guilty, 0)

    # حساب AgeGroup
    if age < 21:
        age_group = 0  # '13-20'
    elif 21 <= age <= 30:
        age_group = 1  # '21-30'
    elif 31 <= age <= 40:
        age_group = 2  # '31-40'
    elif 41 <= age <= 50:
        age_group = 3  # '41-50'
    else:
        age_group = 4  # '51+'

    # إعداد البيانات للتوقع
    features = np.array([[age, gender_encoded, profession_encoded, marital_status_encoded] +
                         binary_features + 
                         [avoiding_social_gatherings_encoded, sleep_well_encoded, 
                          feel_bad_and_guilty_encoded, age_group]])
    
    return features

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    features = encode_input(data['age'], data['gender'], data['profession'], data['marital_status'],
                            data['satisfied_life'], data['dropped_activities'], data['feel_life_empty'],
                            data['bored'], data['feel_helpless'], data['afraid_bad_happening'],
                            data['hopeful_about_future'], data['spend_time_happily'],
                            data['feel_energy'], data['prefer_stay_home'], data['avoiding_social_gatherings'],
                            data['memory_loss'], data['consider_worthless'], data['cry_most_of_the_time'],
                            data['sleep_well'], data['feeling_reduce_appetite'], data['situation_hopeless'],
                            data['people_better_than_you'], data['feel_bad_and_guilty'],
                            data['others_would_better_you_died'])

    # توقع النتيجة
    probabilities = model.predict_proba(features)  # الحصول على احتمالات الاكتئاب
    depression_percentage = probabilities[0][1] * 100  # تحويل الاحتمال إلى نسبة مئوية

    return jsonify({'depression_percentage': float(depression_percentage)})  # أعد النسبة المئوية

if __name__ == '__main__':
    app.run(debug=True)
