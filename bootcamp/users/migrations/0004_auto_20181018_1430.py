# Generated by Django 2.1.2 on 2018-10-18 14:30

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20181016_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+918830285891', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('staff', 'staff'), ('student', 'student')], default='student', max_length=10),
        ),
    ]
