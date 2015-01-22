#!/usr/bin/env python
"""
.. module:: totalstation.py
   :platform: Unix, Windows
   :synopsis: Ulyxes - an open source project to drive total stations and publish observation results.  GPL v2.0 license Copyright (C) 2010-2013 Zoltan Siki <siki@agt.bme.hu>

.. moduleauthor:: Zoltan Siki <siki@agt.bme.hu>, Daniel Moka <mokadaniel@citromail.hu>

"""

from instrument import Instrument
from angle import Angle

class TotalStation(Instrument):
    """ Generic total station instrument
    """
    FACE_LEFT = 0
    FACE_RIGHT = 1

    def __init__(self, name, measureUnit, measureInterf):
        """ Constructor

            :param name: name of instrument
            :param measureUnit: measure unit part of instrument 
            :param measureInterf: interface to measure unit
        """
        # call super class init
        super(TotalStation, self).__init__(name, measureUnit, measureInterf)

    def _process(self, msg):
        """ Send message to measure unit and process answer

            :param msg: message to send
            :returns: parsed answer (dictionary)
        """
        ans = self.measureInterf.Send(msg)
        if self.measureInterf.state != self.measureInterf.IF_OK:
            return {'error': self.measureInterf.state}
        return self.measureUnit.Result(msg, ans)

    def SetATR(self, atr):
        """ Set ATR on 

            :param atr: 0/1 ATR off/on
            :returns: processed answer from instrument
        """
        msg = self.measureUnit.SetATRMsg(atr)
        return self._process(msg)

    def GetATR(self):
        """ Get ATR status of instrument

            :returns: 0/1 ATR off/on
        """
        msg = self.measureUnit.GetATRMsg()
        return self._process(msg)

    def SetLock(self, lock):
        """ Set lock on prism

            :param lock: 0/1 lock off/on
            :returns: processed answer from instrument
        """
        msg = self.measureUnit.SetLockMsg(lock)
        return self._process(msg)

    def GetLock(self):
        """ Get lock status

            :returns: lock status of the instrument 0/1 on/off
        """
        msg = self.measureUnit.GetLockMsg()
        return self._process(msg)

    def SetAtmCorr(self,valueOfLambda, pres, dryTemp, wetTemp):
        """ Set atmospheric correction

            :param valueOfLambda: ????
            :param pres: air presure
            :param dryTemp: dry temperature
            :param wetTemp: wet temperature
        """
        msg = self.measureUnit.SetAtmCorrMsg(valueOfLambda, pres, dryTemp, wetTemp)
        return self._process(msg)

    def GetAtmCorr(self):
        """ Get atmospheric correction

            :returns: atmospheric corrections (dictionary)
        """
        msg = self.measureUnit.GetAtmCorrMsg()
        return self._process(msg)

    def SetRefCorr(self, status, earthRadius, refracticeScale):
        """ Set refraction correction

            :param status: ???
            :param earthRadius: radius of earth
            :param refracticeScale: ???
        """
        msg = self.measureUnit.SetRefCorrMsg(status, earthRadius, refracticeScale)
        return self._process(msg)

    def GetRefCorr(self):
        """ Get refraction correction

            :returns: refraction correction (dictionary)
        """
        msg = self.measureUnit.GetRefCorrMsg()
        return self._process(msg)

    def SetStation(self, easting, northing, elevation):
        """ Set station coordinates

            :param easting: easting of station
            :param northing: northing of station
            :param elevation: elevation of station
            :returns: ???
        """
        msg = self.measureUnit.SetStationMsg(easting, northing, elevation)
        return self._process(msg)

    def    GetStation(self):
        """ Get station coordinates

            :returns: station coordinates (dictionary)
        """
        msg = self.measureUnit.GetStationMsg()
        return self._process(msg)

    def SetEDMMode(self, mode):
        """ Set EDM mode

            :param mode: mode name/id as listed in measure unit
            :returns: ???
        """
        msg = self.measureUnit.SetEDMModeMsg(mode)
        return self._process(msg)

    def GetEDMMode(self):
        """ Get EDM mode

            :returns: actual EDM mode
        """
        msg = self.measureUnit.GetEDMModeMsg()
        return self._process(msg)

    def SetOri(self, ori):
        """ Set orientation

            :param ori: bearing to direction (Angle)
            :returns: ???
        """
        msg = self.measureUnit.SetOriMsg(ori)
        return self._process(msg)

    def SetRCS(self, rcs):
        msg = self.measureUnit.SetRCSMsg(rcs)
        return self._process(msg)

    def Move(self, hz, v, atr=0):
        """ Rotate instrument to a given direction

            :param hz: horizontal direction (Angle)
            :param v: zenith (Angle)
            :param atr: 0/1 ATR on/off
        """
        msg = self.measureUnit.MoveMsg(hz, v, atr)
        return self._process(msg)

    def Measure(self, prg='DEFAULT', incl=0):
        """ Measure distance

            :param prg: EDM program, DEFAULT use actual
            :param incl: inclination ...
            :returns: ???
        """
        if prg == 'DEFAULT':
            prg = self.GetEDMMode()['edmMode']
        msg = self.measureUnit.MeasureMsg(prg, incl)
        return self._process(msg)

    def GetMeasure(self, wait = 12000, incl = 0):
        """ Get measured values

            :param wait: waiting time in ms
            :param inc: inclination ...
            :returns: observations in a dictionary
        """
        msg = self.measureUnit.GetMeasureMsg(wait, incl)
        return self._process(msg)

    def MeasureDistAng(self):
        """ ???
        """
        msg = self.measureUnit.MeasureDistAngMsg()
        return self._process(msg)

    def Coords(self, wait = 1000, incl = 0):
        """ Read coordinates from instrument

            :param wait: waiting time ms
            :param incl: inclination
            :returns: coordinates in a dictionary
        """
        msg = self.measureUnit.CoordsMsg(wait, incl)
        return self._process(msg)

    def GetAngles(self):
        """ Get angles from instrument

            :returns: angles in a dictionary
        """
        msg = self.measureUnit.GetAnglesMsg()
        return self._process(msg)

    def ClearDistance(self):
        """ Clear measured distance on instrument
        """
        msg = self.measureUnit.ClearDistanceMsg()
        return self._process(msg)

    def ChangeFace(self):
        """ Change face

            :returns: ???
        """
        msg = self.measureUnit.ChangeFaceMsg()
        return self._process(msg)

    def GetFace(self):
        """ Get face left or face right

            :returns: 0/1 face left/face right
        """
        a = self.GetAngles()
        if 'v' in a:
            if a['v'].GetAngle('GON') < 200:
                face = self.FACE_LEFT
            else:
                face = self.FACE_RIGHT
        return {'face': 1}

    def MoveRel(self, hz_rel, v_rel, atr=0):
        """ Rotate the instrument relative to actual direction

            :param hz_rel: relative horizontal rotation (Angle)
            :param v_rel: relative zenith rotation (Angle)
            :param atr: 0/1 atr on/off
        """
        #get the actual direction
        msg = self.measureUnit.GetAnglesMsg()
        return self._process(msg)
        return self.Move(res['hz'] + hz_rel, res['v'] + v_rel, atr)

if __name__ == "__main__":
    from leicameasureunit import *
    from serialinterface import *
    mu = LeicaMeasureUnit("TCA 1800")
    iface = SerialInterface("rs-232", "/dev/ttyUSB1")
    ts = TotalStation("Leica", mu, iface)
    ts.SetATR(1)
    print (ts.Move(Angle(0), Angle(90, 'DEG')))
    print (ts.ChangeFace())
    print (ts.GetEDMMode())
    if ts.GetATR()['atrStatus'] == 0:
        ts.SetATR(1)
    print (ts.GetAngles())
    print (ts.GetFace())
    #ts.Measure()
    #print ts.GetMeasure()
