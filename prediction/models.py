from django.db import models


# =====================================
# PATIENT MODEL
# =====================================

class Patient(models.Model):

    patient_name = models.CharField(max_length=120)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    SMOKING_CHOICES = [
        ('never', 'Never'),
        ('No Info', 'No Info'),
        ('current', 'Current'),
        ('former', 'Former'),
        ('ever', 'Ever'),
        ('not current', 'Not Current')
    ]

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)

    age = models.FloatField()

    hypertension = models.IntegerField()

    heart_disease = models.IntegerField()

    smoking_history = models.CharField(max_length=20, choices=SMOKING_CHOICES)

    bmi = models.FloatField()

    HbA1c_level = models.FloatField()

    blood_glucose_level = models.FloatField()

    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name
    
    # =====================================
# PREDICTION MODEL
# =====================================

class Prediction(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    prediction_result = models.CharField(max_length=100)

    probability = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.patient_name} - {self.prediction_result}"
    
# =====================================
# ALERT MODEL
# =====================================

class Alert(models.Model):

    prediction = models.ForeignKey(
        Prediction,
        on_delete=models.CASCADE
    )

    alert_message = models.TextField()

    risk_level = models.CharField(max_length=50)

    email_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.risk_level