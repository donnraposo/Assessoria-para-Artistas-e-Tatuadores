import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("guests", "0001_initial"),
        ("studios", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studiobookingrequest",
            name="guest_id",
        ),
        migrations.AddField(
            model_name="studiobookingrequest",
            name="guest",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="studio_booking_requests",
                to="guests.guest",
            ),
        ),
    ]
