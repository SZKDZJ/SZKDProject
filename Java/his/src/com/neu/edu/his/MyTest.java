package com.neu.edu.his;

/**
*单行注释：//
* 多行注释：/**...*/    /*...*/

public class MyTest {
    public static void main(String[] args) {
        System.out.println(100);   //输出语句：sout+回车
        //println  打印后自动回车换行
        //数字
        System.out.println("Hello world!");
        //字母、中文、特殊符号--  字符串""
        System.out.print(100);
        System.out.println("Hello world");
        //print 打印后不换行
        /**
         * 数据类型：2类
         * 1、基本数据类型
         *   数值型：
         *     byte  字节  1 2 3
         *     short 短整型 123
         *     int   整型 123
         *     float 单精度浮点 2.9F
         *     double双精度浮点 2.9
         *     long  长整型 123
         *   字符型：
         *     char  'a'
         *   布尔类型：
         *     boolean:  true  false
         * 2、引用数据类型：
         *    String  字符串""
         *    class
         *    接口......
         */
        /**
         * 变量的定义
         * 修饰符  数据类型  变量名  =  值;
         * 修饰符  数据类型  变量名;
         * 变量名 = 值;
         */
        int i=1;
        System.out.println(i);
        double d=9.6;
        System.out.println(d);
        //字符串
        String s = "东北大学";
        System.out.println(s);
    }
}