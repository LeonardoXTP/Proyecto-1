# Generated by Django 5.0.3 on 2024-03-25 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('encuestas', '0002_rename_respuestas_respuesta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='respuesta',
            old_name='opcion',
            new_name='respuesta',
        ),
    ]