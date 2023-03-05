# -- coding: utf-8 --
class PoolEmptyError(Exception):
    """
    定义了一个自定义的异常类 PoolEmptyError，该类继承了Exception类，Exception类是Python中所有非退出异常的公共基类。
    在PoolEmptyError类中，定义了一个__init__方法，该方法会在创建一个新的异常对象时被调用，这里的__init__方法并没有定义任何参数，但是调用了父类Exception的__init__方法。
    另外，还定义了一个__str__方法，该方法返回代理池已经枯竭的字符串表示形式。
    当代理池已经没有可用的代理时，就会抛出一个PoolEmptyError异常，而异常信息就是该异常类中定义的__str__方法返回的字符串表示形式。这样做的好处是，当出现异常时，可以自定义异常信息，方便我们进行异常处理。
    """
    def __init__(self):
        # Exception类，是所有非退出异常的公共基类。
        Exception.__init__(self)

    def __str__(self):
        # repr函数，返回对象的规范字符串表示形式。
        return repr('代理池已经枯竭')
