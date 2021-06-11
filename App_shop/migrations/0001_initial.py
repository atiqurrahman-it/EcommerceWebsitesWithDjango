# Generated by Django 3.2.3 on 2021-05-30 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_product_img', models.ImageField(upload_to='Products')),
                ('name', models.CharField(max_length=250)),
                ('sort_discription', models.CharField(max_length=265, verbose_name='sort_discription')),
                ('details_Discription', models.TextField(verbose_name='details_Discription')),
                ('price', models.FloatField()),
                ('old_price', models.FloatField(default=0.0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='App_shop.category')),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
    ]
