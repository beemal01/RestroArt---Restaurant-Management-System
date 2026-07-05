from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Food
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

@receiver([post_save, post_delete], sender=Food)
def item_cache(sender, instance, **kwargs):
    try:
        cache.delete_pattern('*foodlist*')
    except Exception as e:
        logger.warning(f"Cache clear skipped (Redis not available): {e}")
