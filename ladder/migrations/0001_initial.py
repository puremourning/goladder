# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('komi', models.FloatField()),
                ('handicap', models.IntegerField()),
                ('result', models.CharField(max_length=1, choices=[(b'W', b'White win'), (b'B', b'Black win'), (b'D', b'Draw - match abandoned')])),
                ('result_type', models.CharField(max_length=1, choices=[(b'R', b'Resignation'), (b'O', b'Time out'), (b'T', b'Territory')])),
                ('score_black', models.FloatField(null=True)),
                ('score_white', models.FloatField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('rating', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='match',
            name='black',
            field=models.ForeignKey(related_name='+', to='ladder.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='white',
            field=models.ForeignKey(related_name='+', to='ladder.Player'),
            preserve_default=True,
        ),
    ]
