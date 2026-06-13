from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import PatientForm
from .models import Patient, Prediction, Alert
from django.http import HttpResponseForbidden
from ml_models.predict import predict_disease
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (PatientSerializer,PredictionSerializer,AlertSerializer)
from .models import (Patient,Prediction,Alert)
import csv
from django.http import HttpResponse

# ======================================
# HOME PAGE
# ======================================

def home(request):

    return render(request, 'home.html')


# ======================================
# PREDICTION VIEW
# ======================================

@login_required
def predict_view(request):

    result = None
    probability = None
    risk_level = ""
    alert_message = ""
    tips = ""

    if request.method == 'POST':

        form = PatientForm(request.POST)
        print("FORM VALID =", form.is_valid())
        print(form.errors)

        if form.is_valid():
            

            # ======================================
            # SAVE PATIENT DATA
            # ======================================

            patient = form.save(commit=False)
            patient.email = request.user.email
            patient.save()
        
            
            # ======================================
            # GET FORM DATA
            # ======================================

            gender = patient.gender
            age = patient.age
            smoking_history = patient.smoking_history
            hypertension = 1 if patient.hypertension == 'yes' else 0
            heart_disease = 1 if patient.heart_disease == 'yes' else 0
            bmi = patient.bmi
            hba1c = patient.HbA1c_level
            glucose = patient.blood_glucose_level

            # ======================================
            # ENCODE VALUES
            # ======================================

            gender_map = {
                'Male': 1,
                'Female': 0,
                'Other': 2
            }

            smoking_map = {
                'never': 0,
                'No Info': 1,
                'current': 2,
                'former': 3,
                'ever': 4,
                'not current': 5
            }

            gender = gender_map.get(gender, 0)
            smoking_history = smoking_map.get(smoking_history, 0)

            # ======================================
            # PREPARE INPUT DATA
            # ======================================

            input_data = [
                gender,
                age,
                hypertension,
                heart_disease,
                smoking_history,
                bmi,
                hba1c,
                glucose
            ]

            # ======================================
            # ML PREDICTION
            # ======================================

            result, probability = predict_disease(input_data)
           

            # ======================================
            # SAVE PREDICTION
            # ======================================

            prediction = Prediction.objects.create(
                patient=patient,
                prediction_result=result,
                probability=probability
            )

            # ======================================
            # EARLY WARNING SYSTEM
            # ======================================

            if probability >= 80:

                risk_level = "HIGH"

                alert_message = """
🚨 EMERGENCY WARNING 🚨

Very high diabetes risk detected.

Immediate medical consultation is strongly recommended.
"""

                tips = """
• Consult doctor immediately
• Monitor blood sugar daily
• Reduce sugar intake completely
• Take prescribed medicines regularly
• Avoid fast food and soft drinks
• Follow strict diabetic diet
"""

            elif probability >= 40:

                risk_level = "MODERATE"

                alert_message = """
⚠ MODERATE RISK WARNING ⚠

Diabetes risk is increasing.

Lifestyle changes are recommended.
"""

                tips = """
• Reduce sugar quantity
• Take medicines regularly
• Drink more water
• Walk daily for 30 minutes
• Avoid junk food
• Monitor glucose levels weekly
"""

            else:

                risk_level = "LOW"

                alert_message = """
✅ LOW RISK STATUS ✅

Your diabetes risk is currently low.

Maintain healthy lifestyle habits.
"""

                tips = """
• Do daily exercise
• Practice yoga and meditation
• Eat healthy food
• Maintain proper sleep
• Drink enough water
• Continue healthy lifestyle
"""

            # ======================================
            # SAVE ALERT
            # ======================================

            Alert.objects.create(
                prediction=prediction,
                alert_message=alert_message,
                risk_level=risk_level
            )
            # ======================================
            # SEND EMAIL ALERT
            # ======================================

            subject = "AI Disease Risk Alert"

            message = f"""

            Hello {patient.patient_name},

            Prediction Result:
            {result}

            Risk Probability:
            {probability}%

            Risk Level:
            {risk_level}

            Warning Message:
            {alert_message}

            Health Suggestions:
            {tips}

            Stay Safe,
            AI Healthcare System

            """

            

            recipient_email = patient.email

            send_mail(

                subject,

                message,

                'yourgmail@gmail.com',

                [recipient_email],

                fail_silently=False

            )

            # ======================================
            # RESULT PAGE
            # ======================================

        return render(request, 'result.html', {

                'result': result,
                'probability': probability,
                'risk_level': risk_level,
                'alert_message': alert_message,
                'tips': tips

            })

    else:

        
        form = PatientForm()
        

    return render(request, 'predict.html', {

        'form': form

    })


# ======================================
# DASHBOARD VIEW
# ======================================
from django.http import HttpResponseForbidden

@login_required
def dashboard_view(request):

    if request.user.email != "dileepkumarrouthu02@gmail.com":
        return HttpResponseForbidden(
            "Access Denied. Only Admin can access Dashboard."
        )

    total_predictions = Prediction.objects.count()

    high_risk_count = Prediction.objects.filter(
        prediction_result="High Risk of Diabetes"
    ).count()

    low_risk_count = Prediction.objects.filter(
        prediction_result="Low Risk of Diabetes"
    ).count()

    recent_predictions = Prediction.objects.all().order_by(
        '-created_at'
    )[:5]

    context = {
        'total_predictions': total_predictions,
        'high_risk_count': high_risk_count,
        'low_risk_count': low_risk_count,
        'recent_predictions': recent_predictions
    }

    return render(request, 'dashboard.html', context)
# ==========================
# PATIENT API
# ==========================

@api_view(['GET'])
def patients_api(request):

    patients = Patient.objects.all()

    serializer = PatientSerializer(
        patients,
        many=True
    )

    return Response(serializer.data)
@api_view(['POST'])
def predict_api(request):

    data = request.data

    gender = data.get("gender")
    age = float(data.get("age"))
    hypertension = int(data.get("hypertension"))
    heart_disease = int(data.get("heart_disease"))
    smoking_history = data.get("smoking_history")
    bmi = float(data.get("bmi"))
    hba1c = float(data.get("HbA1c_level"))
    glucose = float(data.get("blood_glucose_level"))

    gender_map = {
        "Male": 1,
        "Female": 0,
        "Other": 2
    }

    smoking_map = {
        "never": 0,
        "No Info": 1,
        "current": 2,
        "former": 3,
        "ever": 4,
        "not current": 5
    }

    gender = gender_map.get(gender, 0)
    smoking_history = smoking_map.get(smoking_history, 0)

    input_data = [
        gender,
        age,
        hypertension,
        heart_disease,
        smoking_history,
        bmi,
        hba1c,
        glucose
    ]

    result, probability = predict_disease(input_data)

    return Response({
        "prediction": result,
        "probability": f"{probability:.2f}%"
    })
@api_view(['GET'])
def predictions_api(request):

    predictions = Prediction.objects.all()

    serializer = PredictionSerializer(
        predictions,
        many=True
    )

    return Response(serializer.data)
@api_view(['GET'])
def alerts_api(request):

    alerts = Alert.objects.all()

    serializer = AlertSerializer(
        alerts,
        many=True
    )

    return Response(serializer.data)
def history_view(request):

    predictions = Prediction.objects.filter(
        patient__email=request.user.email
    ).order_by('-created_at')

    return render(
        request,
        'history.html',
        {'predictions': predictions}
    )
def profile_view(request):

    total_predictions = Prediction.objects.filter(
        patient__email=request.user.email
    ).count()

    context = {
        'username': request.user.username,
        'email': request.user.email,
        'date_joined': request.user.date_joined,
        'total_predictions': total_predictions
    }

    return render(
        request,
        'profile.html',
        context
    )
@login_required
def export_csv(request):

    if request.user.email != "dileepkumarrouthu02@gmail.com":

        return HttpResponse("Access Denied")

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="predictions.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'Patient',
        'Prediction',
        'Probability'
    ])

    predictions = Prediction.objects.all()

    for prediction in predictions:

        writer.writerow([
            prediction.patient.patient_name,
            prediction.prediction_result,
            prediction.probability
        ])

    return response