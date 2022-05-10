%不翻译
function draw_network(points, dist_mat, anch_idx,draw_lines)

% figure
scatter(points(:,1),points(:,2),120,'^g','filled','DisplayName','Anchors');
for i= 1:size(points,1)
    labels{i} =['A',num2str(anch_idx(i))];
end
    
text(points(:,1)-85,points(:,2)-65,labels,'VerticalAlignment','bottom','HorizontalAlignment','right','FontSize',12)
hold on

if(draw_lines)
    for i = 1:size(dist_mat,1)
        for j=1:size(dist_mat,2)
          if(dist_mat(i,j)~=0)
              line([points(i,1),points(j,1)], [points(i,2),points(j,2)])
          end
        end

    end
end
axis equal
% axis square

end