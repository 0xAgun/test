# Generated by Django 4.0.4 on 2022-05-13 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_userprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userreports',
            name='image',
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('reports', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userreports')),
            ],
        ),
    ]
