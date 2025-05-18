package com.neu.edu.his.controller;

import com.neu.edu.his.db.DateBase;
import com.neu.edu.his.model.Register;
import com.neu.edu.his.utils.ContactUtils;

/**
 * 挂号窗口的业务控制层
 * @date: 0723
 */
public class RegistrationController {
    /**
     * 挂号窗口的正在判断登录是否成功的方法
     * -1 都是空格 或者null
     * -2
     * 没有按规则 字母、长度不合法
     * 200 登陆成功
     * 0：登录不成功 账号和密码都正确
     */
    public int login(String account,String password) {
        //附加功能：
        //判断输入的字符串是否为空,获取是否都是空格
        if (!ContactUtils.isNull(account) || !ContactUtils.isNull(password)) {
            //不合法，结束该方法
            return -1;
        }
        //判断是否是字母以及数字组成，并且长度是4-8
        if (!ContactUtils.validate(account)||!ContactUtils.validate(password)) {
            //不合法，结束该方法
            return -2;
        }
        //与数据库对比账号密码是否正确
        for(Register register: DateBase.registerTable){
            //对比账号和密码
            if(register.getAccount().equals(account)&&register.getPassword().equals(password)){
                //成功
                return 200;
            }
        }
        //登录不成功
        return 0;
    }
}
