id1_mat = [1 2 3]+1;
id2 = 1;
FP_PW_mat = [-35.64 -4 -3];
real_tag = [];

anchorLoc = [0 0 ; 10 0 ; 0 10 ; 10 10];

TDOA_mat = [1.36680054 -1.50811372 0.10159303];

%filepath = "../../Desktop/Zixin project/nnnsdi_walk_3_17/teraterm.log";
%anchor_selection_solver_Zixin();
NSDI_solve_tag_with_anchor_selection_filter_power_new(id1_mat,id2,TDOA_mat,FP_PW_mat,anchorLoc,real_tag)

%TDoA_fsolve()

% anchor_locations = [0 0 ; 10 0 ; 0 10 ; 10 10];
% TDoA_mat = [1.36680054 -1.50811372 0.10159303];
% id1 = 2
% id2 = 1
% estimation = [0 0];
% 
% NSDI_antenna_correction_TDoA(TDOA_mat,id1,id2)
f_packet_id_mat = [1,1,2,5,7,7,4];
% d = [true, diff(f_packet_id_mat) ~= 0, true];  % TRUE if values change
% m = find(d)
% n = diff(find(d));  % Number of repetitions
% disp(d)
% disp(m)
% disp(n)
f_packet_id_mat = [1,1,2,5,7,7,4];
disp(f_packet_id_mat(1:5));