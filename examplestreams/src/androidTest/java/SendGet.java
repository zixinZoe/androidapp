import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class SendGet{
//    public static void main(String[] args) throws MalformedURLException, IOException {
//        String line = null;
//        getTagLocation(line);
//    }

    public void getTagLocation (String line) throws IOException {

        URL firstURL = new URL("http://localhost:8080/path?line="+line);

        HttpURLConnection request = (HttpURLConnection) (firstURL.openConnection());
        request.setRequestMethod("GET");
        request.connect();

        System.out.println(request.getResponseMessage());

        BufferedReader in = new BufferedReader(
                new InputStreamReader(request.getInputStream()));
        String inputLine;
        StringBuffer content = new StringBuffer();
        while ((inputLine = in.readLine()) != null) {
            content.append(inputLine);
        }
        System.out.println("tagLocation: " + content);
        in.close();
        request.disconnect();

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
    }
}