import time
from scipy.integrate import odeint
import gurobipy as gp
from gurobipy import GRB
from gurobipy import *
import altair as alt
import math


#Cost parameters
Cf=0.011 
# cost of mining
C1= 4.97
#C1 - hydrometallurgy production cost ($/kg)
C2=3.44
#C2 - pyrometallurgy production cost ($/kg)
Cm= 0.025
#Cm-cost of manufacuring ($/kg)
Ct1= 5.55
#Ct1 - copper transportation by EV truck cost ($/kg)
Ct2= 3.3
#Ct2 - copper transportation by diesel truck cost ($/kg)
CR1=3
#CR1- recycling of end-use to production cost ($/kg)
CR2=1.5
#CR2- recycling of end-use to manufacturing cost ($/kg)


# Emission factors 
EMf= 2.4
#EMf - emission factor of mining (kg CO2-eq/kg)
EM1=3.25
#EM1 - emission factor of hydrometallurgy production (kg CO2-eq/kg)
EM2=5.24
#EM2 - emission factor of pyrometallurgy production (kg CO2-eq/kg)

EMm= 0.0013
# EMm - emission factor of manufacturing (kg CO2-eq/kg)
EMt1= 0.025
#EMt1 - emission factor of copper transportation by EV truck (kg CO2-eq/kg)
EMt2= 0.019
#EMt2 - emission factor of copper transportation by diesel truck (kg CO2-eq/kg)
EMR1=0.8
#EMR1- emission factor of recycling of end-use to production (kg CO2-eq/kg)
EMR2=0.4
#EMR2- emission factor of recycling of end-use to manufacturing (kg CO2-eq/kg)


# Demand and production parameters
D=1.8*1000000000 
#D is the minimum demand (kg)
P=1.3*1000000000 
#P is the minimum production (kg)

# weight factor 
α=0.5
# α is the weight factor for the objective function 

# Create a new model 
#P is the minimum production (t)
m = gp.Model()





# Create variables
# f - production volume from mining (t); X1 - hydrometallurgy production (t); X2 - pyrometallurgy
#production (t);
#Y1 - copper transportation by EV truck (t); Y2 - copper transportation by diesel truck (t); R1-
#recycling rate of end-use to production (%)
#R2- recycling rate of end-use to manufacturing (%)
#create variables 
f  = m.addVar(name="f")
X1 = m.addVar(name="X1")
X2 = m.addVar(name="X2")
Y1 = m.addVar(name="Y1")
Y2 = m.addVar(name="Y2")
R1 = m.addVar( name="R1")
R2 = m.addVar( name="R2")


# OPTIGUIDE CONSTRAINT CODE GOES HERE
# Add constraints
m.addConstr (f == X1+X2)
m.addConstr (Y1+Y2 == X1+X2+(Y1+Y2)*(R1+R2))
m.addConstr ((Y1+Y2)*(R1+R2) >=f )
m.addConstr (f>=P)
m.addConstr (Y1+Y2>=D)
m.addConstr (R1<=0.5)
m.addConstr (R2<=0.5)




# weight factor
# Optimize model
cost= f*Cf + X1*C1+ X2*C2+ (X1+X2)*Cm + Y1*Ct1+ Y2*Ct2 +(Y1+Y2)*R1*CR1+(Y1+Y2)*R2*CR2
# minimze cost 
emissisons= f*EMf + X1*EM1+ X2*EM2+ (X1+X2)*EMm + Y1*EMt1 + Y2*EMt2 + (Y1+Y2)*R1*EMR1 + (Y1+Y2) *R2*EMR2
# minimze emissions

# Set objective
m.setObjective( α*(f*Cf + X1*C1+ X2*C2+ (X1+X2)*Cm + Y1*Ct1+ Y2*Ct2 +(Y1+Y2)*R1*CR1+(Y1+Y2)*R2*CR2)+(1-α)*(f*EMf + X1*EM1+ X2*EM2+ (X1+X2)*EMm + Y1*EMt1 + Y2*EMt2 + (Y1+Y2)*R1*EMR1 + (Y1+Y2) *R2*EMR2), gp.GRB.MINIMIZE)

cost=cost.getValue()
emissions= emissisons.getValue()

#Optimize model 

m.optimize()

# OPTIGUIDE DATA CODE GOES HERE
# Solve
m.setParam('NonConvex', 2)
m.update()
m.optimize()



