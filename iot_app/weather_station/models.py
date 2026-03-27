from django.db import models

# Create your models here.

class Sensor(models.Model):
    TIPO_CHOICES = [
        ('temp', 'Temperatura'),
        ('hum', 'Humedad'),
        ('luz', 'Luz'),
        ('mov', 'Movimiento'),
    ]
    name = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    pin = models.IntegerField(help_text="Pin GPIO donde está conectado")
    ubicacion = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_tipo_display()})"

class Lectura(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    valor = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.name} - {self.valor} at {self.fecha}"