// Copyright (c) 2020 Facebook, Inc. and its affiliates.
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

package org.pytorch.demo.objectdetection;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.ColorFilter;
import android.graphics.LightingColorFilter;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Rect;
import android.graphics.RectF;
import android.graphics.drawable.shapes.RoundRectShape;
import android.util.AttributeSet;
import android.view.View;

import androidx.core.content.ContextCompat;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;


public class ResultView extends View {

    private final static int TEXT_X = 40;
    private final static int TEXT_Y = 35;
    private final static int TEXT_WIDTH = 260;
    private final static int TEXT_HEIGHT = 50;

    private Paint mPaintRectangle;
    private Paint mPaintText;
    private ArrayList<Result> mResults;

    String sign;
    List<String> signs = new ArrayList<>();

    //private java.time.LocalTime timer;

    public ResultView(Context context) {
        super(context);
    }

    public ResultView(Context context, AttributeSet attrs){
        super(context, attrs);
        mPaintRectangle = new Paint();
        mPaintRectangle.setColor(Color.YELLOW);
        mPaintText = new Paint();
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        int height = canvas.getHeight();
        int weidth = canvas.getWidth();
        int size = height/10;
        int topx = 10;
        int topy = height-20;

        Paint paint_rect = new Paint();
        paint_rect.setStyle(Paint.Style.FILL);
        paint_rect.setColor(Color.DKGRAY);
        paint_rect.setAlpha(200);
        RectF rectf_rect = new RectF(topx, topy-size-10, weidth-10, topy+10);
        canvas.drawRoundRect(rectf_rect, 10, 10, paint_rect);

        for (int i=0; i<signs.size(); i++){

            sign = signs.get(i);
            String resource_name = "znak_" + sign;
            int resID = getResources().getIdentifier(resource_name, "drawable", getContext().getPackageName());


            if(resID != 0){
                Class res = R.drawable.class;
                Bitmap bitmap = BitmapFactory.decodeResource(getResources(), resID);
                int topxx = topx + 10 + i*(size+10);
                int topyy = topy-size;
                Paint paint = new Paint();
                paint.setStyle(Paint.Style.FILL);
                paint.setColor(Color.WHITE);
                RectF rectf = new RectF(topxx, topyy, topxx+size, topyy+size);
                if (topx+size<weidth){
                    canvas.drawRoundRect(rectf, 10, 10, paint);
                    canvas.drawBitmap(bitmap, null, rectf
                            , null);

                }
            }

        }

        if (mResults == null) return;
        if (mResults!=null) signs.clear();
        for (Result result : mResults) {
            mPaintRectangle.setStrokeWidth(5);
            mPaintRectangle.setStyle(Paint.Style.STROKE);
            canvas.drawRect(result.rect, mPaintRectangle);

            Path mPath = new Path();
            RectF mRectF = new RectF(result.rect.left, result.rect.top, result.rect.left + TEXT_WIDTH,  result.rect.top + TEXT_HEIGHT);
            mPath.addRect(mRectF, Path.Direction.CW);
            mPaintText.setColor(Color.MAGENTA);
            canvas.drawPath(mPath, mPaintText);

            mPaintText.setColor(Color.WHITE);
            mPaintText.setStrokeWidth(0);
            mPaintText.setStyle(Paint.Style.FILL);
            mPaintText.setTextSize(32);
            canvas.drawText(String.format("%s %.2f", PrePostProcessor.mClasses[result.classIndex], result.score), result.rect.left + TEXT_X, result.rect.top + TEXT_Y, mPaintText);
            sign = PrePostProcessor.mClasses[result.classIndex];
            sign.replace('_', '.');
            if (!signs.contains(sign)){
                signs.add(sign);
            }

        }
    }

    public void setResults(ArrayList<Result> results) {
        mResults = results;
    }
}
