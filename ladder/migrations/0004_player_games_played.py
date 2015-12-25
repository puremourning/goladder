# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ladder', '0003_auto_20141031_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='games_played',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
