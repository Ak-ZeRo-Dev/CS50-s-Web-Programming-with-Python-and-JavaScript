# Generated by Django 5.0.6 on 2024-07-15 06:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_bid_listing_alter_bid_user_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bids',
            field=models.ManyToManyField(related_name='bidders', through='auctions.Bid', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='user',
            name='comments',
            field=models.ManyToManyField(related_name='commenters', through='auctions.Comment', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_bids', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_comments', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings_category', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
