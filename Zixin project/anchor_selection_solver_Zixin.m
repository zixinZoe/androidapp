
close all;clc;clear
rng(1024)
load( "Anchor_network_GT.mat" )
load("anchor_connectivity.mat")
tagid = 6;

% folder = ['nnnsdi_walk_3_17'];
% file_path = [folder, '/teraterm.log'];
file_path = "../../Desktop/Zixin project/nnnsdi_walk_3_17/teraterm.log";


%% read TDoA
[packet_id_mat,ID1_mat,ID2_mat,TDOA_mat,FP_PW_tag_mat] = NSDI_read_TDoA_new(file_path);
[init_power_packet_id_mat,FP_PW_init_mat]=NSDI_read_init_power(file_path);

% Filter by initiator power (>-105 dBm)
valid_packet_id = init_power_packet_id_mat( find(FP_PW_init_mat>-105) );
%disp('valid_packet_id')
%disp(valid_packet_id)
%% Filter TDoA
% Filter any outliers
keep_idx = find(abs(TDOA_mat)<30000);

f_packet_id_mat = packet_id_mat(keep_idx);
f_ID1_mat = ID1_mat(keep_idx);
f_ID2_mat = ID2_mat(keep_idx);
f_TDOA_mat = TDOA_mat(keep_idx);
f_FP_PW_tag_mat = FP_PW_tag_mat(keep_idx);
% f_FP_PW_anchor_mat = FP_PW_anchor_mat(keep_idx);

%% Solve tag    
idx=1;
%disp(f_packet_id_mat);
d = [true, diff(f_packet_id_mat) ~= 0, true];  % TRUE if values change
n = diff(find(d));  % Number of repetitions
anchor_actual = anchorLoc_mm;

current_idx=1;
tagLoc=[];
dop=[];
anchor_selected={};
candidate = {};
Tsolve = {};
dop_all={};

for i=1:length(n)
    current_idx = 1+sum(n(1:i-1));
    if( n(i)>=2 )
        % offset id by 1 because matlab index starts with 1
        INIT_id = f_ID2_mat(current_idx)+1; % initiator ID
        RESP_id = f_ID1_mat(current_idx:current_idx+n(i)-1)+1; % responder id
        TDOA_in = f_TDOA_mat(current_idx:current_idx+n(i)-1);   % corresponding TDoA
        FP_PW_in = f_FP_PW_tag_mat(current_idx:current_idx+n(i)-1); % First path power of each responder

        [tagLoc(:,i),dop(i),anchor_selected{i},candidate{i},candidate_dop{i},Tsolve{i},dop_all{i}]...
            = NSDI_solve_tag_with_anchor_selection_filter_power_new(RESP_id,INIT_id,TDOA_in,FP_PW_in,anchorLoc_mm,[]); % solver
        packet_seq(i) = f_packet_id_mat(current_idx);
        anchor_combo{i} = [INIT_id,RESP_id]-1;

    end    
    
end

%% Ground truth path（不翻译）
way_pts = [4631,3145;
            4530,2850;
            5191,2672;
            5690,2621;
            5695,3125;
            5659,3879;
            5467,3997;
            5489,4076;
            5180,4303;
            4954,4423;
            4146,3018;
            3763,3209;
            4534,4553]';
        
pts = generate_path_points(way_pts, 1);
pts_mm = pts/66*5*304.8; % convert between real distance and map pixel distance


%% Filter by candidate relative location
good_candidate = [];
tagLoc_candidate = [];
good_packet_id = [];
tagLoc_candidate2 = [];%tag location
packet_id_candidate2 = [];
for i=1:length(candidate)
    
    % If there are only two responders, only check its DoP
    if(size(Tsolve{i},2)==1 && dop(i)<1.1)
        tagLoc_candidate2 = [tagLoc_candidate2, Tsolve{i}];
        packet_id_candidate2 = [packet_id_candidate2 packet_seq(i)];
    end
    
    % If there are more responders, compare the results
    if(size(Tsolve{i},2)>1)
        % Find the 2 solutions with lowest DoP
       [~,I] = sort(dop_all{i});
       temp = Tsolve{i}(:,I(1:2)); 
       % Find distance between these solutions
        d_vec = pdist(temp');
        % It never goes in here
        if(size(temp,2)==1 && min(dop_all{i})<1.1)
            tagLoc_candidate2 = [tagLoc_candidate2, mean(temp,2)];
            packet_id_candidate2 = [packet_id_candidate2 packet_seq(i)];
        % Check if the distance is smaller than 800mm and Dop is smaller
        % than 1.4
        elseif(~isempty(d_vec) && sum(d_vec<800)==length(d_vec) && min(dop_all{i})<1.4)
            tagLoc_candidate2 = [tagLoc_candidate2, mean(temp,2)];
            packet_id_candidate2 = [packet_id_candidate2 packet_seq(i)];
        end
    end


end
tagLoc_candidate2_filterPW = tagLoc_candidate2(:, find(ismember( packet_id_candidate2, valid_packet_id )) );

save('result.mat')
%% Scatterplot(不翻译）
load('result.mat')

figure
imshow(rgb2gray(img))
hold on
draw_network(anchorLoc_img, connectivity, 0:size(connectivity,1),0)

scatter(tagLoc_candidate2_filterPW(1,:)*66/5/304.8,tagLoc_candidate2_filterPW(2,:)*66/5/304.8,'b.')
plot(pts(1,:),pts(2,:),'r','LineWidth',2)
xlim([3430,6020])
ylim([2536,4826])

%% tag error cdf(不翻译）
for i=1:length(tagLoc_candidate2_filterPW)
    closest_pt_idx = dsearchn(pts_mm',tagLoc_candidate2_filterPW(:,i)');
%     plot([pts_mm(1,closest_pt_idx),tagLoc(1,good_candidate(i))],[pts_mm(2,closest_pt_idx),tagLoc(2,good_candidate(i))],'m')
    tagLoc_error2(i) = norm( pts_mm(:,closest_pt_idx)-tagLoc_candidate2_filterPW(:,i) );
end

figure
cdfplot(tagLoc_error2)
xlim([0,5000])