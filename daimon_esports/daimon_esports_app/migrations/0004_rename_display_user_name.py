# Generated by Django 5.0.6 on 2024-07-06 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daimon_esports_app', '0003_alter_game_score1_alter_game_score2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='display',
            new_name='name',
        ),
    ]
