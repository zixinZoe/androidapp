function pts = generate_path_points(way_points, gap)
   pts = [];
    for i=1:size(way_points,2)-1
        step_vec = (way_points(:,i+1)-way_points(:,i))/norm(way_points(:,i+1)-way_points(:,i))*gap;
        
        line_x = way_points(1,i):step_vec(1):way_points(1,i+1);
        line_y = way_points(2,i):step_vec(2):way_points(2,i+1);
        
        pts = [pts [line_x;line_y]];
    end

end