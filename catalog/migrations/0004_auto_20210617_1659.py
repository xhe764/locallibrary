# Generated by Django 3.1.3 on 2021-06-17 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210616_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['book'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]
