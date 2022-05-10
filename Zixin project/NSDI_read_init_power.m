%solves for the receive power of initiator; receive power: 信号的强弱（dbm)
function [packet_id_mat,FP_PW_init_mat]=NSDI_read_init_power(file_path)

% Pkt 8350: FP_PW=-93.206276 dbm
%% Read TDoA
fileID = fopen(file_path,'r');
f = fscanf(fileID, '%s');
fclose(fileID);
%FP_POWER\[.*,(?<RX_PW_tag>[-.\d]*),(?<FP_PW_tag>[-.\d]*)\]
tok = regexp(f, 'Pkt(?<packet_id>[\d]*):FP_PW=(?<FP_PW_init>[-.\d]*)dbm','names');

temp_packet_id = {tok.packet_id};
temp_FP_PW_init = {tok.FP_PW_init};%first path receive power(indicator of transmission quality)
%other paths are reflections of signals

packet_id_mat = [];
FP_PW_init_mat = [];

for j=1:length(temp_packet_id)
    packet_id_mat(j) = str2double(temp_packet_id{j});

    FP_PW_init_mat(j) = str2double(temp_FP_PW_init{j});
end 



end