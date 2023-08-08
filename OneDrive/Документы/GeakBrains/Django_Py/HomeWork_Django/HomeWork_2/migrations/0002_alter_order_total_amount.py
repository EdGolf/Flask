from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]