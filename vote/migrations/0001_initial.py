# Generated by Django 2.0.13 on 2019-11-06 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='투표 제목')),
                ('candidate_list', models.TextField(verbose_name='후모자 리스트')),
                ('start_time', models.DateTimeField(verbose_name='시작 시간')),
                ('end_time', models.DateTimeField(verbose_name='종료 시간')),
            ],
        ),
    ]