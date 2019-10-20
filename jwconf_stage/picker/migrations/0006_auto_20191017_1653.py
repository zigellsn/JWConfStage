# Generated by Django 2.2.6 on 2019-10-17 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('picker', '0005_auto_20190331_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='credential',
            name='extractor_url',
            field=models.CharField(blank=True, default='http://localhost:5000/api/subscribe', max_length=200),
        ),
        migrations.AlterField(
            model_name='credential',
            name='touch',
            field=models.BooleanField(default=True),
        ),
    ]
