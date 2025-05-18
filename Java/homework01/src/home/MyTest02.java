package home;

import java.util.ArrayList;

/**
 * MyTest
 * depart 普通门诊
 * grade 初级
 *
 * depart 普通门诊
 * grade 副主任医师
 *
 * depart 神经科
 * grade 副主任医师
 *
 * depart 耳鼻喉科
 * grade 主治医师
 */
public class MyTest02 {
    public static void main(String[] args) {
        //创建第一个医生对象
        Doctor doctor01 = new Doctor();
        doctor01.setName("初级医师");
        doctor01.setAccount("doctor01");
        doctor01.setDepart("普通门诊");
        doctor01.setGrade("初级");
        doctor01.setPassword("123");

        Doctor doctor02 = new Doctor();
        doctor02.setName("副主任医师1");
        doctor02.setAccount("doctor02");
        doctor02.setDepart("普通门诊");
        doctor02.setGrade("副主任");
        doctor02.setPassword("456");

        Doctor doctor03 = new Doctor();
        doctor03.setName("副主任医师2");
        doctor03.setAccount("doctor03");
        doctor03.setDepart("神经科");
        doctor03.setGrade("副主任");
        doctor03.setPassword("789");

        Doctor doctor04 = new Doctor();
        doctor04.setName("主治医师");
        doctor04.setAccount("doctor04");
        doctor04.setDepart("耳鼻喉科");
        doctor04.setGrade("主治");
        doctor04.setPassword("012");

        ArrayList<Doctor> list = new ArrayList();
        list.add(doctor01);
        list.add(doctor02);
        list.add(doctor03);
        list.add(doctor04);

        //找到doctor03
        for(int i=0;i<list.size();i++){
            Doctor doctor = list.get(i);
            if("doctor03".equals(doctor.getAccount())){
                System.out.println("找到了");
                doctor.setName("扁鹊");
                System.out.println(doctor.toString());
                //改了原地址信息
                System.out.println(doctor03.toString());
            }
        }
    }
}
