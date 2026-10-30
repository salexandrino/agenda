from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20261025_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='data_criacao',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
