import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

import MechDesign.Helpers as HM

from MechDesign.Units.Units import m_, mm_, kg_, s_, N_, rpm_, W_, deg_
import MechDesign.Units.UnitMethods as UM

import MechDesign.RnM as RnM

#setting and converting initial parameters
def angular_velocity(linear_speed):
    linear_speed_1 = (linear_speed * 1000) / 3600  # Convert km/h to m/s
    SPR_n = linear_speed_1 / (0.5 / 2)  # Assuming a wheel diameter
    SPR_w = SPR_n * (60/(2 * np.pi)) # Convert RPM to rad/s
    return SPR_w

#calulating motor power
def input_power(eff_belt, eff_gear, P_out, K_a):
    P_in = P_out*K_a / (eff_belt * eff_gear)
    return P_in
# Example usage
eff_belt = 0.8  # Belt efficiency  
eff_gear = 0.99  # Gear efficiency
P_out = 6000 # Output power in Watts
K_a = 1.4  # Application factor

P_in = input_power(eff_belt, eff_gear, P_out, K_a)
print(P_in, "W")

SPR_w = angular_velocity(15.5)  # Assign the result to SPR_w
#assign classes
BL = RnM.Belt()
GR = RnM.GearDesign()


#display(BL.i_b)
#display(GR.i_g)
BL.n_1=1500*rpm_
GR.r_n2=SPR_w*rpm_
i_c=0.6
BL.n_2=sp.sqrt(BL.n_1*GR.r_n2/i_c)

print(round(SPR_w,2))
print(BL.n_2,2)
GR.r_n1=BL.n_2
# i total
BL.i = BL.n_1/BL.n_2
GR.i = GR.r_n1/GR.r_n2
i_tot = BL.i * GR.i
print(round(i_tot,2))

#number of teeth
Z_1 = 21
Z_2 = Z_1 * GR.i
print(round(Z_2,0)+1)
#check gear ratio
print(round(GR.i,2))

#Shaft diameter
SH = RnM.Shaft()
SH.E11_5A_MinDiameter
SH.tau_max=240*N_/mm_# material 38Cr2
SH.P = P_in  # Input power in Watts

SH.T = 9550*P_in / (2*3.14*SPR_w*rpm_)
SH.d = (16*SH.T/(np.pi*SH.tau_max))**(1/3)

print("Shaft 1", SH.d, "mm")
print("Torque 1", SH.T, "Nm")

#key connection parameters
key_length = 1.5*SH.d
key_height = 0.5*SH.d
key_width = 0.33*SH.d
print("Key length", key_length, "mm")
print("Key height", key_height, "mm")
print("Key width", key_width, "mm") 


######---KEY CONNECTION CALCULATIONS---#######
#####---COPIED FROM KEY_BU_SHORT.IPYNB---#####

SC=RnM.ShaftConnection()
# SC now hold a specific instance of a ShaftConnection.  On initialization all variables are set to their respective symbolic representation, as can bee seen from the following display statement
print('SC.p_gem now hold the following symbol:')
print(SC.p_gem)

# let's start by setting the value of SC.p_gem to the expression E12_1B
SC.p_gem = SC.E12_1B_KeyAveragePressure()  # this specific instance of SC.p_gem now hold the expression, with all of the symbols
HM.EqPrint('p_gem',SC.p_gem)  # the first part is just text converted to symbol for display purposes only
HM.EqPrint('p_average',SC.p_gem) # as can be seen, the displayed formula is identical, except the left hand
# On the expression: help can be asked using hte build in MyHelp function.  Caution: this is not implemented yet for all help files 
dummy=HM.MyHelp(SC.p_gem)  # the explenations found are the default explenations

# next step is to start adding details 
# setting up constants, based on assignment (units are specified using a trailing '_')
SC.d = SH.d*mm_
SC.T_nom = SH.T*N_*m_
SC.K_A = K_a

# setting up constants that are not likely to change
SC.phi = 1 # 1key
SC.n = 1 # 1 key
SC.K_lambda = 1 # method C

SC.K_t = 0.92
SC.b = key_width*mm_
SC.h = key_length*mm_

# setting up constants chosen more arbitrary
# guessing a first value for key length
SC.l = 80*mm_  # when using l'<=1.3*d with a shaft of 60mm and key width of 18 mm l'<= 78 and l<78+18=96mm and a DIN 116 A60 has max length of 85mm

# setting up helper functions
SC.lprime = SC.E12_1_hI_KeyEffectiveLength()
SC.hprime = SC.E12_1_hJ_KeyEffectiveHeight()
SC.T_eq = SC.E12_1_hC_DynamicLoadTorque()

# all of the elements above now hold a specific value (including a unit)
# e.g.
print('example of a variable holding a value and unit')
HM.EqPrint('SC.d',SC.d)
# meanwhile, SC.p_gem is not changed, it still is holding the symbolic expression
print('p_gem is still holding a symbolic expression')
HM.EqPrint('p_gem',SC.p_gem)
t=HM.MyHelp(SC.p_gem)

# in order to replace the symbols with their value counterparts we have to substitute the symbols in the expression of  p_gem with the specific values (or expressions) from a specific shaft connection instance. 
# broken down into different steps:

# 1 copy expression into a temporary expression
MyExp = SC.p_gem
HM.EqPrint('MyExpOnP_gem',MyExp)
# 2 substitute the symbols in this temporary expression with the values, symbols or expressions from a specific shaft connection (SC)
MyExp2 = HM.substitute(MyExp,SC)
HM.EqPrint('MyEx_2_pOnP_gem',MyExp2)

# intermezzo: the 'substitute' function can also be used to substitute a specific symbol with something else. 
# pairs of symbol and value have to be provided, separated with a ',' 
# e.g.: setting the diameter to 2*60 and K_lambda to 2, will cancel out. Resulting in the identical value for p_gem
# Non-specified parameters will be taken from 'SC'
# Do experiment with some other values, in order to get accustomed with this function.
MyExp3 = HM.substitute(MyExp,SC,d=2*60*mm_,K_lambda=2)  
HM.EqPrint('MyEx_3_pOnP_gem',MyExp3)

# 3 replace the expression for p_gem, in a specific shaft connection, with the new expression
SC.p_gem = MyExp2

# or short:
# SC.p_gem = MD.substitute(SC.p_gem,SC)

# as can be seen from the display statement, units are still to be simplified. 
SC.p_gem = UM.m_to_mm(SC.p_gem)
t=HM.EqPrint('p_gem',SC.p_gem)