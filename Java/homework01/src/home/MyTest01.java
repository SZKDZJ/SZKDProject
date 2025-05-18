package home;

public class MyTest01 {
    public static void main(String[] args) {
        //使用dog类
        //类型 对象名 = new leixing();
        dog Dog = new dog();
        Dog.setName("小白");
        Dog.setType("土狗");
        Dog.setAge(0);
        Dog.setWeight(2.5);

        System.out.println(Dog.getName());
        System.out.println(Dog.getType());
        System.out.println(Dog.getAge());
        System.out.println(Dog.getWeight());

        System.out.println(Dog.toString());
    }
}
