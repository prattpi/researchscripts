# Preservation metrics
import constants
from meteocalc import dew_point

class Metrics:
    def __init__(self, tempf, rh):
        self.tempf = tempf
        self.tempc = (tempf - 32) * 5.0/9.0
        self.rh = rh
    # Calculate Dew Point
    def cal_dp(self):
        return dew_point(temperature=self.tempc, humidity=self.rh).f
    # Calculate Equilibrium Moisture Content (EMC)
    def cal_emc(self):
        emcvalue = max(-20, min(65,(self.tempc))+20) * 101 + (self.rh)
        return constants.emctable[emcvalue]
    # Function to calculate Risk,OK,Good for metal corrosion
    def metal_corr_risk(self, emcvalue):
        if emcvalue < 7:
            return 1 # OK
        elif emcvalue > 10.5:
            return 2 # Risk
        else:
            return 0 # Good
    # Function to calculate risk of mechanical damage 
    def mech_damage_risk(self,emcvalue):
        if (emcvalue < 5 or  emcvalue > 12.5):
            return 2 # Risk
        else:
            return 1 # OK
    # Function to calculate Preservation Index
    def cal_pi(self):
        tempt = 0
        temrh = 0
        if self.tempc < -23:
            tempt = -23
        elif self.tempc > 65:
            tempt = 65
        else:
            tempt = (t+23) * 90
        if self.rh < 6:
            temprh = 6
        elif self.rh > 95:
            temprh = 95
        else:
            temprh = self.rh - 6
        pivalue = tempt + temprh
        return constants.pitable[pivalue]
    # Function to calculate Risk,OK,Good for natural aging
    def nat_aging_risk(self,pivalue):
        if pivalue < 45:
            return 2 # Risk
        elif pivalue > 75:
            return 0 # Good
        else:
            return 1 # OK
    # Function to calculate Mold Growth
    def cal_mold_growth(self):
        pivalue = 0
        ans = 0
        if( self.tempc > 45 or self.tempc < 2 or self.rh < 65):
            ans = 0
        else:
            pivalue = 8010 + (self.tempc - 2) * 36 + (self.rh - 65)
            ans = (constants.pitable[pivalue])
        return ans
    # Function to calculate Mold Risk
    def mold_risk(self,pivalue):
        if pivalue == 0:
            return 0
        else:
            return pivalue # Days to mold
