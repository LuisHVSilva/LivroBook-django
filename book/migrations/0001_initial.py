# Generated by Django 4.2.2 on 2023-06-29 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookRegisterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('edition', models.CharField(blank=True, max_length=50, null=True, verbose_name='Edição')),
                ('npages', models.IntegerField(blank=True, null=True, verbose_name='Número de páginas')),
                ('begin', models.DateField(blank=True, null=True, verbose_name='Início')),
                ('finish', models.DateField(blank=True, null=True, verbose_name='Fim')),
                ('concluded', models.BooleanField(blank=True, default=False, null=True, verbose_name='Terminado?')),
                ('wish', models.BooleanField(blank=True, default=False, null=True, verbose_name='Desejo')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
    ]
