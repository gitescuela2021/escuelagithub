class curso:
    def __init__(self,titulo,descripcion,precio):
        self.titulo = titulo
        self.descripcion = descripcion
        self.precio = precio

    def NombrePrecio(self):
        print('Este curso se llama ' + self.titulo + ' y tu aprendes ' + self.descripcion + ' y tiene el precio' + str(self.precio))

    def Descuento(self,porcentaje):
        self.precio -= self.precio * porcentaje /100

    def __str__(self):
        return self.titulo

curso_enero = curso('rosas','cultivo de rosas',12.34)      
# curso_enero.Descuento(10)

print(curso_enero)

def construye(tipo_volante, potencia, electrico, *aditamentos):
    print(aditamentos)

construye('ajustable','500','Si', 'azul', 'dos puertas','cuero','automatico')

def direccion(pais, ciudad, **info):
    info['pais'] = pais 
    info['ciudad'] = ciudad 
    return info

print(direccion('Argentina','Buenos Aires', calle='Defensa 123', edificacion='Edificio'))
