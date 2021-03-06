from __future__ import print_function, division
import sys
sys.path.append('../..')

import unittest
from mupif import *
from mupif.tests import demo

import mupif.Physics.PhysicalQuantities as PQ
timeUnits = PQ.PhysicalUnit('s',   1.,    [0,0,1,0,0,0,0,0,0])

class TestEx01(unittest.TestCase):
    def setUp(self):
        self.app1,self.app2=demo.AppCurrTime(None),demo.AppPropAvg(None)
    def testEx01(self):
        app1,app2=self.app1,self.app2
        time  = 0
        timestepnumber=0
        targetTime = 1.0
        while (abs(time -targetTime) > 1.e-6):
            #determine critical time step
            dt = min(app1.getCriticalTimeStep().inUnitsOf(timeUnits).getValue(),
                     app2.getCriticalTimeStep().inUnitsOf(timeUnits).getValue())
            #update time
            time = time+dt
            if (time > targetTime):
                #make sure we reach targetTime at the end
                time = targetTime
            timestepnumber = timestepnumber+1
            # create a time step
            istep = TimeStep.TimeStep(time, dt, targetTime, timeUnits, timestepnumber)

            # solve problem 1
            app1.solveStep(istep)
            #request Concentration property from app1
            c = app1.getProperty(PropertyID.PID_Concentration, app2.getAssemblyTime(istep))
            # register Concentration property in app2
            app2.setProperty (c)
            # solve second sub-problem 
            app2.solveStep(istep)
            # get the averaged concentration
            prop = app2.getProperty(PropertyID.PID_CumulativeConcentration, PQ.PhysicalQuantity(time,timeUnits))
            print ("Time: %5.2f concentraion %5.2f, running average %5.2f" % (istep.getTime().getValue(), c.getValue(istep.getTime()), prop.getValue(istep.getTime())))
        self.assertAlmostEqual(prop.getValue(istep.getTime()),0.55)
    def tearDown(self):
        # terminate
        self.app1.terminate();
        self.app2.terminate();

# python test_ex01.py for stand-alone test being run
if __name__=='__main__': unittest.main()

