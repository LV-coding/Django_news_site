# Generated by Django 4.0.2 on 2022-02-12 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News_site',
            fields=[
                ('news_site_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('url', models.EmailField(max_length=254)),
            ],
        ),
    ]
