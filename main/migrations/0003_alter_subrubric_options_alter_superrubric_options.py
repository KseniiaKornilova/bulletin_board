# Generated by Django 4.1.3 on 2023-02-17 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rubric_subrubric_superrubric_rubric_super_rubric'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subrubric',
            options={'ordering': ('super_rubric__order', 'super_rubric__name', 'order', 'name'), 'verbose_name': 'Подрубрику', 'verbose_name_plural': 'Подрубрики'},
        ),
        migrations.AlterModelOptions(
            name='superrubric',
            options={'ordering': ('order', 'name'), 'verbose_name': 'Надрубрику', 'verbose_name_plural': 'Надрубрики'},
        ),
    ]
