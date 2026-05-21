
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from prediction.models import Prediction


class Command(BaseCommand):

    help = 'Send automatic health warning alerts'

    def handle(self, *args, **kwargs):

        predictions = Prediction.objects.all()

        for prediction in predictions:

            patient = prediction.patient

            probability = prediction.probability

            subject = "Healthcare Early Warning Alert"


            # =====================================
            # HIGH RISK
            # =====================================

            if probability >= 80:

                message = f"""

Hello {patient.patient_name},

Your previous diabetes prediction indicates VERY HIGH RISK.

Risk Probability: {probability}%

Emergency Recommendations:


- Consult doctor immediately
- Monitor sugar levels daily
- Avoid sugar foods
- Follow diabetic diet
- Take medicines regularly

This is an automated AI healthcare alert.

                """
                  # =====================================
            # MODERATE RISK
            # =====================================

            elif probability >= 40:

                message = f"""

Hello {patient.patient_name},

Your diabetes risk is MODERATE.

Risk Probability: {probability}%

Recommendations:
- Reduce sugar intake
- Walk daily
- Exercise regularly
- Drink more water
- Monitor glucose weekly

This is an automated AI healthcare alert.

                """
                  # =====================================
            # LOW RISK
            # =====================================

            else:

                message = f"""

Hello {patient.patient_name},

Your diabetes risk is LOW.

Risk Probability: {probability}%

Health Tips:

- Continue healthy diet
- Exercise daily
- Practice yoga
- Maintain healthy sleep
This is an automated AI healthcare alert.

                """
                 # =====================================
            # SEND EMAIL
            # =====================================

            send_mail(
                subject,
                message,
                'yourgmail@gmail.com',
                [patient.email],
                fail_silently=False,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Alert sent to {patient.email}'
                )
            )
