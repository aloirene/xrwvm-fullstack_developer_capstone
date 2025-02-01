from django.db import models

# Car Make Model
class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)  # Optional: Country of origin
    founded_year = models.PositiveIntegerField(blank=True, null=True)  # Optional: Year founded

    def __str__(self):
        return f"{self.name} ({self.founded_year if self.founded_year else 'Unknown Year'})"

# Car Model
class CarModel(models.Model):
    # Choices for car type
    CAR_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
        ('Coupe', 'Coupe'),
        ('Hatchback', 'Hatchback'),
        ('Convertible', 'Convertible'),
        ('Pickup', 'Pickup'),
        ('Van', 'Van'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")  # Renamed to match populate.py
    dealer_id = models.IntegerField(default=1)  # ✅ Added default value to avoid NULL errors
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)  # Use 'type' instead of 'car_type' to match populate.py
    year = models.PositiveIntegerField()  # Store only the year as an integer
    horsepower = models.PositiveIntegerField(blank=True, null=True)  # Optional: Engine power
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional: Price in USD

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"

    class Meta:
        ordering = ["-year"]  # Order by most recent model year