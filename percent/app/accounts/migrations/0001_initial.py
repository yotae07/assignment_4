# Generated by Django 3.2.9 on 2021-11-11 09:36

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
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=32, unique=True)),
                ('price', models.PositiveBigIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccountHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('deposit', '입금'), ('withdraw', '출금')], max_length=10)),
                ('transaction_date', models.DateTimeField()),
                ('amount', models.PositiveBigIntegerField()),
                ('etc', models.CharField(max_length=1000)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.account')),
            ],
        ),
    ]
