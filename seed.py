import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rk_ai_project.settings')
django.setup()

from csc_services.models import Service

def seed():
    services = [
        {
            "title": "Scholarship",
            "description": "Apply for State and National level scholarships.",
            "documents": "Aadhaar Card, Bank Passbook, Income Certificate, Caste Certificate, Previous Year Marksheet",
            "icon": "fa-solid fa-graduation-cap"
        },
        {
            "title": "PAN Card",
            "description": "Apply for a new PAN card or update existing details.",
            "documents": "Aadhaar Card, 2 Passport Size Photos",
            "icon": "fa-solid fa-id-card"
        },
        {
            "title": "Aadhaar",
            "description": "Download Aadhaar, update details, or book an appointment.",
            "documents": "Enrollment slip or existing Aadhaar number",
            "icon": "fa-solid fa-fingerprint"
        },
        {
            "title": "Driving License",
            "description": "Apply for a learner's or permanent driving license.",
            "documents": "Aadhaar Card, Age Proof, Medical Certificate Form 1-A",
            "icon": "fa-solid fa-car"
        }
    ]

    for svc in services:
        Service.objects.update_or_create(
            title=svc['title'],
            defaults={
                'description': svc['description'],
                'required_documents': svc['documents'],
                'icon_class': svc['icon']
            }
        )
    print("Database seeded with default services.")

if __name__ == "__main__":
    seed()
