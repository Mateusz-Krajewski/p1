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
        self.v0x=v0x
        self.x0y=v0y
        self.X=[0]
        self.Y=[0]
        self.Vx=[v0x]
        self.Vy=[v0y]
        self.Ax=[0]
        self.Ay=[0]

class Calculation:
    def __init__(self,config:Config=Config()) -> None:
        self.config=config
        self.data=Data(config.v0*cos(math.radians(config.alfa)),
                       config.v0*sin(math.radians(config.alfa)))
        
    def _generateVy(self,Vy_):
        return Vy_ - (self.config.g +self.config.b*self.config.step*Vy_/self.config.m)*self.config.step
    def _generateVx(self,Vx_):
        return Vx_ - ((self.config.b*self.config.step)*Vx_/self.config.m)*self.config.step

    def _generateAx(self,Vx_):
        return -(self.config.b*Vx_/self.config.m)
    def _generateAy(self,Vy_):
        return -(self.config.g+self.config.b*Vy_/self.config.m)

    def _generateX(self,Ax_,Vx_,X_):
        return X_+Vx_*self.config.step+Ax_*self.config.step*self.config.step
    def _generateY(self,Ay_,Vy_,Y_):
        return Y_+Vy_*self.config.step+Ay_*self.config.step*self.config.step
    
    def calculateXY(self):
        for i in range(0,int(self.config.sym_time/self.config.step)):
            self.data.Ay.append(self._generateAy(self.data.Vy[i]))
            self.data.Ax.append(self._generateAx(self.data.Vx[i]))
            x_=self._generateX(self.data.Ax[i],self.data.Vx[i],self.data.X[i])
            y_=self._generateY(self.data.Ay[i],self.data.Vy[i],self.data.Y[i])
            if y_ <= 0:
                break
            self.data.Y.append(y_)
            self.data.X.append(x_)
            self.data.Vy.append(self._generateVy(self.data.Vy[i]))
            self.data.Vx.append(self._generateVx(self.data.Vx[i]))

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
        """
        plt.subplot(2,3,1)
        plt.plot(self.data.Ax,label="Ax",color="red")
        plt.plot(self.data.Ay,label="Ay",color="blue")
        plt.xlabel("t [s] ")
        plt.ylabel(r"$A[\frac{m}{s^2}]$")
        plt.legend()
        plt.xticks(np.arange(0, len(self.data.Ay), step=2000),labels=scale_labels(np.arange(0,len(self.data.Ay),step=2000)))
        plt.grid(True)
        plt.title("Wykres przyśpieszenia od czasu")
        """

        plt.subplot(2,3,1)
        plt.plot(self.data.X,color="red",label="X")
        plt.plot(self.data.Y,color="blue",label="Y")
        plt.xlabel("t [s]")
        plt.ylabel("odległość [m]")
        plt.xticks(np.arange(0, len(self.data.Y), step=2000),labels=scale_labels(np.arange(0,len(self.data.Y),step=2000)))
        plt.legend()
        plt.grid(True)
        plt.title("Wykres położenia od czasu")

        plt.subplot(2,3,2)
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
            

        
        plt.subplot(2,3,3)
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

    def CalculateAllAlfa(self):
        map:dict={}
        xyz=self.config.alfa
        for alfa in range(0,90):
            calc=Calculation()
            calc.config.alfa=alfa
            calc.calculateXY()
            map[str(alfa)]=calc.calculateMaxXRange()
        self.config.alfa=xyz
        map.pop("0")
        return map
        

if __name__ == "__main__":
    calc=Calculation()
    calc.calculateXY()
    print(f"X: {calc.calculateMaxXRange()}")
    print(f"Y: {calc.calculateMaxYRange()}")
    #print(f"Best alfa: {calc.findBestAlfa()}")
    calc.plotXY()
