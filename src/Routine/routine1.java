package Routine;

/**
 * Created by Ian on 2017/9/25.
 */
class Demo{

}
public class routine1 {
    public static void main(String[] args) {
        String s = "xx";
        Class<?> c = s.getClass();
        try {
            Class<?> c2 = Class.forName("java.lang.String");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        Demo demo1 = new Demo();
        System.out.println(demo1.getClass()); //class Routine.Demo
        routine_interface demo2 = new routine_interface() {
            @Override
            public void f() {

            }

            @Override
            public String f2() {
                return null;
            }
        };
        routine_interface demo3 = new routine_impl();
        demo3.f();

    }
}
