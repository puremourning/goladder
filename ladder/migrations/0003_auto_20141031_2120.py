# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0002_auto_20141030_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='result_type',
            field=models.CharField(default=b'T', max_length=1, blank=True, choices=[(b'R', b'Resignation'), (b'O', b'Time out'), (b'T', b'Territory'), (b'', b'n/a')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='rating',
            field=models.IntegerField(db_index=True),
            preserve_default=True,
        ),
    ]
