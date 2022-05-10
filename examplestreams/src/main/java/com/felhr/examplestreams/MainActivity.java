package com.felhr.examplestreams;

import android.content.BroadcastReceiver;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.ServiceConnection;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.support.annotation.RequiresApi;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.lang.ref.WeakReference;
import java.util.Set;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class MainActivity extends AppCompatActivity {

    /*
     * Notifications from UsbService will be received here.
     */
    private final BroadcastReceiver mUsbReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            switch (intent.getAction()) {
                case UsbService.ACTION_USB_PERMISSION_GRANTED: // USB PERMISSION GRANTED
                    Toast.makeText(context, "USB Ready", Toast.LENGTH_SHORT).show();
                    break;
                case UsbService.ACTION_USB_PERMISSION_NOT_GRANTED: // USB PERMISSION NOT GRANTED
                    Toast.makeText(context, "USB Permission not granted", Toast.LENGTH_SHORT).show();
                    break;
                case UsbService.ACTION_NO_USB: // NO USB CONNECTED
                    Toast.makeText(context, "No USB connected", Toast.LENGTH_SHORT).show();
                    break;
                case UsbService.ACTION_USB_DISCONNECTED: // USB DISCONNECTED
                    Toast.makeText(context, "USB disconnected", Toast.LENGTH_SHORT).show();
                    break;
                case UsbService.ACTION_USB_NOT_SUPPORTED: // USB NOT SUPPORTED
                    Toast.makeText(context, "USB device not supported", Toast.LENGTH_SHORT).show();
                    break;
            }
        }
    };
    private UsbService usbService;
    private TextView display;
    private EditText editText;
    private CheckBox box9600, box38400;
    private MyHandler mHandler;

    private final ServiceConnection usbConnection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName arg0, IBinder arg1) {
            usbService = ((UsbService.UsbBinder) arg1).getService();
            usbService.setHandler(mHandler);
        }

        @Override
        public void onServiceDisconnected(ComponentName arg0) {
            usbService = null;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mHandler = new MyHandler(this);

//        display = (TextView) findViewById(R.id.textView1);
    }

    @Override
    public void onResume() {
        super.onResume();
        setFilters();  // Start listening notifications from UsbService
        startService(UsbService.class, usbConnection, null); // Start UsbService(if it was not started before) and Bind it
    }

    @Override
    public void onPause() {
        super.onPause();
        unregisterReceiver(mUsbReceiver);
        unbindService(usbConnection);
    }

    private void startService(Class<?> service, ServiceConnection serviceConnection, Bundle extras) {
        if (!UsbService.SERVICE_CONNECTED) {
            Intent startService = new Intent(this, service);
            if (extras != null && !extras.isEmpty()) {
                Set<String> keys = extras.keySet();
                for (String key : keys) {
                    String extra = extras.getString(key);
                    startService.putExtra(key, extra);
                }
            }
            startService(startService);
        }
        Intent bindingIntent = new Intent(this, service);
        bindService(bindingIntent, serviceConnection, Context.BIND_AUTO_CREATE);
    }

    private void setFilters() {
        IntentFilter filter = new IntentFilter();
        filter.addAction(UsbService.ACTION_USB_PERMISSION_GRANTED);
        filter.addAction(UsbService.ACTION_NO_USB);
        filter.addAction(UsbService.ACTION_USB_DISCONNECTED);
        filter.addAction(UsbService.ACTION_USB_NOT_SUPPORTED);
        filter.addAction(UsbService.ACTION_USB_PERMISSION_NOT_GRANTED);
        registerReceiver(mUsbReceiver, filter);
    }

    /*
     * This handler will be passed to UsbService. Data received from serial port is displayed through this handler
     */
    class MyHandler extends Handler {
        private final WeakReference<MainActivity> mActivity;

        public MyHandler(MainActivity activity) {
            mActivity = new WeakReference<>(activity);
        }

        int lineNum = 0;//skip the first line
        String line = "";
        String newline = System.getProperty("line.separator");
        final LinearLayout drawingExampleLayout = (LinearLayout)findViewById(R.id.exampleLinearLayout);
        Context context = getApplicationContext();
        int prevx = 0;
        int prevy = 0;
        @RequiresApi(api = Build.VERSION_CODES.O)
        @Override
        public void handleMessage(Message msg){

            switch (msg.what) {
//                case UsbService.MESSAGE_FROM_SERIAL_PORT:
//                    String data = (String) msg.obj;
//                    mActivity.get().display.append("data" + data);
//                    break;
                case UsbService.CTS_CHANGE:
                    Toast.makeText(mActivity.get(), "CTS_CHANGE", Toast.LENGTH_LONG).show();
                    break;
                case UsbService.DSR_CHANGE:
                    Toast.makeText(mActivity.get(), "DSR_CHANGE", Toast.LENGTH_LONG).show();
                    break;
                case UsbService.SYNC_READ:

                    String buffer = (String) msg.obj;//HERE IS THE ONE LINE MESSAGE FOR REAL TIME INPUT
                    String newBuffer = buffer.replace(" ", "@");
                    line = line.concat(newBuffer);//concatenate each character to a string

                    if (line.contains(newline)) {
                        if (lineNum != 0) {
                            lineNum++;
                            //mActivity.get().display.append("Line: " + line);
                            ExecutorService executor = Executors.newSingleThreadExecutor();

                            Callable callable =
                                    new sendGetClass()
                                            .setLine(line);

                            Future<String> future = (Future<String>) executor.submit(callable);

                            try {
                                if(future.get() !="") {
//                                    mActivity.get().display.append("tag location: " + future.get());
                                    drawingExampleLayout.removeAllViews();

                                    String[] coors = future.get().split(",");
                                    String xcor = coors[0].substring(1);
                                    String ycor = coors[1].substring(0,coors[1].length()-1);
//                                    mActivity.get().display.append("x: " + Integer.parseInt(xcor));
//                                    mActivity.get().display.append("y: " + Integer.parseInt(ycor));
                                    if(Integer.parseInt(xcor)>=0 && Integer.parseInt(xcor)<=3600 && Integer.parseInt(ycor)>=0 && Integer.parseInt(ycor)<=3100) {
                                    prevx = Integer.parseInt(xcor);
                                    prevy = Integer.parseInt(ycor);
                                        myCanvas mycanvas = new myCanvas(context, Integer.parseInt(xcor), Integer.parseInt(ycor));
                                    drawingExampleLayout.addView(mycanvas);

                                    if (Integer.parseInt(xcor) > -300 && Integer.parseInt(xcor) < 300) {
                                        if (Integer.parseInt(ycor) > -300 && Integer.parseInt(ycor) < 300) {
                                            //                                            mActivity.get().display.append("at 0");
                                            Snackbar snackbar = Snackbar.make(findViewById(R.id.myCoordinatorLayout), R.string.anchor0,
                                                    Snackbar.LENGTH_SHORT);
                                                Snackbar.SnackbarLayout layout = (Snackbar.SnackbarLayout) snackbar.getView();
// Hide the text
                                                TextView textView = (TextView) layout.findViewById(android.support.design.R.id.snackbar_text);
//                                                textView.setVisibility(View.resolveSize(100,100));
                                                textView.getExtendedPaddingBottom();
                                                textView.setHeight(250);
                                                textView.setTextSize(20);
                                                snackbar.show();
//                                                textView.setGravity(50);
//                                                textView.setPaintFlags(10);
//                                                textView.setBackgroundColor(R.color.background_dark);
// Inflate our custom view
//                                                LayoutInflater mInflater = null;
//                                                View snackView = mInflater.inflate(R.id.my_snackbar, null);
// Configure the view
//                                                ImageView imageView = (ImageView) snackView.findViewById(R.id.image);
//                                                imageView.setImageBitmap(R.id.my_snackbar);
//                                                TextView textViewTop = (TextView) snackView.findViewById(R.id.text);
//                                                textViewTop.setText(R.string.anchor0);
//                                                textViewTop.setTextColor(Color.BLACK);

////If the view is not covering the whole snackbar layout, add this line
//                                                layout.setPadding(0,0,0,0);
//
//// Add the view to the Snackbar's layout
//                                                layout.addView(snackView, 0);
// Show the Snackbar

                                        }
                                        if (Integer.parseInt(ycor) > 2800 && Integer.parseInt(ycor) < 3400) {
                                            //                                            mActivity.get().display.append("at 3");
                                            Snackbar snackbar = Snackbar.make(findViewById(R.id.myCoordinatorLayout), R.string.anchor3,
                                                    Snackbar.LENGTH_SHORT);
                                            Snackbar.SnackbarLayout layout = (Snackbar.SnackbarLayout) snackbar.getView();
// Hide the text
                                            TextView textView = (TextView) layout.findViewById(android.support.design.R.id.snackbar_text);
//                                                textView.setVisibility(View.resolveSize(100,100));
                                            textView.getExtendedPaddingBottom();
                                            textView.setHeight(250);
                                            textView.setTextSize(20);
                                            snackbar.show();


                                        }
                                    }

                                    if (Integer.parseInt(xcor) > 3300 && Integer.parseInt(xcor) < 3900) {
                                        if (Integer.parseInt(ycor) > -300 && Integer.parseInt(ycor) < 300) {
                                            //                                            mActivity.get().display.append("at 0");
                                            Snackbar snackbar = Snackbar.make(findViewById(R.id.myCoordinatorLayout), R.string.anchor1,
                                                    Snackbar.LENGTH_SHORT);
                                            Snackbar.SnackbarLayout layout = (Snackbar.SnackbarLayout) snackbar.getView();
// Hide the text
                                            TextView textView = (TextView) layout.findViewById(android.support.design.R.id.snackbar_text);
//                                                textView.setVisibility(View.resolveSize(100,100));
                                            textView.getExtendedPaddingBottom();
                                            textView.setHeight(250);
                                            textView.setTextSize(20);
                                            snackbar.show();
                                        }
                                        if (Integer.parseInt(ycor) > 2800 && Integer.parseInt(ycor) < 3400) {
                                            //                                            mActivity.get().display.append("at 3");
                                            Snackbar snackbar = Snackbar.make(findViewById(R.id.myCoordinatorLayout), R.string.anchor2,
                                                    Snackbar.LENGTH_SHORT);
                                            Snackbar.SnackbarLayout layout = (Snackbar.SnackbarLayout) snackbar.getView();
// Hide the text
                                            TextView textView = (TextView) layout.findViewById(android.support.design.R.id.snackbar_text);
//                                                textView.setVisibility(View.resolveSize(100,100));
                                            textView.getExtendedPaddingBottom();
                                            textView.setHeight(250);
                                            textView.setTextSize(20);
                                            snackbar.show();


                                        }
                                    }

                                    if (Integer.parseInt(xcor) > 1300 && Integer.parseInt(xcor) < 2100) {
                                        if (Integer.parseInt(ycor) > 1300 && Integer.parseInt(ycor) < 1700) {
                                            //                                            mActivity.get().display.append("at 0");
                                            Snackbar snackbar = Snackbar.make(findViewById(R.id.myCoordinatorLayout), R.string.center,
                                                    Snackbar.LENGTH_SHORT);
                                            Snackbar.SnackbarLayout layout = (Snackbar.SnackbarLayout) snackbar.getView();
// Hide the text
                                            TextView textView = (TextView) layout.findViewById(android.support.design.R.id.snackbar_text);
//                                                textView.setVisibility(View.resolveSize(100,100));
                                            textView.getExtendedPaddingBottom();
                                            textView.setHeight(250);
                                            textView.setTextSize(20);
                                            snackbar.show();
                                        }
                                    }
                                }
                                    else{
                                        myCanvas mycanvas = new myCanvas(context, prevx, prevy);
                                        drawingExampleLayout.addView(mycanvas);
                                    }
//                                    else{
//                                        mActivity.get().display.append("");
//                                    }
                                }
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            } catch (ExecutionException e) {
                                e.printStackTrace();
                            }
                            line = "";

                        } else {
                            lineNum++;
                            line = "";
                        }
                    }
                    //}
                    break;

            }
        }
    }

}
