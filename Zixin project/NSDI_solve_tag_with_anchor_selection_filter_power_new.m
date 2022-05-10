%input: one set of TDoA with a particular initiator; solves for tag location ;filters out all unnecessary results
function [tagLoc,dop,anchor_combo, candidate,candidate_dop,Tsolve,dop_current] = NSDI_solve_tag_with_anchor_selection_filter_power_new(id1_mat,id2,TDOA_mat,FP_PW_mat,anchorLoc,real_tag)


num_response = length(id1_mat);
fun = @TDoA_fsolve;


%% Filter weak anchors
idx_tag_strong = find(FP_PW_mat>-110);
disp(idx_tag_strong)%test idx_tag_strong
% idx_anchor_storng = find(FP_PW_anchor_mat>-150);
if(isempty(idx_tag_strong))
    tagLoc = [0;0];
    dop=0;
    anchor_combo=[];
    candidate=[];
    candidate_dop=[];
    Tsolve=[];
    dop_current=[];
    return
end
idx_strong = idx_tag_strong;
num_response_strong = length(idx_strong);
if(length(idx_strong)<2)
    tagLoc = [0;0];
    dop=0;
    anchor_combo=[];
    candidate=[];
    candidate_dop=[];
    Tsolve=[];
    dop_current=[];
    return
end
%% Rank power and get top 5
if(num_response_strong>5)
    [~,I] = sort(FP_PW_mat(idx_strong));
    I = idx_strong(I(end:-1:end-4));
else
    I = idx_strong;
end

%% 
combo2=[];
combo3=[];
combo4=[];
combo5=[];
combo6=[];

if(length(I)==2)
    combo2 = I;
elseif(length(I)==3)
    combo2 = nchoosek(I,2);
    combo3 = nchoosek(I,3);
elseif(length(I)==4)
    combo2 = nchoosek(I,2);
    combo3 = nchoosek(I,3);
    combo4 = nchoosek(I,4);
elseif(length(I)==5)
    combo2 = nchoosek(I,2);
    combo3 = nchoosek(I,3);
    combo4 = nchoosek(I,4);
    combo5 = nchoosek(I,5);
% elseif(length(I)==6)    
%     combo2 = nchoosek(I,2);
%     combo3 = nchoosek(I,3);
%     combo4 = nchoosek(I,4);
%     combo5 = nchoosek(I,5);
% %     combo6 = nchoosek(I,6);
end

INIT_id = id2;
RESP_id = id1_mat;
D_complete = zeros(size(anchorLoc,1));
D_complete(INIT_id,RESP_id)=TDOA_mat;%TDoA 1*n array one combination of anchors result
 for i=1:size(D_complete,1)
     for j=1:size(D_complete,2)
         if(D_complete(i,j)~=0)
 %             D_complete(i,j) = NSDI_antenna_correction_TDoA_new(D_complete(i,j),i,j,anchorLoc);
             D_complete(i,j) = NSDI_antenna_correction_TDoA(D_complete(i,j),i,j);
 
         end        
     end
 end

A=anchorLoc';%1d:size=2;

count=1;
if(~isempty(combo2))
    for i=1:size(combo2,1)
        idx = combo2(i,:);
        %disp(idx);%test idx
        
        D_mask = zeros(size(D_complete));
        D_mask(INIT_id, RESP_id(idx)) = 1;% find 重新记录index
        D = D_complete .* D_mask;
        save('solve_TDOA.mat','A','D');
        x0 = A(:,1);
        Tsolve(:,count)= fsolve(fun,x0);
%         dop_current(count) = GDOP(A(:,[id2,RESP_id(idx)])', Tsolve(:,count)');
        disp('first input: ')
        disp(A(:,[id2,RESP_id(idx)])')
        disp('second input: ')
        disp(Tsolve(:,count)')
        dop_current(count) = GDOP(A(:,[id2,RESP_id(idx)])', Tsolve(:,count)');
        disp('dop_current: ')
        disp(dop_current)
        anchor_combo{count}=[INIT_id, RESP_id(idx)];
        count=count+1;        
    end
end
if(~isempty(combo3))
    for i=1:size(combo3,1)
        idx = combo3(i,:);
        
        D_mask = zeros(size(D_complete));
        D_mask(INIT_id, RESP_id(idx)) = 1;
        D = D_complete .* D_mask;
        save('solve_TDOA.mat','A','D');
        x0 = A(:,1);
        Tsolve(:,count)= fsolve(fun,x0);
        dop_current(count) = GDOP(A(:,[id2,RESP_id(idx)])', Tsolve(:,count)');
        anchor_combo{count}=[INIT_id, RESP_id(idx)];
        count=count+1;        
    end
end
if(~isempty(combo4))
    for i=1:size(combo4,1)
        idx = combo4(i,:);
        
        D_mask = zeros(size(D_complete));
        D_mask(INIT_id, RESP_id(idx)) = 1;
        D = D_complete .* D_mask;
        save('solve_TDOA.mat','A','D');
        x0 = A(:,1);
        Tsolve(:,count)= fsolve(fun,x0);
        dop_current(count) = GDOP(A(:,[id2,RESP_id(idx)])', Tsolve(:,count)');
        anchor_combo{count}=[INIT_id, RESP_id(idx)];
        count=count+1;        
    end
end
if(~isempty(combo5))
    for i=1:size(combo5,1)
        idx = combo5(i,:);
        
        D_mask = zeros(size(D_complete));
        D_mask(INIT_id, RESP_id(idx)) = 1;
        D = D_complete .* D_mask;
        save('solve_TDOA.mat','A','D');
        x0 = A(:,1);
        Tsolve(:,count)= fsolve(fun,x0);
        dop_current(count) = GDOP(A(:,[id2,RESP_id(idx)])', Tsolve(:,count)');
        anchor_combo{count}=[INIT_id, RESP_id(idx)];

        count=count+1;        
    end
end
% if(~isempty(combo6))
%     for i=1:size(combo6,1)
%         idx = combo6(i,:);
%         
%         D_mask = zeros(size(D_complete));
%         D_mask(INIT_id, RESP_id(idx)) = 1;
%         D = D_complete .* D_mask;
%         save('solve_TDOA.mat','A','D');
%         x0 = A(:,1);
%         Tsolve(:,count)= fsolve(fun,x0);
%         dop_current(count) = GDOP(A()', Tsolve');
%         count=count+1;        
%     end
% end


% [~,I]=min(dop_current);
% tagLoc = Tsolve(:,I);
% dop = dop_current(I);
% anchor_combo = anchor_combo{I}-1;
% scatter(Tsolve(1,:)*66/5/304.8,Tsolve(2,:)*66/5/304.8,'g+')
% [~,I] = min( sqrt(sum( (Tsolve-real_tag).^2, 1 )) );
[~,I]=min(dop_current);
tagLoc = Tsolve(:,I);
% scatter(tagLoc(1)*66/5/304.8,tagLoc(2)*66/5/304.8,'r*')
% scatter(anchorLoc(anchor_combo{I},1)*66/5/304.8,anchorLoc(anchor_combo{I},2)*66/5/304.8,'b','filled')
% scatter(anchorLoc(anchor_combo{I}(1),1)*66/5/304.8,anchorLoc(anchor_combo{I}(1),2)*66/5/304.8,'r','filled')
% idx = find(dop_current<1.2);
% scatter(Tsolve(1,idx)*66/5/304.8,Tsolve(2,idx)*66/5/304.8,'b*')

[~,idx] = sort(dop_current);
disp('idx: ')
disp(idx)
disp('length(idx)')
disp(length(idx))
disp('min(3,length(idx)')
disp(min(3,length(idx)))
disp('idx(1:min(3,length(idx)))')
disp(idx(1:min(3,length(idx))))

idx = idx(1:min(3,length(idx)));
disp('new idx')
disp(idx)
% scatter(Tsolve(1,idx)*66/5/304.8,Tsolve(2,idx)*66/5/304.8,'ko')
if(length(idx)==1)
    candidate=Tsolve;
    candidate_dop = dop_current(1);
else
    candidate=Tsolve(:,idx);
    candidate_dop = dop_current(idx);
end

dop = dop_current(I);
anchor_combo = anchor_combo{I}-1;

end


function dop = GDOP(anchors, tag)%solves for dilusion of precision(the smaller the better)
%% anchors nx2 matrix
%  tag 1x2 vector
anchors = [2.34 2.45 ; 5.34 45.3 ; 65.4 45.2 ; 45.3 3.54];
tag = [1 2];

relative_mat = anchors-tag;
%disp(relative_mat);
distance_vec = sqrt( sum(relative_mat.^2,2) );
%disp(distance_vec);
H = relative_mat ./ distance_vec;
%disp(H);
Q = inv(H' * H);
%disp(Q);
dop = sqrt( trace(Q) );
%disp(dop)
end

%不翻译
function dop = TDoA_DOP(anchors, tag)
%% anchors nx2 matrix
%  tag 1x2 vector
relative_mat = tag-anchors;
distance_vec = sqrt( sum(relative_mat.^2,2) );
H = relative_mat ./ distance_vec - tag/norm(tag);
Q = inv(H' * H);
dop = sqrt( trace(Q) );

end