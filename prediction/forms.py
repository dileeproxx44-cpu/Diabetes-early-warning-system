from django import forms

from .models import Patient


class PatientForm(forms.ModelForm):

    class Meta:

        model = Patient

        fields = [
            'patient_name',
            'gender',
            'age',
            'hypertension',
            'heart_disease',
            'smoking_history',
            'bmi',
            'HbA1c_level',
            'blood_glucose_level',
            'email'
        ]