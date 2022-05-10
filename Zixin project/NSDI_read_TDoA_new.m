%interprets the TDoA file
function [packet_id_mat,ID1_mat,ID2_mat,TDOA_mat,FP_PW_tag_mat]=NSDI_read_TDoA_new(file_path)

% Pkt 8153 - 3 to 10: FP_PW=-88.443237 dBm; TDoA-ToA 3 to 10: -174707 mm;
% Pkt 8153: FP_PW=-79.861740 dbm
% Pkt 64851 - 2 to 10: FP_PW=-78.819443 dBm; TDoA 2 to 10: -7297 mm

%% Read TDoA
file_path = "../../Desktop/Zixin project/nnnsdi_walk_3_17/teraterm.log";%test
fileID = fopen(file_path,'r');
f = fscanf(fileID, '%s');
fclose(fileID);
%FP_POWER\[.*,(?<RX_PW_tag>[-.\d]*),(?<FP_PW_tag>[-.\d]*)\]
tok = regexp(f, 'Pkt(?<packet_id>[\d]*)-\d*to\d*:FP_PW=(?<FP_PW_tag>[-.\d]*)dBm;TDoA(?<ID1>[-\d]*)to(?<ID2>[-\d]*):(?<TDoA>[-\d]*)mm;','names');

temp_packet_id = {tok.packet_id};
temp_ID1 = {tok.ID1};
temp_ID2 = {tok.ID2};
temp_TDOA = {tok.TDoA};
% temp_FP_PW_anchor = {tok.FP_PW_anchor};
% temp_RX_PW_anchor = {tok.RX_PW_anchor};
temp_FP_PW_tag = {tok.FP_PW_tag};

packet_id_mat = [];
ID1_mat = [];
ID2_mat = [];
TDOA_mat = [];
% FP_PW_anchor_mat = [];
% RX_PW_anchor_mat = [];
FP_PW_tag_mat = [];

for j=1:length(temp_ID1)
    packet_id_mat(j) = str2double(temp_packet_id{j});
    ID1_mat(j)=str2double(temp_ID1{j});
    ID2_mat(j)=str2double(temp_ID2{j});
    TDOA_mat(j) = str2double(temp_TDOA{j});
%     FP_PW_anchor_mat(j) = str2double(temp_FP_PW_anchor{j});
%     RX_PW_anchor_mat(j) = str2double(temp_RX_PW_anchor{j});
    FP_PW_tag_mat(j) = str2double(temp_FP_PW_tag{j});
end 
length(packet_id_mat)%test


end