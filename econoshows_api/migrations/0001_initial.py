# Generated by Django 3.1.7 on 2021-03-18 23:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(max_length=20)),
                ('band_name', models.CharField(max_length=50)),
                ('lineup', models.CharField(max_length=20)),
                ('links', models.CharField(max_length=200)),
                ('photos', models.ImageField(null=True, upload_to='bands')),
                ('bio', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('door_time', models.TimeField()),
                ('show_time', models.TimeField()),
                ('cover', models.CharField(max_length=20)),
                ('date', models.DateField(default='0000-00-00')),
                ('is_all_ages', models.BooleanField(default=False)),
                ('poster', models.ImageField(null=True, upload_to='show_posters')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(max_length=10)),
                ('venue_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('booking_info', models.CharField(max_length=50)),
                ('description', models.CharField(default='', max_length=500)),
                ('is_all_ages', models.BooleanField(default=False)),
                ('has_backline', models.BooleanField(default=False)),
                ('website', models.CharField(default='', max_length=150)),
                ('photos', models.ImageField(null=True, upload_to='venues')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShowVenue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venue', to='econoshows_api.show')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shows', to='econoshows_api.venue')),
            ],
        ),
        migrations.CreateModel(
            name='ShowBand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shows', to='econoshows_api.band')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bands', to='econoshows_api.show')),
            ],
        ),
        migrations.AddField(
            model_name='band',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bands', to='econoshows_api.genre'),
        ),
        migrations.AddField(
            model_name='band',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
