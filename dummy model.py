import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gurobipy import *
import altair as alt
import math


#Cost parameters
Cf=1
# cost of mining
C1=2
#C1 - hydrometallurgy production cost ($/t)
C2=3
#C2 - pyrometallurgy production cost ($/t)
Cm=6
#Cm-cost of manufacuring ($/t)
Ct1=4
#Ct1 - copper transportation by EV truck cost ($/t)
Ct2=5
#Ct2 - copper transportation by diesel truck cost ($/t)
CR1=6
#CR1- recycling of end-use to production cost ($/t)
CR2=7
#CR2- recycling of end-use to manufacturing cost ($/t)
# Emission factors 
EMf=4
#EMf - emission factor of mining (t CO2-eq/t)
EM1=2
#EM1 - emission factor of hydrometallurgy production (t CO2-eq/t)
EM2=3
#EM2 - emission factor of pyrometallurgy production (t CO2-eq/t)

EMf= 8
# EMf - emission factor of manufacturing (t CO2-eq/t)
EMt1=4
#EMt1 - emission factor of copper transportation by EV truck (t CO2-eq/t)
EMt2=5
#EMt2 - emission factor of copper transportation by diesel truck (t CO2-eq/t)
EMR1=4
#EMR1- emission factor of recycling of end-use to production (t CO2-eq/t)
EMR2=3
#EMR2- emission factor of recycling of end-use to manufacturing (t CO2-eq/t)

# Energy consumption factor
Ef=8
#Ef - energy consumption of mining (kwh/t)
E1=4
#E1 - energy consumption of hydrometallurgy production cost (kwh/t)
E2=4
#E2 - energy consumption of pyrometallurgy production cost (kwh/t)
Em=9
#Em - energy consumption of manufacturing (kwh/t)
Et1=5
#Et1 - energy consumption of copper transportation by EV truck cost (kwh/t)
Et2 =7
#Et2 - energy consumption of copper transportation by diesel truck cost (kwh/t)
ER1=8
#ER1- energy consumption of recycling of end-use to production cost (kwh/t)
ER2=9
#ER2- energy consumption of recycling of end-use to manufacturing cost (kwh/t)

# Demand and production parameters
D=400
#D is the minimum demand (t)
P=350

#P is the minimum production (t)
m = gp.Model()

# Add decision varibles
# f - production volume from mining (t); X1 - hydrometallurgy production (t); X2 - pyrometallurgy
#production (t);
#Y1 - copper transportation by EV truck (t); Y2 - copper transportation by diesel truck (t); R1-
#recycling rate of end-use to production (%)
#R2- recycling rate of end-use to manufacturing (%)

f = m.addVar(name="f")
X1 = m.addVar(name="X1")
X2 = m.addVar(name="X2")
Y1 = m.addVar(name="Y1")
Y2 = m.addVar(name="Y2")
R1 = m.addVar( name="R1")
R2 = m.addVar( name="R2")

# Add constraints
m.addConstr (f == X1+X2)
m.addConstr (Y1+Y2 == X1+X2+(Y1+Y2)*(R1+R2))
m.addConstr ((Y1+Y2)*(R1+R2) >=f )
m.addConstr (f>=P)
m.addConstr (Y1+Y2>=D)
m.addConstr (R1<=0.5)
m.addConstr (R2<=0.5)

#Objective function
m.setObjective(f*Cf + X1*C1+ X2*C2+ (X1+X2)*Cm + Y1*Ct1+ Y2*Ct2 +(Y1+Y2)*R1*CR1+(Y1+Y2)*R2*CR2, gp.GRB.MINIMIZE)
# minimze cost 

m.setObjective(f*EMf + X1*EM1+ X2*EM2+ (X1+X2)*EMf + Y1*EMt1 + Y2*EMt2 + (Y1+Y2)*
R1*EMR1 + (Y1+Y2) *R2*EMR2, gp.GRB.MINIMIZE)

# minimze emissions

m.setObjective(f*Ef + X1*E1+ X2*E2+ (X1+X2)*Em + Y1*Et1 +Y2*Et2+ (Y1+Y2)*R1*ER1 + (Y1+Y2)*R2*ER2
, gp.GRB.MINIMIZE)

# minimize energy 
m.setParam('NonConvex', 2)
m.optimize()