# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='featured_image',
            field=mezzanine.core.fields.FileField(blank=True, verbose_name='Featured Image', null=True, max_length=255, upload_to='shop'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='file',
            field=mezzanine.core.fields.FileField(verbose_name='Image', max_length=255, upload_to='product'),
        ),
    ]
