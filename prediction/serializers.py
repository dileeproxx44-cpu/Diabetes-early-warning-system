from rest_framework import serializers
from .models import Patient, Prediction, Alert


# ==========================
# PATIENT SERIALIZER
# ==========================

class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = '__all__'


# ==========================
# PREDICTION SERIALIZER
# ==========================

class PredictionSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(
        source='patient.patient_name',
        read_only=True
    )

    class Meta:
        model = Prediction
        fields = '__all__'


# ==========================
# ALERT SERIALIZER
# ==========================

class AlertSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(
        source='prediction.patient.patient_name',
        read_only=True
    )

    class Meta:
        model = Alert
        fields = '__all__'