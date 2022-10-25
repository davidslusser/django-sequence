from telnetlib import SE
from django.db import models
from django_sequence.fields import SequenceField


class Product(models.Model):
    sku = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku


class Order(models.Model):   
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sequence = SequenceField()

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f'OR-{self.id}'

    def add_stages(self):
        stage_list = [
            {'name': 'my_stage_one', 'description': 'description of the first stage', },
            {'name': 'my_stage_two', 'description': 'description of the second stage', },
            {'name': 'my_stage_three', 'description': 'description of the third stage', },
        ]
        self.sequence.add_stages(stage_list)
