# Generated by Django 4.2 on 2024-09-09 00:04

from django.db import migrations
from loan_manager.models import User

def create_admin_user(apps, schema_editor):
    User = apps.get_model('loan_manager', 'User')
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin', 
            email='admin@example.com', 
            password='123456'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('loan_manager', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin_user)
    ]
