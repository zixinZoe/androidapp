package com.felhr.examplestreams;

import android.content.BroadcastReceiver;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
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

        display = (TextView) findViewById(R.id.textView1);
        editText = (EditText) findViewById(R.id.editText1);
        Button sendButton = (Button) findViewById(R.id.buttonSend);
        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!editText.getText().toString().equals("")) {
                    String data = editText.getText().toString();
                    if (usbService != null) { // if UsbService was correctly binded, Send data
                        usbService.write(data.getBytes());
                    }
                }
            }
        });

        box9600 = (CheckBox) findViewById(R.id.checkBox);
        box9600.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(box9600.isChecked())
                    box38400.setChecked(false);
                else
                    box38400.setChecked(true);
            }
        });

        box38400 = (CheckBox) findViewById(R.id.checkBox2);
        box38400.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(box38400.isChecked())
                    box9600.setChecked(false);
                else
                    box9600.setChecked(true);
            }
        });

        Button baudrateButton = (Button) findViewById(R.id.buttonBaudrate);
        baudrateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(box9600.isChecked())
                    usbService.changeBaudRate(9600);
                else
                    usbService.changeBaudRate(38400);
            }
        });
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

        //sendGetClass sendget = new sendGetClass();
        String line = "";
        String newline = System.getProperty("line.separator");

        @Override
        public void handleMessage(Message msg) {
            switch (msg.what) {
                case UsbService.MESSAGE_FROM_SERIAL_PORT:
                    String data = (String) msg.obj;
                    mActivity.get().display.append("data" + data);
                    break;
                case UsbService.CTS_CHANGE:
                    Toast.makeText(mActivity.get(), "CTS_CHANGE", Toast.LENGTH_LONG).show();
                    break;
                case UsbService.DSR_CHANGE:
                    Toast.makeText(mActivity.get(), "DSR_CHANGE", Toast.LENGTH_LONG).show();
                    break;
                case UsbService.SYNC_READ:
                    String buffer = (String) msg.obj;//HERE IS THE ONE LINE MESSAGE FOR REAL TIME INPUT
                    String newBuffer = buffer.replace(" ", "_");
                    line = line.concat(newBuffer);//concatenate each character to a string

                    if (line.contains(newline)) {

//                        Thread thread = new Thread(new Runnable() {
//                            @Override
//                            public void run() {


                                ExecutorService executor = Executors.newSingleThreadExecutor();
                                //ThreadPerTaskExecutor executor = new ThreadPerTaskExecutor();
//                        Thread thread =
//                                new sendGetClass()
//                                        .setActivity(this)
//                                        .setLine(line);
                                Callable callable =
                                        new sendGetClass()
                                                .setActivity(this)
                                                .setLine(line);

                                //thread.start();

                                Future<String> future = (Future<String>) executor.submit(callable);
                                //Future<String> future = executor.execute(callable);
                                try {
                                    mActivity.get().display.append(future.get());
                                } catch (InterruptedException e) {
                                    e.printStackTrace();
                                } catch (ExecutionException e) {
                                    e.printStackTrace();
                                }
//                            }
//                        }
//                        );

                        //thread.start();
                        //String line = "line: " +
                       // mActivity.get().display.append("line: "+line);


                        //if(! thread.isAlive()) {
                        line = "";
                        //}

//                        mActivity.get().display.append(line);
//                        line="";
                    }
//                    if(line.contains(newline)){
//                        mActivity.get().display.append(line);
//                        line = "";
//                    }
                    //line = "";
                    break;
            }
                        //mActivity.get().display.append("bufferblock: "+line);
//                        sendGetClass target = new sendGetClass();
//                        //String output = "";
//                        Thread thread = new Thread(String.valueOf((Callable<String>) () -> {
//                            String output = "Printing content";
////                                output = target.getTagLocation(line);
////                                mActivity.get().display.append("output "+output);
////                                return output;
//                              mActivity.get().display.append("output "+output);
//                              return output;
//                        }));
//                        thread.start();

                        //Thread thread = new Thread(target);
                        //thread.start();
//                            Callable call = new target.getTagLocation(line);
//                           Thread thread =  new Thread(call);
//                            //StringBuffer output = target.getTagLocation(line);
//                            StringBuffer output = thread.start();
                        //mActivity.get().display.append("output"+output);


            }
        }

//    class ThreadPerTaskExecutor implements Executor {
//        public void execute (Runnable r) {
//            new Thread(r).start();
//        }
////        public void submit (Callable c) {
////            new Thread((Runnable) c).start();
////        }
//    }
    }
