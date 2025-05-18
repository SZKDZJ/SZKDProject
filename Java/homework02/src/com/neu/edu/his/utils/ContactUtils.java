package com.neu.edu.his.utils;

import java.util.Calendar;

/**
 * 文本工具类
 * @date: 0723
 */
public class ContactUtils {

    //判断字符串是否为空
    public static boolean isNull(String msg){
        if(msg==null){
            return false;
        }
        if ("".equals(msg.trim())){//msg.trim()可去除字符串两端空格
            return false;
        }
        return true;
    }
    /**
     * 判断文本是否符合规则
     * 包含字母大写或小写或数字，且长度在4-8范围内
     * @param msg
     * @return
     */
    public static boolean validate(String msg){
        //正则表达式
        String regex = "[a-zA-Z0-9]{4,8}";
        return msg.matches(regex);//msg.matches(regex)
    }

    public  static int getDay(){
        //日历类(系统自带）
        Calendar calendar = Calendar.getInstance();
        //获取今天是星期几
        //周日第一天
        int dayOfWeek = calendar.get(Calendar.DAY_OF_WEEK);
        dayOfWeek -= 1;
        if(dayOfWeek==0){
            dayOfWeek = 7;
        }
        return dayOfWeek;
    }
}