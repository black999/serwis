# Generated by Django 2.2 on 2019-05-20 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kasa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr_unikatowy', models.CharField(max_length=12)),
                ('nr_fabryczny', models.CharField(max_length=12)),
                ('data_fisk', models.DateField()),
                ('ostatni_przeg', models.DateField()),
                ('cykl_przeg', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Podatnik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=30)),
                ('nazwa_cd', models.CharField(max_length=30)),
                ('kod_pocztowy', models.CharField(max_length=6)),
                ('miasto', models.CharField(max_length=25)),
                ('ulica', models.CharField(max_length=25)),
                ('nr_domu', models.CharField(max_length=6)),
                ('nip', models.CharField(max_length=10)),
                ('wojewodzctwo', models.CharField(max_length=15)),
                ('gmina', models.CharField(max_length=15)),
                ('poczta', models.CharField(max_length=25)),
                ('telefon', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Producent_kasy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=25)),
                ('ulica', models.CharField(max_length=25)),
                ('nr_domu', models.CharField(max_length=6)),
                ('kod_pocztowy', models.CharField(max_length=6)),
                ('miasto', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name_plural': 'Producenci kas',
            },
        ),
        migrations.CreateModel(
            name='Serwisant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwisko', models.CharField(max_length=15)),
                ('imie', models.CharField(max_length=15)),
                ('nr_plomby', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Serwisanci',
            },
        ),
        migrations.CreateModel(
            name='Urzad_skarbowy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=25)),
                ('ulica', models.CharField(max_length=25)),
                ('nr_domu', models.CharField(max_length=6)),
                ('kod_pocztowy', models.CharField(max_length=6)),
                ('miasto', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name_plural': 'Urzędy Skarbowe',
            },
        ),
        migrations.CreateModel(
            name='Przeglad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('kasa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kasy.Kasa')),
                ('serwisant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kasy.Serwisant')),
            ],
        ),
        migrations.CreateModel(
            name='Model_kasy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=20)),
                ('producent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kasy.Producent_kasy')),
            ],
            options={
                'verbose_name_plural': 'Modele kas',
            },
        ),
        migrations.AddField(
            model_name='kasa',
            name='model_kasy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kasy.Model_kasy'),
        ),
        migrations.AddField(
            model_name='kasa',
            name='podatnik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kasy.Podatnik'),
        ),
        migrations.AddField(
            model_name='kasa',
            name='urzad_skarbowy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kasy.Urzad_skarbowy'),
        ),
    ]