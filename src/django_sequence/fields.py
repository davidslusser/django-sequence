from django.db import models
from django.db.utils import OperationalError
from django_sequence.models import Sequence


def get_sequence_object():
    try:
        return Sequence.objects.create()
    except OperationalError:
        return None



class SequenceField(models.ForeignKey):
    description = 'A field to track the Sequence of a given object entry'

    def __init__(self, **kwargs):
        kwargs['to'] = 'django_sequences.Sequence'
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['on_delete'] = models.CASCADE
        kwargs['default'] = get_sequence_object
        super(SequenceField, self).__init__(**kwargs)

