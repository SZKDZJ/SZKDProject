package home;

/**
 * 狗
 */
public class dog {
    //属性  定义同时封装
    //私有化
    //private 类型  名字；
    private String name;
    private String type;
    private int age;
    private double weight;
    //行为
    //get** 取值  set** 赋值
    // Alt+Insert  快捷键：迅速生成对应属性的get set 方法
    //或右键-->generate-->setter/getter/getter and setter

    public String getName() {
        return name;
    }

    public String getType() {
        return type;
    }

    public int getAge() {
        return age;
    }

    public double getWeight() {
        return weight;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setType(String type) {
        this.type = type;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public void setWeight(double weight) {
        this.weight = weight;
    }

    //用于展示所有信息
    @Override
    public String toString() {
        return "dog{" +
                "name='" + name + '\'' +
                ", type='" + type + '\'' +
                ", age=" + age +
                ", weight=" + weight +
                '}';
    }
}
