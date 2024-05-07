import matplotlib
import matplotlib.pyplot as plt
from config import Config
from math import sin,cos
import math
import numpy as np

def scale_labels(x):
    return np.round(x/1000).astype(int)

class Data:
    def __init__(self,v0x,v0y) -> None:
        self.X:list[float]=[0]
        self.Y:list[float]=[0]
        self.Vx:list[float]=[v0x]
        self.Vy:list[float]=[v0y]
        self.Ax:list[float]=[0]
        self.Ay:list[float]=[0]

class Calculation:
    def __init__(self,config:Config=Config()) -> None:
        self.config=config
        self.data=Data(config.v0*cos(math.radians(config.alfa)),
                       config.v0*sin(math.radians(config.alfa)))
    def calculate(self):
        for i in range (1,int(self.config.sym_time/self.config.step)):
            self.data.Ax.append((-self.config.b/self.config.m)*self.data.Vx[i-1])
            self.data.Vx.append(self.data.Vx[i-1]+self.data.Ax[i]*self.config.step)
            self.data.X.append(self.data.X[i-1]+self.data.Vx[i]*self.config.step+self.data.Ax[i]*self.config.step*self.config.step/2)

            self.data.Ay.append((-self.config.g-(self.config.b/self.config.m)*self.data.Vy[i-1]))
            self.data.Vy.append(self.data.Vy[i-1]+self.data.Ay[i]*self.config.step)
            self.data.Y.append(self.data.Y[i-1]+self.data.Vy[i]*self.config.step+(self.data.Ay[i]*(self.config.step*self.config.step/2)))
            if self.data.Y[-1] <=0:
                break

    def calculateMaxYRange(self):
        y_max=0
        for y in self.data.Y:
            if y > y_max:
                y_max=y
        return y_max
    def calculateMaxXRange(self):
        return self.data.X[-1]
    
    def calculateFlyTime(self):
        return len(self.data.Y)*self.config.step

    def plotXY(self):
        plt.figure(figsize=(21,9))
        plt.subplot(2,3,1)
        plt.plot(self.data.Ax[1:],label="Ax",color="red")
        plt.plot(self.data.Ay[1:],label="Ay",color="blue")
        plt.xlabel("t [s] ")
        plt.ylabel(r"$A[\frac{m}{s^2}]$")
        plt.legend()
        plt.xticks(np.arange(0, len(self.data.Ay), step=2000),labels=scale_labels(np.arange(0,len(self.data.Ay),step=2000)))
        plt.grid(True)
        plt.title("Wykres przyśpieszenia od czasu")

        plt.subplot(2,3,2)
        plt.plot(self.data.X,color="red",label="X")
        plt.plot(self.data.Y,color="blue",label="Y")
        plt.xlabel("t [s]")
        plt.ylabel("odległość [m]")
        plt.xticks(np.arange(0, len(self.data.Y), step=2000),labels=scale_labels(np.arange(0,len(self.data.Y),step=2000)))
        plt.legend()
        plt.grid(True)
        plt.title("Wykres położenia od czasu")

        plt.subplot(2,3,3)
        plt.plot(self.data.Vx,label="Vx",color="red")
        plt.plot(self.data.Vy,label="Vy",color="blue")
        plt.xlabel("t [s]")
        plt.ylabel(r"V $[\frac{m}{s^2}]$")
        plt.xticks(np.arange(0, len(self.data.Vy), step=2000),labels=scale_labels(np.arange(0,len(self.data.Vy),step=2000)))
        plt.legend()
        plt.grid(True)
        plt.title("Wykres prędkości od czasu")

        bestAngle = "Unactive Alfa Calculations"

        if self.config.calc_a_for_range:
            plt.subplot(2,3,4)
            Mymap=self.CalculateAllAlfa()
            plt.plot(Mymap.keys(),Mymap.values())
            plt.xlabel(r"$\alpha [\degree]$")
            plt.ylabel(r"$range [m]$")
            plt.xticks(np.arange(0,90,step=3))
            plt.title(r"Wykres zależności zasięgu strzału od kąta $ \alpha $")
            plt.grid(True)
            bestAngRange = 0
            for alfa,rg in Mymap.items():
                if rg > bestAngRange:
                    bestAngle=alfa
                    bestAngRange = rg
            

        
        plt.subplot(2,3,5)
        plt.plot(self.data.X,self.data.Y)
        plt.xlabel("X [m]")
        plt.ylabel("Y [m]")
        plt.title("Wykres położenia Y od X")
        plt.grid(True)

        plt.subplot(2,3,6)
        plt.axis('off')
        plt.text(0.2,0.5,
                 f"Odległość strzału X: {round(self.calculateMaxXRange(),2)}, \n"+
                 f"Odległość strzału oś Y: {round(self.calculateMaxYRange(),2)}, \n"+
                 f"czas lotu: {round(self.calculateFlyTime(),2)}, \n"+
                 f"Najlepszy kąt: {bestAngle}",
                 horizontalalignment='left',
                            verticalalignment='center', fontsize=12)

        plt.tight_layout()
        plt.show()

    def CalculateAllAlfa(self)->dict[str,float]:
        my_map:dict[str,float]={}
        xyz=self.config.alfa
        for alfa in range(0,90):
            calc=Calculation()
            calc.config.alfa=alfa
            calc.calculate()
            my_map[str(alfa)]=calc.calculateMaxXRange()
        self.config.alfa=xyz
        my_map.pop("0")
        return my_map
        

if __name__ == "__main__":
    calc=Calculation()
    calc.calculate()
    print(f"X: {calc.calculateMaxXRange()}")
    print(f"Y: {calc.calculateMaxYRange()}")
    #print(f"Best alfa: {calc.findBestAlfa()}")
    calc.plotXY()
