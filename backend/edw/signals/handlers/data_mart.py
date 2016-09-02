# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db.models import F
from django.db.models.signals import (
    pre_delete,
    m2m_changed
)
from django.dispatch import receiver

from edw.signals import make_dispatch_uid
from edw.signals.mptt import (
    move_to_done,
    pre_save,
    post_save
)

from edw.models.data_mart import DataMartModel


def get_children_keys(sender, parent_id):
    key = ":".join([
        sender._meta.object_name.lower(),
        sender.CHILDREN_CACHE_KEY_PATTERN.format(parent_id=parent_id)
        if parent_id is not None else
        "toplevel"
    ])
    return [key, ":".join([key, "active"])]


#==============================================================================
# DataMart model event handlers
#==============================================================================
"""
Model = DataMartModel.terms.through
@receiver(m2m_changed, sender=Model, dispatch_uid=make_dispatch_uid(
    m2m_changed, 'invalidate_after_terms_set_changed', Model))
def invalidate_after_terms_set_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    '''
    Automatically normalize terms set
    '''
    print "M2M_CHANGED!!!", instance, action, pk_set
    # pre_remove
    # post_remove
    # pre_add
    # post_add

    if action == 'post_add':
        if not hasattr(instance, '_during_terms_validation'):
            # normalize terms set
            instance.validate_terms(pk_set)
            # clear cache
            keys = [instance.ALL_ACTIVE_TERMS_COUNT_CACHE_KEY, instance.ALL_ACTIVE_TERMS_IDS_CACHE_KEY]
            cache.delete_many(keys)
"""

"""
# Excample...
@receiver(m2m_changed, sender=Video.category.through)
def video_category_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    pk_set = kwargs.pop('pk_set', None)
    action = kwargs.pop('action', None)
    if action == "pre_add":
        if 1 not in pk_set:
            c = Category.objects.get(pk=1)
            instance.category.add(c)
            instance.save()
"""


def invalidate_data_mart_before_save(sender, instance, **kwargs):
    if instance.id is not None:
        try:
            original = sender._default_manager.get(pk=instance.id)
            if original.parent_id != instance.parent_id:
                if original.active != instance.active:
                    DataMartModel.clear_children_buffer()  # Clear children buffer
                    instance._parent_id_validate = True
                else:
                    keys = get_children_keys(sender, original.parent_id)
                    cache.delete_many(keys)
            else:
                if original.active != instance.active:
                    if instance.active:
                        parent_id_list = list(original.get_family().
                                              exclude(lft=F('rght')-1).values_list('id', flat=True))
                        parent_id_list.append(None)
                    else:
                        parent_id_list = list(original.get_descendants(include_self=True).
                                              exclude(lft=F('rght')-1).values_list('id', flat=True))
                        parent_id_list.append(original.parent_id)
                    keys = []
                    for parent_id in parent_id_list:
                        keys.extend(get_children_keys(sender, parent_id))
                    cache.delete_many(keys)
                    instance._parent_id_validate = True
        except sender.DoesNotExist:
            pass


def invalidate_data_mart_after_save(sender, instance, **kwargs):
    if instance.id is not None and not getattr(instance, '_parent_id_validate', False) :
        keys = get_children_keys(sender, instance.parent_id)
        cache.delete_many(keys)


def invalidate_data_mart_before_delete(sender, instance, **kwargs):
    invalidate_data_mart_after_save(sender, instance, **kwargs)


def invalidate_data_mart_after_move(sender, instance, target, position, prev_parent, **kwargs):
    keys = get_children_keys(sender, prev_parent.id if prev_parent is not None else None)
    cache.delete_many(keys)

    invalidate_data_mart_after_save(sender, instance, **kwargs)


Model = DataMartModel.materialized
for clazz in [Model] + Model.__subclasses__():
    pre_save.connect(invalidate_data_mart_before_save, sender=clazz,
                     dispatch_uid=make_dispatch_uid(
                         pre_save,
                         invalidate_data_mart_before_save,
                         clazz
                     ))
    post_save.connect(invalidate_data_mart_after_save, sender=clazz,
                      dispatch_uid=make_dispatch_uid(
                          post_save,
                          invalidate_data_mart_after_save,
                          clazz
                      ))
    pre_delete.connect(invalidate_data_mart_before_delete, sender=clazz,
                       dispatch_uid=make_dispatch_uid(
                           pre_delete,
                           invalidate_data_mart_before_delete,
                           clazz
                       ))
    move_to_done.connect(invalidate_data_mart_after_move, sender=clazz,
                         dispatch_uid=make_dispatch_uid(
                             move_to_done,
                             invalidate_data_mart_after_move,
                             clazz
                         ))