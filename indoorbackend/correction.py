
#ddoa: a single distance difference of arrival
#antenna_delays: a tuple of delay in each antenna
def antenna_correct_ddoa(ddoa, id1, id2, antenna_delays):
   
   c = 299792458
   corrected_ddoa = ( 4*ddoa/1000/c*1e9 + 2*antenna_delays[id2] - 2*antenna_delays[id1] )/4/1e9*1000*c
   return corrected_ddoa
   #print corrected_ddoa

# antenna_delays = [-514.800046735725,
# -515.807752377787,
# -515.311106592656, 
# -515.115189872074,
# -514.882780169421,
# -513.592856014242,
# -514.918087972098,
# -515.128385013776,
# -514.793541561308,
# -515.321036364222,
# -515.241712743109,
# -514.973272610434,
# -514.989929612259]




# antenna_correct_ddoa(1.36680054,1,0,antenna_delays)
