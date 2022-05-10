
import java.net.*;
import java.io.*;


public class SendPost {
    public static void main(String[] args) throws MalformedURLException, IOException {
        URL reqURL = new URL("http://localhost:8080"); //the URL we will send the request to
        HttpURLConnection request = (HttpURLConnection) (reqURL.openConnection());
        String post = "this will be the post data that you will send";
        request.setDoOutput(true);
        request.addRequestProperty("Content-Length", Integer.toString(post.length())); //add the content length of the post data
        request.addRequestProperty("Content-Type", "application/x-www-form-urlencoded"); //add the content type of the request, most post data is of this type
        request.setRequestMethod("POST");
        request.connect();
        OutputStreamWriter writer = new OutputStreamWriter(request.getOutputStream()); //we will write our request data here

        PrintWriter pToDocu = new PrintWriter(String.valueOf(reqURL));
        pToDocu.println("request posted");
        pToDocu.close();
        //OutputStreamWriter writer = new OutputStreamWriter(reqURL); //we will write our request data here
        System.out.println("request posted.");
        writer.write(post);

        writer.flush();
    }
}



