import joblib
import numpy as np
import pandas as pd

class DepressionModel:
    def __init__(self, model_path):
        # تحميل النموذج من الملف
        self.model = joblib.load(model_path)


    def predict(self, features):
        """
        Predict the probability of depression based on input data.

        Parameters:
        input_data (DataFrame): DataFrame containing the input features for prediction.

        Returns:
        float: Probability of depression (as a percentage).
        """
        # تأكد من أن البيانات في نفس الشكل الذي تم تدريب النموذج عليه
        features = pd.DataFrame(features)
        
        # الحصول على احتمالية الاكتئاب
        probabilities = self.model.predict_proba(features)[:, 1]  # Class 1 (مكتئب)
        
        # تحويل الاحتمالات إلى نسب مئوية
        depression_percentage = probabilities * 100
        
        return depression_percentage



"""     def predict(self, features):
        # توقع النتيجة باستخدام النموذج
        result = self.model.predict(features)
        return result 
 """
