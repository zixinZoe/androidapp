%矫正TDoA
function dist_mm_corrected = NSDI_antenna_correction_TDoA(TDoA_mm,id1,id2)
TDoA_mm = 1.36680054;
id1 = 2;
id2 = 1;
antenna_delays = [-514.800046735725;
-515.807752377787;
-515.311106592656; 
-515.115189872074;
-514.882780169421;
-513.592856014242;
-514.918087972098;
-515.128385013776;
-514.793541561308;
-515.321036364222;
-515.241712743109;
-514.973272610434;
-514.989929612259];

c=physconst('lightspeed');
dist_mm_corrected = ( 4*TDoA_mm/1000/c*1e9 + 2*antenna_delays(id2) ...
    - 2*antenna_delays(id1) )/4/1e9*1000*c;
disp(dist_mm_corrected)
end