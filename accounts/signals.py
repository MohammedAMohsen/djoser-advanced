from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import User


@receiver(pre_save, sender=User)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    """
    Delete the previous avatar file when the user uploads a new one.
    """
    # User is being created for the first time
    if not instance.pk:
        return
    try:
        old_user = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return
    old_avatar = old_user.avatar
    new_avatar = instance.avatar
    if (
        old_avatar
        and old_avatar != new_avatar
        and old_avatar.storage.exists(old_avatar.name)
    ):
        old_avatar.delete(save=False)


@receiver(post_delete, sender=User)
def delete_avatar_on_user_delete(sender, instance, **kwargs):
    """
    Delete avatar file after deleting the user.
    """
    if (
        instance.avatar
        and instance.avatar.storage.exists(instance.avatar.name)
    ):
        instance.avatar.delete(save=False)