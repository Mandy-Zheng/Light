import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    Ia = calculate_ambient(ambient, areflect)
    Id = calculate_diffuse(light, dreflect, normal)
    Is = calculate_specular(light, sreflect, view, normal)
    shade=[int(Ia[0]+Id[0]+Is[0]),int(Ia[1]+Id[1]+Is[1]),int(Ia[2]+Id[2]+Is[2])]

    limit_color(shade)
    return shade

def calculate_ambient(alight, areflect):
    Iambient=[alight[0]*areflect[0],alight[1]*areflect[1],alight[2]*areflect[2]]
    return Iambient

def calculate_diffuse(light, dreflect, normal):
    normalize(normal)
    normalize(light[LOCATION])
    product = dot_product(normal, light[LOCATION])
    if (product < 0):
        product = 0
    Idiffuse = [light[COLOR][0]*dreflect[0]*product,light[COLOR][1]*dreflect[1]*product,light[COLOR][2]*dreflect[2]*product]
    return Idiffuse

def calculate_specular(light, sreflect, view, normal):
    normalize(normal)
    normalize(light[LOCATION])
    product = dot_product(normal, light[LOCATION])
    if (product<0):
        product=0
    temp=[]
    Ispecular=[]
    for i in range(3):
        temp.append(2*normal[i]*product - light[LOCATION][i])
    v=normalize(view)
    t=normalize(temp)
    cosAlpha=dot_product(temp,view)
    if (cosAlpha<0):
        cosAlpha=0
    for i in range(3):
        Ispecular.append(sreflect[i] * light[COLOR][i] * math.pow(cosAlpha,SPECULAR_EXP))
    return Ispecular

def limit_color(color):
    for i in range(3):
        if (color[i]>255):
            color[i]=255

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
