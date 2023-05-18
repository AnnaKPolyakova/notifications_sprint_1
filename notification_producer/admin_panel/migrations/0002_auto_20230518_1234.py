# Generated by Django 3.2 on 2023-05-18 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['created_at'], 'verbose_name': 'Уведомление', 'verbose_name_plural': 'Уведомления'},
        ),
        migrations.AlterField(
            model_name='notification',
            name='author',
            field=models.ForeignKey(blank=True, help_text='Администратор создавший уведомление', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Администратор создавший уведомление'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='text',
            field=models.TextField(help_text='Текст уведомления', max_length=400, verbose_name='Текст уведомление'),
        ),
    ]