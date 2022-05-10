package com.felhr.examplestreams;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.view.View;

public class myCanvas extends View {
    private String action = "";
    Paint paint = new Paint();
    Paint paint1 = new Paint();
    Paint paint2 = new Paint();

    int x;
    int y;

    public myCanvas(Context context,int x,int y) {
        super(context);
        this.x = x;
        this.y = y;
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        paint.setTextSize(100);
        paint.setColor(Color.BLUE);
        // Set the point, line width. If do not set this, the point is too small to see, the line is too thin also.
        paint.setStrokeWidth(30);

        paint1.setTextSize(100);
        paint1.setColor(Color.YELLOW);
        // Set the point, line width. If do not set this, the point is too small to see, the line is too thin also.
        paint1.setStrokeWidth(30);

        paint2.setTextSize(100);
        paint2.setColor(Color.RED);
        // Set the point, line width. If do not set this, the point is too small to see, the line is too thin also.
        paint2.setStrokeWidth(30);
        // Fill out the background color to refresh the screen.
//        canvas.drawColor(Color.BLUE);
//        if (ConstantsUtil.DRAW_POINT.equals(action)) {
            // Draw one point in pixel.
//        canvas.drawPoint(0, 0, paint1);
//        canvas.drawPoint(x, y, paint2);
//        System.out.println("width: "+canvas.getWidth());
//        System.out.println("height: "+canvas.getHeight());
//        canvas.drawPoint(canvas.getWidth(), canvas.getHeight(), paint2);
//        canvas.drawPoint(Math.abs(canvas.getWidth()), Math.abs(canvas.getHeight()), paint1);
            canvas.drawPoint((x*canvas.getWidth())/3600, canvas.getHeight()-y*canvas.getHeight()/3100, paint);
//        }
    }
}