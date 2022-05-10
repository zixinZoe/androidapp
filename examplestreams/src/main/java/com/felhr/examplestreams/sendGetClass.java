package com.felhr.examplestreams;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.concurrent.Callable;


public class sendGetClass extends Thread implements Callable {
//public class sendGetClass{
    private String mLine;

    public sendGetClass setLine(String line)
    { mLine = line; return this; }

//    public static void main(String[] args) {
//        String mLine = "0,0;3600,0;3600,3100;0,3100@115;484;238";
//        call(mLine);
//    }

    public String call() {
        //URL firstURL = new URL("http://localhost:8080/path?line="+line);
        //URL firstURL = new URL("www.google.com");
        URL firstURL = null;
        try {
            firstURL = new URL("http://143.215.95.156:8080/page?line=" + mLine);
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

        return content;
        //return "hello";
    }
}