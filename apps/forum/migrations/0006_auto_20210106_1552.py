# Generated by Django 3.1.4 on 2021-01-06 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_forum_invite_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='invite_link',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Invite link'),
        ),
    ]