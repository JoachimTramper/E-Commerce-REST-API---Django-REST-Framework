# users/migrations/0003_drop_address_unique.py
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_address_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set(),  
        ),
    ]



