# Generated by Django 4.1.2 on 2022-10-25 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_sequences', '0002_populate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequence',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='stageresult',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='stagestate',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]