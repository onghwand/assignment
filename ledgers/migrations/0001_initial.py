# Generated by Django 3.2.12 on 2023-01-05 19:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memo', models.CharField(max_length=256, null=True)),
                ('cashflow', models.IntegerField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('day', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)])),
                ('original_url', models.CharField(max_length=256, null=True)),
                ('shorten_url', models.CharField(max_length=256, null=True)),
                ('expiration_time', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledgers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
