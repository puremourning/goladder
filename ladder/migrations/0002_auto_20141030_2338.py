# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='result_type',
            field=models.CharField(max_length=1, choices=[(b'R', b'Resignation'), (b'O', b'Time out'), (b'T', b'Territory'), (b'', b'n/a')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='score_black',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='match',
            name='score_white',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
