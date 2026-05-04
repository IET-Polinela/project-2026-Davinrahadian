# Generated for Lab Session 7 dashboard data.

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='category',
            field=models.CharField(
                choices=[
                    ('Jalan Rusak', 'Jalan Rusak'),
                    ('Sampah', 'Sampah'),
                    ('Lampu Mati', 'Lampu Mati'),
                    ('Drainase', 'Drainase'),
                    ('Keamanan', 'Keamanan'),
                ],
                default='Jalan Rusak',
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name='report',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='report',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-created_at']},
        ),
    ]
