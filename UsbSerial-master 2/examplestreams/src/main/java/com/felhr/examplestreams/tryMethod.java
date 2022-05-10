//package com.felhr.examplestreams;
//
//import java.util.concurrent.Callable;
//import java.util.concurrent.TimeUnit;
//
////public class tryMethod implements Callable{
////    public void main(String[] args){
////        String output = call();
////        System.out.println(output);
////    }
//////    public static void tryMethod() {
//////        System.out.println("Aloha");
//////    }
////
//////    @Override
//////    public void run() {
//////        System.out.println("Aloha");
//////    }
////    public String call() {
////        return "Aloha";
////    }
////}
//
//
////    public static void main(String[] args) {
////        for (int i = 0; i < 10; i++) {
////            sendGetClass target = new sendGetClass();
////    //String output = "";
////            Thread thread = new Thread(String.valueOf(new Runnable() {
////                public void run() {
////                    String output = "Printing content";
////    //                                output = target.getTagLocation(line);
////    //                                mActivity.get().display.append("output "+output);
////    //                                return output;
////                    //mActivity.get().display.append("output "+output);
////                    System.out.println(output);
////                    //return output;
////                }
////
////            }));
////            thread.start();
////        }
////    }
//
//
//
//
//    private Integer number;
//
//    public void FactorialCalculator(Integer number) {
//        this.number = number;
//    }
//
//    @Override
//    public Integer call() throws Exception {
//        int result = 1;
//        if ((number == 0) || (number == 1)) {
//            result = 1;
//        } else {
//            for (int i = 2; i <= number; i++) {
//                result *= i;
//                TimeUnit.MILLISECONDS.sleep(20);
//            }
//        }
//        System.out.println("Result for number - " + number + " -> " + result);
//        return result;
//    }
//
//
//
//
//public static void main(String[] args) {
//    final int[] numbers = {1, 2, 3};
//    Thread parameterizedThread = new Thread(String.valueOf(new Callable<String>() {
//        @Override
//        public String call() {
//            String material = "print this";
//            System.out.println(material);
//            return material;
//        }
//    }));
//    parameterizedThread.start();
//}
//}