from os.path import isfile

from django.db import models
from datetime import date, time, datetime

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=36)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    secret_key = models.CharField(max_length=24)
    limit_time = datetime.strptime('05:00:00', '%X').time()
    self_sign = models.CharField(max_length=15,
                                 verbose_name="¿De que modo podemos identificar las lineas que generaste?")


class Time(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    start = models.DateTimeField(verbose_name="Inicio")
    end = models.DateTimeField(verbose_name="Fin")
    delta = models.DateTimeField(verbose_name="Tiempo real")
    finished = models.BooleanField(verbose_name="Terminado")
    date = models.DateField(verbose_name="Fecha de trabajo")

    def checkTiming(self):
        limit = self.user.limit_time
        if self.delta > limit:
            self.finished = True
            return "Has excedido el tiempo limite de tus 5 horas"


class File(models.Model):
    creator = models.ForeignKey(User, models.CASCADE, null=True)
    file = models.FilePathField(verbose_name="Archivo sobre el cual trabajaste")


class LocCounter(models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=True)
    file = models.ForeignKey(File, models.CASCADE, null=True)
    loc_created = models.IntegerField("Lineas creadas")
    functions_created = models.IntegerField("Funciones creadas")
    objects_created = models.IntegerField("Objetos creados")
    doc_lines = models.IntegerField("Lineas de documentación generadas")
    loc_modified = models.IntegerField("Lineas cambiadas")

    def countLines(self):
        if isfile(self.file):
            with open(self.file,'r') as reader:
                source = reader.readlines()
                for i in range(0, len(source)):
                    line = source[i]
                    if line.lstrip(' ').startswith('#'):
                        ++self.doc_lines

                    if line.lstrip(' ').__contains__(self.user.self_sign) and line.lstrip(' ').__contains__('#N'):
                        ++self.loc_created

                    if line.lstrip(' ').__contains__(self.user.self_sign) and line.lstrip(' ').__contains__('#M'):
                        ++self.loc_modified

                    if line.lstrip(' ').__contains__(self.user.self_sign) and line.lstrip(' ').startswith('def'):
                        ++self.functions_created

                    if line.lstrip(' ').__contains__(self.user.self_sign) and line.lstrip(' ').startswith('class'):
                        ++self.objects_created





