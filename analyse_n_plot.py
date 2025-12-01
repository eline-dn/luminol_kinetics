from PIL import Image # utilisation de bibliothèque PIL
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2
from scipy.signal import savgol_filter

from pylab import *

def niveau_gris(pixel):#luminosite d'un pixel
    pixel_gris=0.2125*pixel[0]+0.7154*pixel[1]+0.0721*pixel[2]
    return pixel_gris

def luminosite_moy_image(image):
    n,p=len(image),len(image[0])
    seuil=0#seuil à partir duquel on prend en compte ou non la luminosite pixel, ie le pixel est-il dans l'erlenmeyer ou non?
    luminosite_moyenne=0
    compteur=0
    for i in range(n):
        for j in range(p):
            l=niveau_gris(image[i][j])
            if l>=seuil:
                luminosite_moyenne+=l
                compteur+=1
    luminosite_moyenne=luminosite_moyenne//compteur#on obtient la moyenne de la luminosité dans le becher pour une image
    return luminosite_moyenne

def recup_images_vid():
    cap=cv2.VideoCapture("C:/Users/eline/Documents/PCSI/Chimie/tipe luminol/3mL.MOV")#rentrer le chemin d'acces entre "" avec des / et non des \
    check,vid=cap.read()
    counter=0
    check=True
    liste_images=[]
    while check==True:
        #cv2.imwrite("frame%d.jpg"%counter,vid)
        check,vid=cap.read()
        liste_images.append(vid)
        counter+=1
    liste_images.pop()
    return liste_images

def chercher_max(l):
    max=0
    indice_max=0
    n=len(l)
    for i in range(n):
        if l[i]>=max:
            max=l[i]
            indice_max=i
    return(max,indice_max)

##traitement de la video

A=recup_images_vid()#liste contenant les photos
# liste_luminosite=len(A)*[0]

def selection_carre(im): #on étudie la luminosité d'un carré de 50x50 pixels centré au milieu de la solution
    n=len(im)
    p=len(im[0])
    mZoom=50*[None]
    for i in range(50):
        mZoom[i]=50*[None]
        for j in range(50):
            mZoom[i][j]=im[i+2*n//5][j+2*p//5]
    return mZoom


m=len(A)
B=m*[None]
liste_luminosite=m*[0]
# compteur=0

for i in range(0,m): #création d'une liste conteant chaque luminosité de chaque image
    liste_luminosite[i]=luminosite_moy_image(selection_carre(A[i]))#A[i] est une image sous la forme d'un tableau de n*p pixels


max=chercher_max(liste_luminosite)[0]
indice_max=chercher_max(liste_luminosite)[1]
#acte1=indice_max*[None]
a2=len(liste_luminosite)-indice_max
#acte2=a2*[None]
# compteur1=0
acte1=[]
acte2=[]
a1bis=[]
a1ter=[]
a2bis=[]
a2ter=[]


for i in range(indice_max):
    # while luminosite[i]==0:

    if liste_luminosite[i]>0:

        acte1.append((log(liste_luminosite[i])))
        a1bis.append(1/liste_luminosite[i])
        a1ter.append(1/liste_luminosite[i]**2)


for i in range(indice_max,m):
    if liste_luminosite[i]>0:

        acte2.append(log(liste_luminosite[i]))
        a2bis.append(1/liste_luminosite[i])
        a2ter.append(1/liste_luminosite[i]**2)


acte2=np.array(acte2)
acte1=np.array(acte1)

a1bis=np.array(a1bis)
a1ter=np.array(a1ter)

a2bis=np.array(a2bis)
a2ter=np.array(a2ter)
##tracé de courbe

#liste des temps:
duree=len(A)/59.96#duree de la video en s
temps=np.linspace(0,duree,m)
temps1=np.linspace(0,len(acte1)/59.96,len(acte1))
temps2=np.linspace(0,len(acte2)/59.96,len(acte2))

p2=np.polyfit(temps2,acte2,1)
p1=np.polyfit(temps1,acte1,1)
p1bis=np.polyfit(temps1,a1bis,1)
p1ter=np.polyfit(temps1,a1ter,1)

p2bis=np.polyfit(temps2,a2bis,1)
p2ter=np.polyfit(temps2,a2ter,1)
# x=savgol_filter(liste_luminosite,70,3)
# y=savgol_filter(acte1,5,3)
# z=savgol_filter(acte2,60,3)

print("reg lin 1:",p1)
print("reg lin 2:",p2)
print("reg lin 1bis:",p1bis)
print("reg lin 1ter:",p1ter)
print("reg lin 2bis:",p2bis)
print("reg lin 2ter:",p2ter)

# plt.figure(1)           #courbe représenatnt l'intensité lumineuse en fonction du temps
# plt.subplot(1,2,1)
# plt.plot(temps,liste_luminosite,label="luminosite", color='purple')
# plt.subplot(1,2,2)
# plt.plot(temps,x,label="luminosité lissée", color='purple')

plt.figure(2)      #courbe représentant le log de la première partie et sa régression linéaire en fonction du temps
plt.subplot(2,2,1)
plt.plot(temps1,acte1,"*",label="acte1", color='green')
plt.plot(temps1,p1[0]*temps1+p1[1],label="reg lin acte1")
# plt.subplot(2,4,2)
# plt.plot(temps1,y,label="acte1 lissé", color='green')


plt.subplot(2,2,2)  #courbe représentant le log de la deuxième partie et sa régression linéaire en fonction du temps
plt.plot(temps2,acte2,label="acte2", color='pink')
plt.plot(temps2,p2[0]*temps2+p2[1],label="reg lin acte2")
# plt.subplot(2,4,4)
# plt.plot(temps2,z,label="acte2 lissé", color='pink')
plt.legend()

plt.figure(3)
plt.subplot(2,2,1)
plt.plot(temps1,a1bis,"*",label="a1bis", color='green')
plt.plot(temps1,p1bis[0]*temps1+p1bis[1],label="reg lin acte1bis")

plt.subplot(2,2,2)
plt.plot(temps1,a1ter,"*",label="a1ter", color='green')
plt.plot(temps1,p1ter[0]*temps1+p1ter[1],label="reg lin acte1ter")
plt.legend()

plt.figure(4)
plt.subplot(2,2,1)
plt.plot(temps2,a2bis,"*",label="a2bis", color='green')
plt.plot(temps2,p2bis[0]*temps2+p2bis[1],label="reg lin acte2bis")

plt.subplot(2,2,2)
plt.plot(temps2,a2ter,"*",label="a2ter", color='green')
plt.plot(temps2,p2ter[0]*temps2+p2ter[1],label="reg lin acte2ter")
plt.legend()

plt.show()
