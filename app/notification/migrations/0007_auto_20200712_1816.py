# Generated by Django 3.0.7 on 2020-07-12 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0006_auto_20200712_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='active',
            field=models.BooleanField(verbose_name='Aktiv'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='importance',
            field=models.IntegerField(choices=[(0, 'Information'), (1, 'Wichtig'), (2, 'Dringend'), (3, 'Warnung')], default=0, verbose_name='Wichtigkeit'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='locale',
            field=models.CharField(default=' ', max_length=10, verbose_name='Sprache'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='max_duration',
            field=models.IntegerField(verbose_name='Gültigkeitsdauer'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(blank=True, default='', verbose_name='Nachricht'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='subject',
            field=models.CharField(default='', max_length=255, verbose_name='Betreff'),
        ),
    ]
