%solves for TDoA; replace with other algorithm(see attached paper)
function F = TDoA_fsolve(x)
load('solve_TDOA.mat')
% F(1) = x(1,1)-A(1,1);
% F(2) = x(2,1)-A(2,1);
% F(3) = x(1,4)-B(1,1);
% F(4) = x(2,4)-B(2,1);
% F(5) = x(1,3)-C(1,1);
% F(6) = x(2,3)-C(2,1);

% F(3) = mean(x(1,:))-(A(1,1)+B(1,1))/2;
% F(4) = mean(x(2,:))-(A(2,1)+B(2,1))/2;

idx = 1;
for i=1:size(D,1)
    for j =1:size(D,2)
        if(D(i,j)~=0)
            F(idx) = -sqrt( (x(1)-A(1,i))^2 + (x(2)-A(2,i))^2 ) + sqrt( (x(1)-A(1,j))^2 + (x(2)-A(2,j))^2 )-D(i,j);
            idx = idx + 1;
            %disp(F)
        end
    end
    
end
