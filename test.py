import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# تحميل النموذج المدرب
model = joblib.load('model.pkl')

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

# مثال لاستخدام الدالة
age = int(input("Enter Age: "))
gender = input("Enter Gender (Male/Female): ")
profession = input("Enter Profession (Student/Employee/Others): ")
marital_status = input("Enter Marital Status (Single/Married/Divorced): ")
satisfied_life = input("Satisfied Life? (Yes/No): ")
dropped_activities = input("Dropped Activities? (Yes/No): ")
feel_life_empty = input("Feel Life Empty? (Yes/No): ")
bored = input("Bored? (Yes/No): ")
feel_helpless = input("Feel Helpless? (Yes/No): ")
afraid_bad_happening = input("Afraid of Bad Happening? (Yes/No): ")
hopeful_about_future = input("Hopeful About Future? (Yes/No): ")
spend_time_happily = input("Spend Time Happily? (Yes/No): ")
feel_energy = input("Feel Energy? (Yes/No): ")
prefer_stay_home = input("Prefer Stay Home? (Yes/No): ")
avoiding_social_gatherings = input("Avoiding Social Gatherings? (Most of The Time/Sometimes/Not at All): ")
memory_loss = input("Memory Loss? (Yes/No): ")
consider_worthless = input("Consider Worthless? (Yes/No): ")
cry_most_of_the_time = input("Cry Most of The Time? (Yes/No): ")
sleep_well = input("Sleep Well? (Most of The Time/Sometimes/Not at All): ")
feeling_reduce_appetite = input("Feeling Reduce Appetite and Losing Weight? (Yes/No): ")
situation_hopeless = input("Situation Hopeless? (Yes/No): ")
people_better_than_you = input("People Better Than You? (Yes/No): ")
feel_bad_and_guilty = input("Feel Bad and Guilty? (Most of The Time/Sometimes/Not at All): ")
others_would_better_you_died = input("Others Would Better You Died? (Yes/No): ")

# تحويل الإدخالات إلى ميزات
features = encode_input(age, gender, profession, marital_status,
                        satisfied_life, dropped_activities, feel_life_empty,
                        bored, feel_helpless, afraid_bad_happening,
                        hopeful_about_future, spend_time_happily,
                        feel_energy, prefer_stay_home, avoiding_social_gatherings,
                        memory_loss, consider_worthless, cry_most_of_the_time,
                        sleep_well, feeling_reduce_appetite, situation_hopeless,
                        people_better_than_you, feel_bad_and_guilty,
                        others_would_better_you_died)

# توقع النتيجة
result = model.predict(features)
print("Result:", "Depressed" if result[0] == 1 else "Not Depressed")
