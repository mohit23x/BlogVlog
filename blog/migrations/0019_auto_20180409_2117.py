# Generated by Django 2.0.3 on 2018-04-09 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20180409_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='usrimg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.UserImage'),
        ),
        migrations.AddField(
            model_name='commentreply',
            name='usrimg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.UserImage'),
        ),
    ]
