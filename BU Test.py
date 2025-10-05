# import statements
import sympy as spc
import numpy as np
import matplotlib.pyplot as plt

import MechDesign.Helpers as HM

from MechDesign.Units.Units import m_, mm_, kg_, s_, N_, rpm_, W_, deg_
import MechDesign.Units.UnitMethods as UM

import MechDesign.RnM as RnM
# --- comment out the '#' at the beginning of the lines to run the code mentioned above ---
UM.PrintAvailableUnits()
#help(UM)
#help(RnM)         #--- calling this line will give you an overview of the chapters available in this package ---
# creating the chain to be calculated
CH = RnM.Chain()     #--- since Chain is part of the RnM library we call it as a part of it ---

#--- code to demonstrate that CH holds the parameters ---
print(CH.i)          #---This prints the raw value of a symbol named '_i,' a form you are unlikely to use ---
display(CH.i)        #---This prints (displays) a better readable form of symbol '_i' ---
print(CH.n_1)        #---This prints the raw value of a symbol named '_n_1,' a form you are unlikely to use ---
display(CH.n_1)      #---A better readable form of symbol '_n_1', note how the use of the '_' before the '1' generates a nice subscript ---

#---When you're inside a code block (e.g. on the line), try typing 'CH.' and then press 'TAB.' This will display a list of the created parameters.---
#---In the context of this mechanical design code, a distinct class of symbols has been defined. ---
#---These symbols can include 'a description,' 'a comment,' 'a default value,' and 'a range.' ---
#---Note that the key distinction between 'description' and 'comment' lies in their usage: the former is fixed, ----
#---while the latter can be freely utilized for making notes. Let's demonstrate---
#---When attempting this on your own, don't forget to take advantage of tab-completion. ---
#---Note that tab-completion only functions once the code has been executed. ----
display(CH.i.description)
display(CH.n_1.description)
CH.i.comment = 'we still need to figure out this value'
CH.i.range = [1, 5000]
CH.i.def_value = 5678
#---Several helper functions are also available, including one for printing out expressions. All of these functions are part of the 'H' module. ---
HM.MyHelp(CH.i)       #---The function is named 'MyHelp' because it provides assistance for the expressions you generate.---
#---Let's create a very simple, nonsensical dummy expression ---
DummyExpression = CH.i*CH.n_1
HM.MyHelp(DummyExpression)
#---Note that symbols are indeed closley printed together.---
#---Utilize these additional properties to your advantage while coding.----
# setting the value of known parameters
CH.n_1=125 * rpm_    #---Notice the imidiate addition of units---
CH.n_2=50 * rpm_
#---Let's diplay n_1 now---
HM.EqPrint('n_1',CH.n_1)     #---The first input of 'EqPrint' can be any text without spaces and will be placed on the left-hand side of the equation.---
HM.EqPrint('something',CH.n_1)
t=0 #---By default, code cells will print the last line of code if it doesn't contain an '=' sign. Adding 't=0' is just to prevent double printing.---
# An initial estimate of the gear ratio is needed; the final gear ratio will depend on the number of teeth on both gear wheels.
iprime = CH.n_1/CH.n_2
HM.EqPrint('iprime',iprime)
t=0       
#--- Notice that the two units, of course, cancel each other out. ---
CH.z_1 = 23
CH.z_2 = 57
#---In this particular scenario, we have the option to manually code this, but all the formulas from the book are already available.---
CH.i = CH.E17_1B_GearRatioTeeth() #---When multiple expressions share the same equation number, they are ordered from left to right as A,B,C, etc.---
#---Again remember the tab-completions, expressions all start with E'chapterNr'_'NrOfExpression. ---
#---Typing 'E17_1' and pressing 'Tab' will limit the options, and tab-completion will help you avoid typos in the method names ---
HM.EqPrint('i',CH.i*mm_)
t=0