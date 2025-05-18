package home;

import java.util.ArrayList;
import java.util.Scanner;

public class HomeWorkTest {
    public static void main(String[] args) {
        //第一个患者
        Patient patient01 = new Patient();
        patient01.setId("2020");
        patient01.setName("Tom");
        patient01.setGeneral("男性");
        patient01.setAge(26);
        patient01.setDepart("眼科");

        //第二个患者
        Patient patient02 = new Patient();
        patient02.setId("2021");
        patient02.setName("David");
        patient02.setGeneral("男性");
        patient02.setAge(35);
        patient02.setDepart("耳鼻喉科");

        //第三个患者
        Patient patient03 = new Patient();
        patient03.setId("2022");
        patient03.setName("Angel");
        patient03.setGeneral("女性");
        patient03.setAge(23);
        patient03.setDepart("神经科");

        //第四个患者
        Patient patient04 = new Patient();
        patient04.setId("2023");
        patient04.setName("Helen");
        patient04.setGeneral("女性");
        patient04.setAge(7);
        patient04.setDepart("儿科");

        //第五个患者
        Patient patient05 = new Patient();
        patient05.setId("2024");
        patient05.setName("Mindy");
        patient05.setGeneral("女性");
        patient05.setAge(36);
        patient05.setDepart("妇产科");

        //放入集合
        ArrayList<Patient> array = new ArrayList<>();
        array.add(patient01);
        array.add(patient02);
        array.add(patient03);
        array.add(patient04);
        array.add(patient05);

        //输入患者名
        System.out.println("请输入患者名字：");
        Scanner scanner = new Scanner(System.in);
        String name = scanner.next();

        //查找患者
        boolean sign = false;
        for(int i=0;i<array.size();i++){
            Patient patient = array.get(i);
            if(name.equals(patient.getName())){
                System.out.println(array.get(i));
                sign = true;
            }
        }
        if(!sign) {
            System.out.println("查无此人");
        }
    }
}
