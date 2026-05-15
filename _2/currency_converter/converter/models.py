from django.db import models

class Currency(models.Model):
    currency_code = models.CharField(max_length=3) # e.g., USD
    exchange_rate = models.FloatField() # Rate to EUR
    
    def __str__(self):
        return self.currency_code