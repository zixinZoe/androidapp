package com.felhr.examplestreams;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.concurrent.Callable;


public class sendGetClass extends Thread implements Callable{
//    public void main(String[] args) throws MalformedURLException, IOException {
//
//        call();
//        //System.out.println("Thread "+Thread.currentThread().getId()+" is running.");
//    }
    //private MainActivity.MyHandler mActivity;
    private MainActivity.MyHandler mActivity;
    private String mLine;


    public sendGetClass setActivity(MainActivity.MyHandler activity)
    { mActivity = activity; return this; }

    public sendGetClass setLine(String line)
    { mLine = line; return this; }

    //public void run() {
    public String call() {
        //URL firstURL = new URL("http://localhost:8080/path?line="+line);
        //URL firstURL = new URL("www.google.com");
        URL firstURL = null;
        try {
            firstURL = new URL("http://localhost:8080/page?line=" + mLine);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
        HttpURLConnection request = null;
        try {
            request = (HttpURLConnection) (firstURL.openConnection());
        } catch (IOException e) {
            e.printStackTrace();
        }
        try {
            request.setRequestMethod("GET");
        } catch (ProtocolException e) {
            e.printStackTrace();
        }
        try {
            request.connect();
        } catch (IOException e) {
            e.printStackTrace();
        }

        //System.out.println(request.getResponseMessage());

        BufferedReader in = null;
        try {
            in = new BufferedReader(
                    new InputStreamReader(request.getInputStream()));
        } catch (IOException e) {
            e.printStackTrace();
        }
        String inputLine = "";
        //StringBuffer content = new StringBuffer();
        String content = "";
        while (true) {
            try {
                if (!((inputLine = in.readLine()) != null)) break;
            } catch (IOException e) {
                e.printStackTrace();
            }
            //content.append(inputLine);
            content = inputLine;
            //return content;
        }
        //System.out.println("tagLocation: " + content);
        try {
            in.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        request.disconnect();
        //return content;
        //mActivity.get().display.append("output"+content;


//        URL reqURL = new URL("http://localhost:8080/path?DDoA=0,5491,5151,8890;0,0,0,0;0,0,0,0;0,0,0,0&anchor_location=0,0;10000,0;0,10000;10000,10000"); //the URL we will send the request to
//        HttpURLConnection request = (HttpURLConnection) (reqURL.openConnection());
//        request.setRequestMethod("GET");
//        request.connect();
//        //request.getResponseCode() ==
//
//        System.out.println(request.getResponseMessage());
//        //解析json object
//
//        BufferedReader in = new BufferedReader(
//                new InputStreamReader(request.getInputStream()));
//        String inputLine;
//        StringBuffer content = new StringBuffer();
//        while ((inputLine = in.readLine()) != null) {
//            content.append(inputLine);
//        }
//        System.out.println("tagLocation: " + content);
//        in.close();
//        request.disconnect();
//
        return content;
    }
//
//    @Override
//    public StringBuffer call() {
//        String line = "heysenorita";
//        StringBuffer output = null;
//        try {
//            output = getTagLocation(line);
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//        return output;
//    }
}