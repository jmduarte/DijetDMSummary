from ROOT import *
import ROOT,sys,os,math
from math import *
import numpy as np


def Gammaqq(gq,Mmed,mq,style):
    if style=="Axial":
        return gq**2*Mmed*math.pow((1-float(4*mq**2)/Mmed**2),1.5)/(4*pi)
    elif style=="Vector":
        return gq**2*Mmed*math.pow((1-float(4*mq**2)/Mmed**2),0.5)*(1+2*float(mq**2)/Mmed**2)/(4*pi)

def Gammaqq_tot(gq,Mmed,style):
    if Mmed>=173*2:
        return 5*Gammaqq(gq,Mmed,0,style)+Gammaqq(gq,Mmed,173,style)
    else:
        return 5*Gammaqq(gq,Mmed,0,style)

def GammaDM(gDM,Mmed,mDM,style):
    if 2*mDM<=Mmed:
        if style=="Axial":
            return gDM**2*Mmed*math.pow((1-float(4*mDM**2)/Mmed**2),1.5)/(12*pi)
        elif style=="Vector":
            return gDM**2*Mmed*math.pow((1-float(4*mDM**2)/Mmed**2),0.5)*(1+2*float(mDM**2)/Mmed**2)/(12*pi)
    else:
        return 0

def A(gq,Mmed,mDM,style):
    return gq**2*Gammaqq_tot(gq,Mmed,style)/(Gammaqq_tot(gq,Mmed,style)+GammaDM(1,Mmed,mDM,style))

def B(gq,Mmed,mDM,style):
    return gq**4*GammaDM(1,Mmed,1,style)/(Gammaqq_tot(gq,Mmed,style)+GammaDM(1,Mmed,mDM,style))

### transfer the limit from gDM=1 & mDM=1 to arbitrary mDM
### used by dijet chi analysis
def g_q(gq,Mmed,mDM,style):
    return math.pow((A(gq,Mmed,mDM,style)+math.pow(A(gq,Mmed,mDM,style)**2+4*B(gq,Mmed,mDM,style),0.5))*0.5,0.5)



### transfer the limit for 2mDM>MMed (gqprime) to gDM=1 & mDM=1
### not useful anymore
def gq(gqprime):
    #return gq*math.pow(0.5+math.pow(0.25+1/(18*(gq**2)),0.5),0.5)
    return math.pow(3*gqprime**2+math.pow(gqprime**2*(9*gqprime**2+2),0.5),0.5)/math.pow(6,0.5)


### width(gq, MMed) function (mDM=1, gDM=1)
def medWidth(gq,Mmed,style):
  return Gammaqq_tot(gq, Mmed, style)/float(Mmed)+1/(12*3.141592653)


### width(gqprime, MMed) function (2mDM>MMed)
def medWidth_gqprime(gq,Mmed,style):
    #return 6*gq**2/(4*3.141592653)
    return Gammaqq_tot(gq, Mmed, style)/float(Mmed)


### gqprime(width, MMed) function
def gqprime(width, Mmed,style):
    for gq in np.linspace(0,1.5,1001):
        if medWidth_gqprime(gq,Mmed,style)<=width:
            gqprime=gq
    return gqprime


## for tests
if __name__=="__main__":

    print "Transfer limits from gq (gDM=1) to gqprime (gDM=inf.)"

    med_min=2000
    med_max=6000
    med_step=10

    file_chi=TFile("limitsDetLHCa_DMAxial_mdm1_v5.root")

    exp_chi=file_chi.Get("gq_exp")
    obs_chi=file_chi.Get("gq_obs")

    new_exp_chi=TGraph(0)
    for mmed in np.linspace(med_min,med_max,num=int((med_max-med_min)/med_step+1)):
        ifound=0
        for gqs in np.linspace(0.1,2.0,1000):
            if ifound==1: continue
            if g_q(gqs,mmed,mmed,"Axial")>exp_chi.Eval(mmed):
                new_exp_chi.SetPoint(new_exp_chi.GetN(),mmed,gqs)
                ifound=1


    new_obs_chi=TGraph(0)
    for mmed in np.linspace(med_min,med_max,num=int((med_max-med_min)/med_step+1)):
        ifound=0
        for gqs in np.linspace(0.1,2.0,1000):
            if ifound==1: continue
            if g_q(gqs,mmed,mmed,"Axial")>obs_chi.Eval(mmed):
                new_obs_chi.SetPoint(new_obs_chi.GetN(),mmed,gqs)
                ifound=1

    file_out=TFile("limitsDetLHCa_DMAxial_gqprime_v5.root","RECREATE")

    new_obs_chi.Write("gqprime_obs")
    new_exp_chi.Write("gqprime_exp")

    file_out.Close()
