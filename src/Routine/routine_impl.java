package Routine;

/**
 * Created by Ian on 2017/9/25.
 */
public class routine_impl implements routine_interface{
    @Override
    public void f() {
        System.out.println("public C.f()");
    }

    @Override
    public String f2() {
        return null;
    }
}
