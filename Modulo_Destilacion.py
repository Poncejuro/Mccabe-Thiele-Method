import xlrd
import numpy as np
import matplotlib.pyplot as plt
from numpy import polyfit
import sys
import pandas as pd


#funciones multiuso
def curva(archivo,hoja):
    libro = xlrd.open_workbook(archivo)
    sheet = libro.sheet_by_name(hoja)
    nf = np.array(sheet.nrows)
    x = []
    y = []
    for i in range(nf):
        x.append(sheet.cell_value(i,0))
        y.append(sheet.cell_value(i,1))
        z = [0,1]
    return x,y,z
    
def pendiente_estado(f):    
    if f == 1:
        m=0
    elif f == 0:
        m=1000
    else:
        m=-(1-f)/f
    return m
          
def pendientes(x1,x2,y1,y2):    
    m=(y2-y1)/(x2-x1)
    return m
    
def intersecciones(x1,y1,m1,x2,y2,m2):
    x=((y1-y2)-(m1*x1-m2*x2))/(m2-m1)
    y=m1*(x-x1)+y1
    return x, y
    
def platos(Pendiente,Xrecta,Yrecta,Yiterada,x,y,Px,Py):
    m=Pendiente
    xi=Xrecta
    yii=Yrecta
    yStart=Yiterada
    polinomio=np.array(polyfit(y,x,4))
    xp = polinomio[0]*yStart**4 + polinomio[1]*yStart**3 + polinomio[2]*yStart**2 + polinomio[3]*yStart + polinomio[4]
    yp = yii + m*(xp-xi)    
    Px.append(xp)
    Py.append(yStart)
    Px.append(xp)
    Py.append(yp)     
    return Px,Py
    
def zonas(yDOWN,yUP,m,Xrecta,Yrecta,x,y,Px,Py):      
    while yDOWN < yUP:
        w=platos(m,Xrecta,Yrecta,yUP,x,y,Px,Py)
        w=np.array(w)
        aux=w[1]
        if np.size(aux) <100:
            aux1=aux[np.size(aux)-1]
            yUP=aux1
        else:
            print("el estado termodinámico no es posible")
            sys.exit()
            break
    return w
  
#instrucciones para el tipo del problema
def c1a(D,B,F,R,f):
    #Cruva de equilibrio
    by=D/(R+1)
    vareq=curva("Datos.xlsx","Equilibrio")  
    x=vareq[0]
    y=vareq[1]
    z=vareq[2]
    #putos para la interseccion D-F
    md=pendientes(D,0,D,by)
    mf=pendiente_estado(f)
    h=np.array(intersecciones(D,D,md,F,F,mf)) 
    #vectores del estado termodinámico y la línea de operación
    xr=[B,h[0],D]
    yr=[B,h[1],D]
    cx=[h[0], F]
    cy=[h[1], F]
    #ultima zona
    mb=pendientes(B,h[0],B,h[1])
    #inicialización de los vectores paralos puntos de los platos
    Px = [D]
    Py = [D]
    #zona del prpimer plateado
    w=zonas(h[1],D,md,D,D,x,y,Px,Py)
    #eliminación del último pláto
    Px=w[0]
    Py=w[1]  
    Px=Px.tolist()
    Py=Py.tolist()
    Px.pop()
    Py.pop()
    Px.pop()
    Py.pop()
    #zona del segundo plateado
    w=zonas(B,Py[-1],mb,h[0],h[1],x,y,Px,Py)
    #numero de platos
    Np=round((np.size(Px)-1)/2)
    plt.plot(x,y,z,z,xr,yr,cx,cy,Px,Py)
    plt.show()
    #exportando datos   
    Dx=Px
    Dy=Py
    Dx.append(xr)
    Dy.append(yr)
    Dx.append(cx)
    Dy.append(cy)
    Data_Frame = {'x': Dx,
                   'y': Dy}
    df = pd.DataFrame(Data_Frame, columns = ['x','y'])
    df.to_excel ("Resultados.xlsx")
    return Np

def c2a(D,B,F,R,f,f2,F2,m1,m2,m3):
    #Cruva de equilibrio
    by=D/(R+1)
    vareq=curva("Datos.xlsx","Equilibrio")  
    x=vareq[0]
    y=vareq[1]
    z=vareq[2]
    #putos para la interseccion D-intermedio
    mf=pendiente_estado(f)
    md=pendientes(D,0,D,by)
    h=np.array(intersecciones(D,D,md,F,F,mf)) 
    #putos para la interseccion intermedia
    mf2=pendiente_estado(f2)
    h2=np.array(intersecciones(B,B,m3,F2,F2,mf2)) 
    #vectores del estado termodinámico y la línea de operación    
    xr=[B,h2[0],h[0],D]
    yr=[B,h2[1],h[1],D]
    cx=[h[0], F]
    cy=[h[1], F]
    cx2=[h2[0], F2]
    cy2=[h2[1], F2]
    #inicialización de los vectores paralos puntos de los platos
    Px = [D]
    Py = [D]
    #zona del prpimer plateado
    w=zonas(h[1],D,md,D,D,x,y,Px,Py)
    #eliminación del último pláto
    Px=w[0]
    Py=w[1]  
    Px=Px.tolist()
    Py=Py.tolist()
    Px.pop()
    Py.pop()
    Px.pop()
    Py.pop()
    #zona del segundo plateado
    w=zonas(h2[1],Py[-1],m2,h[0],h[1],x,y,Px,Py)
    #eliminación del último pláto
    Px=w[0]
    Py=w[1]  
    Px=Px.tolist()
    Py=Py.tolist()
    Px.pop()
    Py.pop()
    Px.pop()
    Py.pop()
    #zona del tercer plateado
    w=zonas(B,Py[-1],m3,h2[0],h2[1],x,y,Px,Py)
    #numero de platos
    Np=round((np.size(Px)-1)/2)
    #armado de la gráfica
    plt.plot(x,y,z,z,xr,yr,cx,cy,cx2,cy2,Px,Py)
    plt.show()
    #exportando datos
    Dx=Px
    Dy=Py
    Dx.append(xr)
    Dy.append(yr)
    Dx.append(cx)
    Dy.append(cy)
    Dx.append(cx2)
    Dy.append(cy2)
    Data_Frame = {'x': Dx,
                   'y': Dy}
    df = pd.DataFrame(Data_Frame, columns = ['x','y'])
    df.to_excel ("Resultados.xlsx")
    return Np

