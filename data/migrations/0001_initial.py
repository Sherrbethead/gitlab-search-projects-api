# Generated by Django 3.0.4 on 2020-03-14 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_query', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GitlabData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('last_activity_at', models.DateTimeField()),
                ('search_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gitlab_data', to='data.SearchData')),
            ],
        ),
    ]