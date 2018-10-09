# Generated by Django 2.1.2 on 2018-10-08 04:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('castpage', '0005_auto_20181004_2143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('venue', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('cast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='castpage.Cast')),
            ],
            options={
                'ordering': ['date', 'start_time'],
            },
        ),
    ]