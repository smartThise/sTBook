#import "../module/myutils.typ":*
#show:conf

= OOP
#outline()

<oop>
== 〇 哇好神秘还有绪论课 #datetime(day:28,month:2,year:2026).display()
<哇好神秘还有绪论课-2026.2.28>
我去，居然是雷霆方法论基础？！结构化？！面向对象？！神秘秘神？！

#strong[不能反直觉反常识？！强强！？] 对象？我的对象在哪里？！弱弱，，，
#strong[属性和操作？！静态和动态？！] 抽象？！过程抽象和数据抽象？！
eg.类型是什么？！#strong[数据的存储和表示+数据支持的操作？！]

== 壹 编译源程序 #datetime(day:3,month:3,year:2026).display()
<壹-编译源程序-2026.3.3>
=== 一、编译链接
<一编译链接>
#link("./20260303/argv.cpp")[举例： argv argc 等参数的运用]

实际意义上的一个完整编译流程如下：

```bash
g++ -c ex1.cpp 
g++ -o ex1 ex1.o
```

第一步是编译，第二步是链接。 注意到还有多文件链接。

```bash
g++ -c ex1.cpp ex1.o
g++ -c func1.cpp func1.o
g++ ex1.o func1.o -o ex1
```

当然我们平时偷懒是可以的。
只是想告诉你这个编译和链接的实际过程，第二步把两个文件里的函数链接了？！

#strong[链接文件里面声明和定义不相同会类型报错。]
`#include`的本质是把代码直接复制下来了。
#strong[声明可以多声明，定义只能定义一次。]
声明的时候可以修改只说参数类型，不喊名字。
#strong[变量也可以声明或者定义。即使不赋值也可以被定义！注意下面的例子：]

```cpp
// num.cpp
int a=1;
```

```cpp
// ex1.cpp
int a;
int main(){
    a=1;
    return 0
}
```

这时就炸了。重复定义。 #strong[定义=声明+内存分配] 
=== 二、`extern` 关键字 
有一点点烧脑。用于全局变量的共享。

```cpp
//num.h
extern int a;
extern int b;
extern int c;
extern int d[10];

//num.cpp
#include<num.h>
a=1;
b=2;
c=3;
```

头文件中只声明，不定义，目的是防止重复定义。 
=== 三、宏定义/常量
请使用`const`以保证类型的正确性！ 对于宏：

```cpp
#define name(value) command_string
#define sqr(x) ((x)*(x))

sqr(3+2) = 25
```

#strong[请注意这个时候括号十分重要。因为不带括号的时候只是把串原封不动地搬运过来。]
宏定义可以用来防止头文件被反复包含。

```cpp
// Method 1
#ifndef _HEAD_
#define _HEAD
...(如声明/定义)
#endif
// Method 2
#pragma once
```

还可以用来神秘的 debug。

```cpp
#define DEBUG
#ifdef DEBUG
debug();
#endif
```

=== 四、Make
<四make>
`Makefile`编写规则：
#strong[只编译并链接被修改的文件，其他不管。但是如果头文件被改变了，所有引用了这个头文件的都要重新编译。]
格式举例：

```bash
all: main test
main: main.cpp stu.cpp
    g++ -o main main.cpp stu.cpp
test: stu.cpp stu_test.cpp
    g++ -o test stu_test.cpp stu.cpp
clean:
    rm main test

//bash 举例
make all
make test
make main
make clean
```

Make 的更多用法还是自己去查吧。 氧气和臭氧优化后不能 gdb。

=== 五、函数重载：一个函数名字，两个以上实现方法。
*关键在于参数类型的不同。但是如果出现了参数的缺省，就会产生二义性。*

举例：
```cpp
int fun(int a, int b=0);
int fun(int a); 
```
会产生二义性。因为当调用`fun(1)`的时候，编译器无法判断是调用第一个函数还是第二个函数。

但是！
```cpp
int fun(int a);
int fun(float a); 
```
*就不会产生二义性。因为当调用`fun(1)`的时候，编译器会选择第一个函数，因为参数类型是`int`，而不是`float`。*

=== 六、auto, decltype
`auto`和`decltype`都是C++11引入的类型推断机制，可以编译器根据上下文自动推断变量的类型。

==== `auto`
```cpp
auto x = 5; // x 的类型被推断为 int
auto y = 3.14; // y 的类型被推断为 double
auto z = "Hello"; // z 的类型被推断为 const char*
```

- `auto`必须在定义时初始化。
- `auto`不能用于函数参数声明。
- `auto`不能用如 `sizeof, typeid` 等上下文中。
  
- 在定义模板函数时用于声明依赖模板参数的返回类型：
```cpp
template<typename _Tx, typename _Ty>
void Multiply(_Tx x, _Ty y){
    auto v = x * y; // 返回类型由编译器根据表达式 x * y 推断
    std::cout << v << std::endl;
}
Multiply(3, 4.5); // 输出 13.5，v 的类型被推断为 double
```
  
==== `decltype`
- 重用匿名类型：
```cpp
struct {
    int a;
    double b;
} myStruct;
decltype(myStruct) anotherStruct; // anotherStruct 的类型与 myStruct 相同   
```

除此之外还可以用来追踪推导 `auto` 返回的的类型，在 C++ 14 后不必要：
```cpp 
auto func(int x,int y) -> decltype(x+y) {
    return x + y; // 返回类型被推断为 int
}
```

=== 七、内存申请和释放
```cpp
int* p = new int(10); // 申请一个 int 类型的内存
int *arr = new int[5]; // 申请一个 int 类型的数组
delete p; // 释放单个 int 类型的内存
delete[] arr; // 释放数组内存  
```

`nullptr` 是 C++11 引入的空指针常量，表示一个空指针。使用 `nullptr` 可以避免与整数 `0` 混淆，提高代码的可读性和安全性。

== 贰 对象 #datetime(day:10,month:3,year:2026).display()

*成员函数必须在类的内部声明，但是可以在类的外部定义（实现）。*

举例：
```cpp
class MyClass {
public:
    void myFunction(); // 成员函数声明
};
void MyClass::myFunction() { // 成员函数定义
    // 函数体
}
```

=== 一、访问权限：
- `public`：公共成员，类的外部可以访问。
- `private`：私有成员，只有类的内部可以访问。也是默认的访问权限。
- `protected`：受保护成员，只有类的内部和派生类可以访问。

可以通过 `object.member` 的方式访问对象的成员函数和成员变量。或者 `pointer->member` 的方式访问指针指向对象的成员函数和成员变量。在类外只能访问 `public` 成员。

神秘：在类的内部可以访问传入的同一个类的对象的 `private` 成员！因为它们属于同一个类。

举例：
```cpp
class MyClass {
private:
    int privateVar;
public:
    void setPrivateVar(int value) {
        privateVar = value; // 访问自己的 private 成员
    }
    void accessOther(MyClass& other) {
        other.privateVar = 10; // 访问同类的其他对象的 private 成员
    }
};
```

=== 二、`this`指针
指向当前对象的指针。可以在成员函数内部使用 `this` 来访问当前对象的成员变量和成员函数。

举例：
```cpp
class MyClass {
private:
    int value;  
public:
    MyClass(int v) : value(v) {}
    void printValue() {
        cout << "Value: " << this->value << endl;
    }
};
```

错综复杂的类外类内关系……阿弥诺斯，小白手套欸呦喂，我这不赖，已取餐。

=== 三、内联函数
由于和宏代码是直接拷贝复制代码到指定位置，会产生莫名其妙的边际效应，你永远无法想象到各种优先级问题，即使加了括号也不一定能完全解决。

相比之下，*内联函数*可以执行类型检查，可调试。它的本质是生成和函数等价的表达式。并且*宏定义*无法调用私有成员函数，而内联函数可以。

注意事项：
- 避免大段代码的内联，因为会增加编译时间和可执行文件的大小。
- *避免对包含循环、递归或复杂逻辑的函数使用内联。*
- 避免将声明和定义分开，因为内联函数必须在调用之前定义。
- 定义在类内部的成员函数默认是内联的，但这只是一个建议，编译器可能会选择不内联。
- *一般构造函数、析构函数*通常会被编译器自动内联。

`inline` *永远只是建议修饰，不是命令。*编译器有权拒绝不合理的内联请求。

=== 四、`new delete`

`new` 生成一个类对象，并且返回它的指针。、

```cpp
A *pA = new A(1);
```

`delete` 释放一个类对象。

== 叁 构造函数和析构函数 #datetime(day:17,month:3,year:2026).display()

回顾：要对用户定义类型进行严格检查；要隐藏属性；要自动化对象的初始化和清除，做好对象内存分配等等。

=== 一、构造函数：诞生

- 构造函数没有返回值
- 构造函数名与类名相同
- 构造函数可以重载

举例：
```cpp
class Student {
    int ID;
    public:
        Student(int id) : ID(id) {}
        Student(int year,int order){
            ID = year * 10000 + order;
        }
};
```

*注意！按照声明顺序而不是初始化顺序排列成员！*如下面 `ID1` 不可预测。

```cpp
class Student {
    int ID1;
    int ID2;
    public:
        Student(int id) : ID2(id), ID1(ID2) {}
};
```
==== 委派构造函数：调用其他构造函数。

```cpp
class Info{
    public:
        Info(int a):a(a){}
        Info(int a,int b):Info(a){b=b;}
        Info(int a,int b,int c):Info(a,b){c=c;}
};
```

==== 就地初始化：
```cpp
class A{
    private:
        int a{0};
        double b=2.0;
    public:
            A(){}
};
```

==== 默认/缺省构造函数：
```cpp
class A{
    public:
        A(){};
};

A a;
A b=A();
A c();
// 这个时候 c 是一个函数声明，而不是一个对象声明。它可以生成一个对象。

//显式默认构造函数
class A{
    public:
        A()=default;
};

//显式删除默认构造函数
class A{
    public:
        A()=default;
        A(int i){}
        A(char cls)=delete;

};
A a('c');
```

*一个实例生成的时候，会先调用成员的构造函数（如果成员没有就默认构造），再构造自己的。*

*如果你已经定义了构造函数，编译器不会帮你默认构造了！！！*

==== 对象数组的初始化：
```cpp
A a[50];
// 只有一个参数
A a[3]={1,2,3};
//多个参数
A a[3]={A(1,2),A(3,4),A(5,6)};
```

=== 二、析构函数：死亡
- 没有参数
- 唯一
- 没有返回值

举例：
```cpp
class MyClass {
    int num;
    int* ID_list;
public:
    MyClass() { // 构造函数
        // 构造函数体
    }
    ~MyClass() { // 析构函数
        // 析构函数体
        if(ID_list) delete[] ID_list; // 释放内存
    }
};
```

*析构函数会在对象生命周期结束时自动调用。*比如说程序结束的时候：
```cpp
//我们此前 Test 里面创建了一个 Member m

Test t;
int main(){return 0;}
// 输出： ~Test() ~Member()
```

*晚构造，先析构！！！*

析构函数也会自动隐式定义。*但是不会删除指针成员，因此可能导致内存泄漏。*

=== 三、局部对象的构造和析构

其实没啥好说的，就是看括号里面的东西。

=== 四、全局对象的构造和析构

- 在 `main()` 之前构造
- 在同一编译单元中，按照定义顺序构造
- 在不同编译单元中顺序不确定
- 在 `main()` 执行完 `return` 语句后析构

*尽量少用全局对象！*全局对象之间最好不要有依赖关系，否则析构顺序会出问题。

=== 五、引用

引用是对象的别名，可以理解为指针常量。引用必须在声明时初始化，并且一旦初始化就不能改变。

举例：
```cpp
int a = 5;
int& ref = a; // ref 是 a 的引用
ref = 10; // 修改 ref 也会修改 a
cout << a << endl; // 输出 10
```

二者绑定，改了一个另一个也会变。而且不能解绑。

有些时候和指针很像。

举例：交换两个变量的值
```cpp
void swap(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}
```

*看一个做错的题：*

```cpp
class Int {
public:
    int data;
    Int() { data = 1; }
    Int(int i): data(i) {}
};

void func1(Int& a, Int b) {
    a.data += b.data;
}

Int& func2(Int& a, Int b) {
    func1(a, b);
    Int tmp(a.data + b.data);
    return tmp;
}

int main() {
    Int a, b(3);
    Int& f = func2(a, b);
    cout << a.data << "_";
    cout << f.data << endl;
    return 0;
}
```

初始状态：`a.data = 1`（默认构造），`b.data = 3`（值构造）。

调用 `func2(a, b)` 时，`Int& a` 是 main 中 a 的引用，`Int b` 是值拷贝。

+ `func1(a, b)` 执行 `a.data += b.data`，即 $1 + 3 = 4$，main 中的 `a.data` 变为 4。
+ `Int tmp(a.data + b.data)` 在栈上构造局部变量，`tmp.data` $= 4 + 3 = 7$。
+ `return tmp` 返回 `tmp` 的引用。

`func2` 返回类型为 `Int&`，而 `tmp` 是栈帧上的局部变量。函数返回后栈帧销毁，`tmp` 随之消亡，main 中的 `f` 成为悬空引用（dangling reference），指向已释放的内存。

注意：`tmp` 并非"返回前被销毁"，而是函数返回后随栈帧一起消亡。引用被传递出去了，但其所指向的对象已不复存在，后续访问是未定义行为。

引用的用途：
- 作为函数参数，可以避免复制对象，提高效率。
- 作为函数返回值，可以返回引用，而不是复制对象。
- 作为类的成员变量，可以简化代码，提高可读性。
- 相对指针，引用更安全，不会出现空指针的情况。

=== 六、运算符重载

举例：
```cpp
A& operator+=(A& a){
    data+=a.data;
    return *this;
}
```
可以重载的运算符：
- 算术运算符：+、-、\*、/、%
- 关系运算符：==、!=、<、>、<=、>=
- 逻辑运算符：&&、||、!
- 位运算符：&、|、^、~、<<、>>
-  单目运算符：+、-、\*、&、!
-  自增自减运算符：++、--
-  赋值运算符：=、+=、-=、\*=、/=、%=、&=、|=、^=、<<=、>>=
-  空间运算符：new、delete、new[]、delete[]
-  其他运算符：()、[]、->、,、->\*

==== 前缀后缀重载区分

后缀关键是引入了哑元，哑元可以没有名，所以可能实际不会被调用。

```cpp
A operator++(int){
    A temp(data);
    ++data;
    return temp;
}
```

==== () 重载

```cpp
int operator()(int a, int b){
    return a+b;
}
```

==== [] 重载

```cpp
int& operator[](int i){
    return data[i];
}
```

如果是引用，则可以修改原对象。否则只能读取。

注意：=，[]，()，-> 这几个运算符只能重载为成员函数。否则可能会对是否自动合成重载符产生影响。

==== 流运算符重载

```cpp
ostream& operator<<(ostream& os, const A& a){
    os<<a.data;
    return os;
}

istream& operator>>(istream& is, A& a){
    is>>a.data;
    return is;
}

```

此时我们不得不谈到：友元。

=== 七、友元 #datetime(day:24,month:3,year:2026).display()

```cpp
#include <iostream>
using namespace std;

class Test {
    int id;
public:
    Test(int i) : id(i) { cout << "obj_" << id << " created\n"; }

    friend istream& operator>> (istream& in, Test& dst);
    friend ostream& operator<< (ostream& out, const Test& src);
};

istream& operator>> (istream& in, Test& dst) {
        in >> dst.id;
        return in;
}

ostream& operator<< (ostream& out, const Test& src) {
    out << src.id << endl;
    return out;
}

int main() {
    Test obj(1);
    cout << obj;  // operator<<(cout,obj)
    cin >> obj;   // operator>>(cin,obj)
    cout << obj;
    return 0;
}
```

友元是这个对象的“朋友”，可以访问这个对象的私有成员 / 保护成员。

举例：
```cpp
class A{
    int data;
    friend B b;
    b.id=data;
}
```
友元函数举例：

```cpp
class A{
    int data;
    friend void func(A a);
    friend void X::foo(A);
    friend X::X(Y),X::~X();
};
A a;
func(a);
```

友元函数在类外定义，但是可以访问类的私有成员。且在 `private,public` 声明没有区别。

更详细的例子：
```cpp
class Y; // 前向声明
class X
{
    int data;
    friend void func(X &x, Y &y);
};
class Y
{
    int data;
    friend void func(X &x, Y &y);
};
void func(X &x, Y &y)
{
    cout << x.data << y.data << endl;
}

```
友元类：
```cpp
class Y {};
class A{
    int data;
    friend class Y;
    friend X;
}
class X{};
// X,Y 都可以访问 A 的私有成员
```

*注意：*
- 友元关系是*非对称的*，即 A 是 B 的友元，B 不是 A 的友元。
- 友元关系*不传递*，即 A 是 B 的友元，B 是 C 的友元，A 不一定是 C 的友元。
- 友元关系*不具继承性*，即 A 是 B 的友元，C 继承自 B，A 不一定是 C 的友元。
- 友元声明不能直接在里面定义了。

== 肆 静态变量和静态函数 常量

=== 一、静态变量，静态函数

内部可链接，只能初始化一次，而且作用域仅限其声明的文件。*比如*在其他文件被 `extern` 声明后*不*可以在其他文件中使用。

前缀是 `static`。

==== 静态数据成员 / 类变量

在整个类内所有对象共享，初始化时需要加 `static`。应该在 `.h` 文件中声明，在 `.cpp` 文件（实现文件）中定义，防止重复定义。

在实例化所有对象之前就已经分配了静态数据成员的内存空间。

举例：
```cpp
// Test.h
class Test {
public:
    static int count;
    Test();
    ~Test();
};

// Test.cpp
#include "Test.h"
int Test::count = 0;
Test::Test() { count++; }
Test::~Test() { count--; }

// main.cpp
#include "Test.h"
int main() {
    Test a;
    Test b;
    cout << Test::count << endl; // 输出 2
    cout << a.count << endl; // 输出 2
    return 0;
}
```

==== 静态成员函数

只能访问静态成员变量，不能访问非静态成员变量。因为非静态成员变量是每个对象独有的，而静态成员函数是所有对象共享的。


=== 二、常量

- `const` 修饰的变量不能被修改。
- 修饰引用/指针时，引用/指针不能被修改，指向的内容不能被修改。
- 修饰函数返回值时，函数返回值不能被修改。

==== 常量数据成员

可以在构造函数初始化列表中初始化、就地初始化，但是不能在构造函数体通过赋值初始化。

==== 常量成员函数

不能修改非静态数据成员，即不能改变对象的状态。

==== 常量对象

只能调用常量成员函数，不能调用非常量成员函数。

错误举例：
```cpp
class Student {
    int ID;
    public:
        Student(int id) : ID(id) {}
        int who() const { return ID; } // 常量成员函数
        int Who() {return ID;} // 编译错误，常量函数不能调用非常量成员
};
```

==== 常量静态变量

需要在类外初始化。但是有两个例外：`int` 和 `enum` 可以就地初始化。

*不存在*常量静态函数。静态函数是所有对象共享的，而常量函数只能在常量对象上调用。

```cpp
class Foo{
    static const int a=1; // 可以就地初始化
    static const int b; // 可以在类外初始化
    static const char* cs; // 不可以就地初始化
};
```

哦哦哦，给你看哥哥的大表格！

#table(
  columns: (auto, 1fr, 1fr, 1fr, 1fr),
  align: center + horizon,
  stroke: 0.5pt,

  // 表头
  [],
  [静态数据成员],
  [常量数据成员],
  [常量静态数据成员\(除int enum 外)],
  [常量静态数据成员\(int, enum)],

  // 初始化
  table.cell(colspan: 5)[*初始化*],
  [就地初始化],       [],    [✓],  [],    [✓],
  [初始化列表初始化], [],    [✓],  [],    [],
  [构造函数体内初始化],[],   [],   [],    [],
  [类外初始化],       [✓],   [],   [✓],   [✓],

  // 访问
  table.cell(colspan: 5)[*访问*],
  [普通成员函数], [✓], [✓], [✓], [✓],
  [静态成员函数], [✓], [],  [✓], [✓],
  [常量成员函数], [✓], [✓], [✓], [✓],

  // 修改
  table.cell(colspan: 5)[*修改*],
  [普通成员函数], [✓], [], [], [],
  [静态成员函数], [✓], [], [], [],
  [常量成员函数], [✓], [], [], [],
)

==== 再谈常量对象和静态对象：构造和析构

- 常量对象的构造和析构时机和普通对象一样。
    - 在 `main()` 函数开始执行前，全局对象被构造。
    - 在 `main()` 函数执行结束后，全局对象被析构。
    - 在执行到局部对象的代码前，局部对象被构造。    
    - 在局部对象作用域执行结束后，局部对象被析构。
- 静态全局对象的构造和析构时机和普通全局对象一样。
- 函数中的静态对象在函数调用时构造，*离开作用域不析构*。第二次调用函数时，静态对象不会被重新构造，直接使用上一次构造的结果。在 `main()` 函数结束后，静态对象被析构。

- 类静态对象：类 A 的 对象 a 作为类 B 的静态变量。
    - 在 `main()` 函数开始执行前初始化。
    - 在 `main()` 函数结束后析构。
    - 和 B 的构造和析构时机无关。

== 伍 参数对象的构造和析构

如果传递的是形参

```cpp
class A{
    public:
        const char* s;
        A(const char* str) : s(str) {
            cout << s << "A constructing" << endl;
        }
        ~A() {
            cout << s << "A destructing" << endl;
        }
};
```

如果传递的是引用

```cpp
class A{
    public:
        const char* s;
        A(const char* &str) : s(str) {
            cout << s << " A constructing" << endl;
        }
        ~A() {
            cout << s << " A destructing" << endl;
        }
};
void func(A a) {
    cout << a.s << "func" << endl;
}
int main() {
    A a("a");
    func(a);
    return 0;
}
```

输出：(构造一次，析构两次？！)

其实是 b 被拷贝构造函数进行了初始化。函数结束，b 被析构。

```
a A constructing
...
a A destructing
a A destructing
```

如果传递传递指针，你很有可能对同一块空间进行了两次释放，从而报错！

所以尽可能使用引用传递，避免拷贝构造函数和析构函数的调用，还可以节省时间开销。

// 1. 构造函数调用次数分析
#let count_table = table(
  columns: (auto, 1fr, auto),
  inset: 8pt,
  align: (center, left, center),
  stroke: 0.5pt + gray,
  [*语句*], [*解析*], [*调用次数*],
  [`A *p = new A;`], [堆上创建单个对象], [1],
  [`A p2[10];`], [对象数组（10个元素）], [10],
  [`A p3;`], [栈上普通对象], [1],
  [`A *p4[10];`], [指针数组（不创建对象）], [0],
  [*总计*], [], [*12*]
)

#count_table

// 2. 类与成员特性要点
- *类内初始化*：C++11 允许声明时直接赋值。
- *静态成员函数*：没有 `this` 指针，不能访问非静态成员。
- *静态数据成员*：必须类外定义，严禁在 `.h` 中直接定义（防重复定义）。
- *常量静态整型*：`static const int` 允许类内初始化。

// 3. 内存释放安全性
#rect(
  fill: rgb("#fff0f0"), 
  stroke: red, 
  inset: 10pt,
  radius: 2pt,
  width: 100%
)[
  *核心警告：* `new[]` 必须配对 `delete[]`。
  
  $ "Actual Start Address" = p A - 4 $
  
  若误用 `delete pA`：
  1. 仅调用第一个元素的析构函数，导致内存泄漏。
  2. 释放地址错误（应从 $p A - 4$ 处释放），直接导致程序崩溃。
]

=== 一、参数中的常量和常量引用

*最小特权原则*：给足够完成任务的权限，但是不要多余修改、删除权限。

这个时候终于出现了我们喜闻乐见众所周知的：*常量引用*！


在这个例子里面，我们通过常量引用，将 `const` 修饰的变量传递给函数，这样函数内部就不能修改这个变量了。
```cpp
void add(const int& a,const int&b)
```

=== 二、拷贝构造函数

拷贝构造函数是 C++ 的一种特殊的构造函数，它用于创建一个新对象，该对象是已有对象的副本。

拷贝构造函数的格式如下：
```cpp
ClassName(const ClassName& obj){id=obj.id;...}
```

其中，`ClassName` 是类的名称，`obj` 是一个已有的对象，用于初始化新对象。*用参数对象初始化当前对象！*

拷贝构造函数被调用的三种常见情况：
+ 用一个类对象定义另一个新的类对象 `Test a; Test b(a); Test c=a;`
+ 函数调用时以类的对象为形参 `Func(Test a)`
+ 函数返回类对象 `Test Func(void)`

编译器会自动调用”拷贝构造函数”，在已有对象基础上生成新对象。

#image("../Assets/img/20260331_134659.png",width:500pt)

==== 拷贝构造函数：实例1

```cpp
#include <iostream>
using namespace std;
class Test {
public:
    Test() { //构造函数
        cout << “Test()” << endl;
    }
    Test(const Test& src) { //拷贝构造
        cout << “Test(const Test&)” << endl;
    }
    ~Test() { //析构函数
        cout << “~Test()” << endl;
    }
};
Test copyObj(Test obj) {
    cout << “func()...” << endl;
    return Test();
}
int main() {
    cout << “main()...” << endl;
    Test t;
    t = copyObj(t);
    return 0;
}
```

输出：
```text
main()...
Test() //main函数内初始化 Test
Test(const Test&)//func参数 拷贝构造
func()...
Test()  //初始化 Test类的对象
Test(const Test&) //返回时拷贝构造
~Test()
~Test()
~Test()
~Test()
```

*注意：*采用编译选项禁止编译器进行返回值优化：
`g++ test.cpp --std=c++11 -fno-elide-constructors -o test`

==== 拷贝构造函数：实例2

```cpp
#include <iostream>
#include <cstring>
using namespace std;
class Pointer {
    int *m_arr;
    int m_size;
public:
    Pointer(int i):m_size(i) { //构造
        m_arr = new int[m_size];
        memset(m_arr, 0, m_size*sizeof(int));
    }
    ~Pointer(){delete []m_arr;} //析构
    void set(int index, int value) {
        m_arr[index] = value;
    }
    void print();
};
void Pointer::print() {
    cout << “m_arr: “;
    for (int i = 0; i < m_size; ++ i) {
        cout << “ “ << m_arr[i];
    }
    cout << endl;
}
int main() {
    Pointer a(5);
    Pointer b = a; //调用默认的拷贝构造
    a.print();
    b.print();
    b.set(2, 3);
    b.print();
    a.print();
    return 0;
}
```

输出：
```text
m_arr:  0, 0, 0, 0, 0  //a.print()
m_arr:  0, 0, 0, 0, 0  //b.print()
m_arr:  0, 0, 3, 0, 0  //b.print()
m_arr:  0, 0, 3, 0, 0  //a.print()
```

#strong[问题分析：]位拷贝会使得对象 `a, b` 的指针成员 `m_arr` 指向同一个内存地址。当类内含指针类型的成员时，为避免指针被重复删除，不应使用隐式定义的拷贝构造函数。

==== 问题？
造成程序效率显著下降。

尽可能避免使用拷贝构造函数，使用引用传递参数！！！

解决方法：

- （1）使用引用/常量引用传参数或返回对象；

- （2）将拷贝构造函数声明为private；

- （3）用delete关键字让编译器不生成拷贝构造函数的隐式定义版本。

=== 三、内联函数、左值引用与右值引用

==== 左值与右值

首先区分什么是左值和右值：

- *左值*：可以取地址、有名字的值。例如变量 `a`。
- *右值*：不能取地址、没有名字的值。常见于常量、函数返回值、表达式结果。例如 `1`、`a+b`。

```cpp
int a = 1;
int b = func();
int c = a + b;
// a, b, c 是左值
// 1, func()返回值, a+b的结果 是右值
```

左值可以取地址，并且可以被 `&` 引用（左值引用）：
```cpp
int *d = &a;      // ✓ 左值可以取地址
int &e = a;       // ✓ 左值引用绑定左值
int *f = &(a+b);  // ✗ 右值不能取地址
int &g = a + b;   // ✗ 普通左值引用不能绑定右值
```

==== 右值引用

虽然右值无法取地址，但可以被 `&&` 引用（右值引用）：

```cpp
int &&e = a + b;  // ✓ 右值引用绑定右值
int &&f = a;      // ✗ 右值引用不能绑定左值
const int &g = 3; // ✓ 常量左值引用可以绑定右值
```

==== 引用绑定规则

#table(
  columns: (auto, 1fr, 1fr, 1fr),
  align: center + horizon,
  stroke: 0.5pt,
  [], [非常量左值], [常量左值], [右值],
  [非常量左值引用 &], [✓], [], [],
  [常量左值引用 const &], [✓], [✓], [✓],
  [右值引用 &&], [], [], [✓],
)

关键点：
+ 左值引用能绑定左值，右值引用能绑定右值
+ *例外*：常量左值引用也能绑定右值（为了兼容性设计）
+ 所有的引用（包括右值引用）本身都是左值

==== 右值引用示例

```cpp
void ref(int &x) {
    cout << "left " << x << endl;
}
void ref(int &&x) {
    cout << "right " << x << endl;
}
int main() {
    int a = 1;
    ref(a);   // 输出: left 1（a是左值，调用左值引用版本）
    ref(2);   // 输出: right 2（2是右值，调用右值引用版本）
    return 0;
}
```

一个有趣的例子：
```cpp
void ref(int &x) { cout << "left " << x << endl; }
void ref(int &&x) {
    cout << "right " << x << endl;
    ref(x);   // 这里调用哪个？
}
int main() {
    ref(1);   // 1是右值
    return 0;
}
```

输出：
```text
right 1
left 1
```

因为*所有的引用本身都是左值*！`x` 虽然是右值引用参数，但它本身是个有名字的变量，所以是左值。

==== 右值引用的意义

右值引用的核心用途：*延续即将销毁变量的生命周期*。

当函数返回一个临时对象时，这个对象马上就要被销毁。如果使用拷贝构造函数，需要重新开辟内存并复制数据，效率低下。使用右值引用配合移动构造函数，可以直接"偷走"临时对象的资源。

#strong[简单理解：]
- 左值 = 有名字、有地址的"常住居民"，可以长期使用
- 右值 = 没名字、即将消亡的"临时工"，资源可以被"偷走"
- 左值引用 `&` = 给"常住居民"起别名
- 右值引用 `&&` = 在"临时工"消失前，把它的资源转移出来

=== 四、移动构造函数

==== 移动构造函数 vs 拷贝构造函数

```cpp
// 拷贝构造函数
ClassName(const ClassName& VariableName);

// 移动构造函数
ClassName(ClassName&& VariableName);
```

核心区别：
- *拷贝构造*：重新开辟内存，复制数据
- *移动构造*：直接"偷走"临时对象的指针，不复制数据

#table(
  columns: (1fr, 1fr, 1fr),
  align: center + horizon,
  stroke: 0.5pt,
  [], [拷贝构造函数], [移动构造函数],
  [参数类型], [`const ClassName&`], [`ClassName&&`],
  [内存操作], [重新开辟并拷贝], [直接复用指针],
  [适用场景], [对象需要长期保留], [临时对象即将销毁],
)

==== 移动构造函数示例

```cpp
class Test {
public:
    int *buf;  // only for demo
    Test() {
        buf = new int[10];  // 申请一块内存
        cout << "Test(): this->buf @ " << hex << buf << endl;
    }
    ~Test() {
        cout << "~Test(): this->buf @ " << hex << buf << endl;
        if (buf) delete[] buf;
    }
    // 拷贝构造函数
    Test(const Test& t) : buf(new int[10]) {
        for(int i=0; i<10; i++)
            buf[i] = t.buf[i];  // 拷贝数据
        cout << "Test(const Test&) called. this->buf @ "
             << hex << buf << endl;
    }
    // 移动构造函数
    Test(Test&& t) : buf(t.buf) {  // 直接复制地址，避免拷贝
        cout << "Test(Test&&) called. this->buf @ "
             << hex << buf << endl;
        t.buf = nullptr;  // 将t.buf改为nullptr，使其不再指向原来内存区域
    }
};
```

==== 移动构造函数实例

```cpp
Test GetTemp() {
    Test tmp;
    cout << "GetTemp(): tmp.buf @ " << hex << tmp.buf << endl;
    return tmp;
}
void fun(Test t) {
    cout << "fun(Test t): t.buf @ " << hex << t.buf << endl;
}
int main() {
    Test a = GetTemp();
    cout << "main() : a.buf @ " << hex << a.buf << endl;
    fun(a);
    return 0;
}
```

===== 情况一：开启返回值优化（默认）

编译指令：`g++ test.cpp --std=c++11 -o test`

```text
Test(): this->buf @ 0x7fa908c04b90
GetTemp(): tmp.buf @ 0x7fa908c04b90
main() : a.buf @ 0x7fa908c04b90
Test(const Test&) called. this->buf @ 0x7fa908c04ba0
fun(Test t): t.buf @ 0x7fa908c04ba0
~Test(): this->buf @ 0x7fa908c04ba0
~Test(): this->buf @ 0x7fa908c04b90
```

注意：编译器进行了返回值优化（RVO），所以没有调用移动构造函数，也少调用了几次拷贝构造函数！

===== 情况二：禁止返回值优化 + 有移动构造函数

编译指令：`g++ test.cpp --std=c++11 -fno-elide-constructors -o test`

```text
Test(): this->buf @ 0x7f8951c04b90
GetTemp(): tmp.buf @ 0x7f8951c04b90
Test(Test&&) called. this->buf @ 0x7f8951c04b90
~Test(): this->buf @ 0x0 (tmp被移动后)
Test(Test&&) called. this->buf @ 0x7f8951c04b90  (a = GetTemp())
~Test(): this->buf @ 0x0 (GetTemp返回的临时对象)
main() : a.buf @ 0x7f8951c04b90
Test(const Test&) called. this->buf @ 0x7f8951c04ba0
fun(Test t): t.buf @ 0x7f8951c04ba0
~Test(): this->buf @ 0x7f8951c04ba0
~Test(): this->buf @ 0x7f8951c04b90
```

注意观察：
+ `Test a = GetTemp()` 调用了移动构造函数（因为 `GetTemp()` 返回的是右值）
+ `fun(a)` 调用了拷贝构造函数（因为 `a` 是左值）
+ 移动构造后，原对象的 `buf` 变成了 `nullptr`

===== 情况三：禁止返回值优化 + 删除移动构造函数

编译指令：`g++ test.cpp --std=c++11 -fno-elide-constructors -o test`

```text
Test(): this->buf @ 0x7fabf8c04b50
GetTemp(): tmp.buf @ 0x7fabf8c04b50
Test(const Test&) called. this->buf @ 0x7fabf8c04b60
~Test(): this->buf @ 0x7fabf8c04b50
Test(const Test&) called. this->buf @ 0x7fabf8c04b50
~Test(): this->buf @ 0x7fabf8c04b60
main() : a.buf @ 0x7fabf8c04b50
Test(const Test&) called. this->buf @ 0x7fabf8c04b60
fun(Test t): t.buf @ 0x7fabf8c04b60
~Test(): this->buf @ 0x7fabf8c04b60
~Test(): this->buf @ 0x7fabf8c04b50
```

没有移动构造函数时，全部使用拷贝构造函数。

==== 什么时候调用移动构造函数？什么时候调用拷贝构造函数？

#strong[判断依据：引用的绑定规则]

+ 拷贝构造函数的形参类型为 `const ClassName&`（常量左值引用），可以绑定：常量左值、左值、右值
+ 移动构造函数的形参类型为 `ClassName&&`（右值引用），可以绑定：右值
+ *优先级*：当传入右值时，优先匹配右值引用参数的函数

===== 拷贝构造函数的调用时机

+ 用一个类对象/引用/常量引用初始化另一个新的类对象
  - `Test b = a;`（a 是左值）
  - `Test b = ref_a;`（ref_a 是引用）
+ 以类的对象为函数形参，传入实参为类的对象/引用/常量引用
  - `func(a);`（a 是左值）
+ 函数返回类对象（类中未显式定义移动构造函数，不进行返回值优化）

===== 移动构造函数的调用时机

+ 用一个类对象的右值初始化另一个新的类对象
  - `Test b = func(a);`（func 返回临时对象，是右值）
  - `Test b = std::move(a);`（std::move 把左值转成右值）
+ 以类的对象为函数形参，传入实参为类对象的右值
  - `func(Test());`（临时对象是右值）
  - `func(std::move(a));`（std::move 把 a 转成右值）
+ 函数返回类对象（类中显式定义移动构造函数，不进行返回值优化）
  - `return Test();` 或 `return tmp;` 均调用移动构造

==== 返回值优化（RVO）

编译器默认会进行返回值优化，条件：
+ return 的值类型与函数签名的返回值类型相同
+ return 的是一个局部对象

开启 RVO 时，编译器会直接在调用者的栈帧上构造返回值，完全省去拷贝/移动构造函数的调用。

*注意*：如果你想观察移动构造函数的效果，需要用 `-fno-elide-constructors` 禁用 RVO。

==== std::move 函数

`std::move` 可以将左值转换为右值，从而触发移动构造函数：

```cpp
Test a;
Test b = std::move(a);  // 调用移动构造函数
```

`std::move` 本身不做任何操作，只是类型转换。实际的"移动"操作在移动构造函数中实现。

典型应用：高效 swap

```cpp
template <class T>
void swap(T& a, T& b) {
    T tmp(std::move(a));  // 移动构造
    a = std::move(b);     // 移动赋值
    b = std::move(tmp);   // 移动赋值
}
```

避免了三次不必要的拷贝操作！

==== 构造函数综合实例

写出以下代码的运行结果：

```cpp
#include <iostream>
class Test {
public:
    Test() {
        printf("Test()\n");
    } //默认构造函数
    ~Test() {
        printf("~Test()\n");
    } //析构函数
    Test(const Test &con) {
        printf("Test(const Test &con)\n");
    } //拷贝构造函数
    Test(Test &&con) {
        printf("Test(Test &&con)\n");
    } //移动构造函数
};
Test func(Test a) {
    return Test();
}
int main() {
    Test a;
    Test b = func(a);
    return 0;
}
```

编译指令：`g++ test.cpp --std=c++11 -fno-elide-constructors`

#strong[答案分析：]用 (1+) 和 (1-) 这样的形式来对应类的构造和析构。

```text
Test()                  //(1+) 执行 Test a;
Test(const Test &con)   //(2+) Test b = func(a);
                        //     func(a)传参调用拷贝构造函数
Test()                  //(3+) return Test();
                        //     Test() 对应的构造函数
Test(Test &&con)        //(4+) return Test();
                        //     为了传值调用的移动构造函数
~Test()                 //(3-) return Test();
                        //     Test() 对应的析构函数
Test(Test &&con)        //(5+) Test b = func(a);
                        //     给 b 传值时调用的移动构造函数
~Test()                 //(4-) Test b = func(a);
                        //     完成赋值后 func(a) 返回值对应的析构函数
~Test()                 //(2-) Test b = func(a);
                        //     参数释放对应的析构函数
~Test()                 //(5-) 析构 b
~Test()                 //(1-) 析构 a
```

详细步骤解析：

#table(
  columns: (auto, 1fr, 1fr),
  align: left + horizon,
  stroke: 0.5pt,
  [*步骤*], [*代码*], [*说明*],
  [1], [`Test a;`], [构造 a，调用默认构造函数],
  [2], [`func(a)` 传参], [拷贝构造函数，将 a 拷贝给参数对象],
  [3], [`return Test();`], [构造临时对象，调用默认构造函数],
  [4], [`return Test();`], [移动构造函数，将临时对象移动给返回值],
  [5], [临时对象析构], [步骤3创建的临时对象析构],
  [6], [`Test b = ...`], [移动构造函数，将返回值移动给 b],
  [7], [返回值析构], [步骤4创建的返回值对象析构],
  [8], [参数对象析构], [步骤2创建的参数对象析构],
  [9], [`main` 结束], [析构 b，然后析构 a],
)

#strong[关键点：]
+ 函数参数按值传递时，会调用拷贝构造函数
+ 函数返回临时对象时，会调用移动构造函数（如果有定义）
+ 析构顺序与构造顺序相反（栈的 LIFO 特性）

*多选题*

`Test` 类中显式声明了三类构造函数：

- *普通构造函数*：`Test(int val)`
- *移动构造函数*：`Test(Test&& t)`
- *拷贝构造函数*：`Test(const Test& t)`

现给出一段测试代码，*下列描述错误的是*：
```cpp
Test F(Test&& a){
    Test b = a;        // (2)
    const Test& c = b; // (3)
    return c;          // (4)
}
int main(){
    Test A = F(1); // (1)
    return 0;
}
```

选项：

- *A*：(1)处将 1 传入 F 时会调用普通构造函数 `Test(int val)` 以构建临时对象。
- *B*：(2)处调用移动构造函数。
- *C*：(3)处调用拷贝构造函数。
- *D*：(4)处返回局部变量的引用，可能会为程序带来潜在的风险。

*答案：BCD*

*(1) `Test A = F(1);` — 选项 A（正确描述）*

`F` 的参数类型为 `Test&&`，传入整数字面量 `1` 时，编译器需要先隐式构造一个 `Test` 类型的临时对象，因此会调用 `Test(int val)` 普通构造函数，再将该临时对象绑定到右值引用参数 `a`。

#block(fill: luma(235), inset: 8pt, radius: 4pt)[
  ✅ A 描述*正确*
]

*(2) `Test b = a;` — 选项 B（错误描述）*

关键点：`a` 的类型虽然是 `Test&&`，但*具名的右值引用在函数体内是左值*（named rvalue reference is lvalue）。因此 `Test b = a` 匹配 `Test(const Test& t)`，调用的是*拷贝构造函数*，而非移动构造函数。若想触发移动构造，应写：
```cpp
Test b = std::move(a);
```

#block(fill: luma(235), inset: 8pt, radius: 4pt)[
  ❌ B 描述*错误*：实际调用的是拷贝构造函数
]

*(3) `const Test& c = b;` — 选项 C（错误描述）*

此处仅将 `c` 绑定为 `b` 的 `const` 引用，*不构造任何新对象*，不调用任何构造函数。

#block(fill: luma(235), inset: 8pt, radius: 4pt)[
  ❌ C 描述*错误*：没有调用任何构造函数
]

*(4) `return c;` — 选项 D（错误描述）*

函数返回类型是 `Test`（按值返回），而非 `Test&`。`return c` 会以 `c` 为源*拷贝构造*一个新的返回值对象，返回的是值副本，不是对局部变量的引用，不存在悬空引用风险。

#block(fill: luma(235), inset: 8pt, radius: 4pt)[
  ❌ D 描述*错误*：返回的是值，不是引用，无悬空风险
]

=== 十、拷贝赋值运算符与移动赋值运算符

==== 拷贝赋值运算符

已定义的对象之间相互赋值，通过调用对象的"拷贝赋值运算符函数"来实现：

```cpp
ClassName& operator= (const ClassName& right) {
    if (this != &right) {  // 避免自己赋值给自己
        // 将right对象中的内容拷贝到当前对象中...
    }
    return *this;
}
```

*注意区分下面两种代码：*
```cpp
ClassName a;
ClassName b;
a = b;       // 赋值运算符：a 和 b 都已存在
ClassName a = b;  // 拷贝构造函数：a 还不存在
```

==== 拷贝赋值运算符实例

```cpp
class Test {
public:
    int *buf;
    Test() : buf(new int[10]) {}
    ~Test() { if (buf) delete[] buf; }

    Test& operator= (const Test& right) {
        if (this == &right)
            cout << "same obj!\n";
        else {
            for(int i=0; i<10; i++)
                buf[i] = right.buf[i];  // 拷贝数据
            cout << "operator=(const Test&) called.\n";
        }
        return *this;
    }
};
```

#strong[重要规则：]赋值重载函数必须是类的*非静态成员函数*（non-static member function），不能是友元函数。

==== 移动赋值运算符

和移动构造函数原理类似，直接"偷走"资源的指针：

```cpp
Test& operator= (Test&& right) {
    if (this == &right)
        cout << "same obj!\n";
    else {
        this->buf = right.buf;  // 直接赋值地址
        right.buf = nullptr;    // 置空，防止重复释放
        cout << "operator=(Test&&) called.\n";
    }
    return *this;
}
```

配合 `std::move` 实现高效 swap：

```cpp
template <class T>
void swap(T& a, T& b) {
    T tmp(std::move(a));  // 第一行调用移动构造函数
    a = std::move(b);     // std::move 的结果为右值引用
    b = std::move(tmp);   // 后两行均调用移动赋值运算符
}
```

==== 拷贝/移动赋值运算符的调用时机

#strong[判断依据：引用的绑定规则]

+ 拷贝赋值运算符的形参类型为 `const ClassName&`（常量左值引用），可以绑定：常量左值、左值、右值
+ 移动赋值运算符的形参类型为 `ClassName&&`（右值引用），可以绑定：右值
+ *优先级*：当赋值运算符右侧为右值时，优先匹配右值引用参数的函数

#table(
  columns: (1fr, 1fr, 1fr),
  align: center + horizon,
  stroke: 0.5pt,
  [*场景*], [*调用的运算符*], [*原因*],
  [`a = b`（b 是左值）], [拷贝赋值运算符], [左值绑定 `const &`],
  [`a = std::move(b)`], [移动赋值运算符], [右值绑定 `&&`],
  [`a = func()`（返回临时对象）], [移动赋值运算符], [右值绑定 `&&`],
  [`a = Test()`], [移动赋值运算符], [临时对象是右值],
)

==== 编译器自动合成的函数/运算符

类中特殊的成员函数/运算符，即使用户不显式定义，编译器也会根据需要自动合成：

#table(
  columns: (auto, 1fr),
  align: left + horizon,
  stroke: 0.5pt,
  [*类型*], [*说明*],
  [默认构造函数], [无参构造函数],
  [拷贝构造函数], [const ClassName& 参数],
  [移动构造函数], [ClassName&& 参数（C++11起）],
  [拷贝赋值运算符], [operator=(const ClassName&)],
  [移动赋值运算符], [operator=(ClassName&&)（C++11起）],
  [析构函数], [`~ClassName()`],
)

#strong[注意：]如果你定义了任何构造函数，编译器就不会自动生成默认构造函数了！但拷贝/移动构造函数和赋值运算符仍会自动生成（除非显式删除）。

=== 十一、类型转换

==== 类型转换概述

当编译器发现表达式和函数调用所需的数据类型和实际类型不同时，便会进行自动类型转换。

```cpp
void print(int d) { }
int main() {
    print(3.5);  // double -> int，自动类型转换
    print('c');  // char -> int，自动类型转换
    return 0;
}
```

自动类型转换可通过两种方式实现：
+ 定义*类型转换运算符*（在源类中）
+ 定义*类型转换构造函数*（在目标类中）

==== 方法一：类型转换运算符

在*源类*中定义"目标类型转换运算符"：

```cpp
#include <iostream>
using namespace std;
class Dst {  // 目标类 Destination
public:
    Dst() { cout << "Dst::Dst()" << endl; }
};
class Src {  // 源类 Source
public:
    Src() { cout << "Src::Src()" << endl; }
    operator Dst() const {
        cout << "Src::operator Dst() called" << endl;
        return Dst();
    }
};
```

#strong[语法说明：]
+ `operator 目标类型()` 是特殊的成员函数
+ *不需要指定返回类型*，因为 `operator Dst()` 已经指明了返回 `Dst`
+ 必须是成员函数，不能是友元

==== 方法二：类型转换构造函数

在*目标类*中定义"源类对象作参数的构造函数"：

```cpp
#include <iostream>
using namespace std;
class Src;  // 前置类型声明，因为在 Dst 中要用到 Src 类
class Dst {
public:
    Dst() { cout << "Dst::Dst()" << endl; }
    Dst(const Src& s) {  // 源类对象作参数的构造函数
        cout << "Dst::Dst(const Src&)" << endl;
    }
};
class Src {
public:
    Src() { cout << "Src::Src()" << endl; }
};
```

==== 两种方法的使用

两种方法任选一种即可：

```cpp
void Transform(Dst d) { }
int main() {
    Src s;
    Dst d1(s);     // 显式初始化，两种方法都支持
    Dst d2 = s;    // 隐式转换，两种方法都支持
    Transform(s);  // 隐式转换，两种方法都支持
    return 0;
}
```

#rect(
  fill: rgb("#fff0f0"),
  stroke: red,
  inset: 10pt,
  radius: 4pt,
  width: 100%
)[
  *警告：*两种自动类型转换的方法*不能同时使用*，否则会产生二义性，编译器不知道选择哪个。使用时任选其中一种！
]

==== 类型转换运算符：错误示例

```cpp
class SmallInt;
operator int(SmallInt&);  // 错误：不是成员函数
class SmallInt {
public:
    int operator int() const;    // 错误：不能指定返回类型
    operator int(int = 0) const; // 错误：参数列表不为空
    operator int*() const { return 42; } // 错误：42不是合法指针
};
```

#strong[错误分析：]
+ 类型转换运算符必须是成员函数，不能是全局函数
+ 不能指定返回类型（`operator int()` 已经隐含返回 `int`）
+ 参数列表必须为空（转换运算符不接收额外参数）
+ 必须返回正确类型的值

正确写法：
```cpp
class SmallInt {
public:
    operator int() const { return val; }  // 正确
    operator int*() const { return &val; } // 正确
private:
    int val;
};
```

==== 类型转换实例

```cpp
class SmallInt {
public:
    // 构造函数：从 int 转换为 SmallInt
    SmallInt(int i=0): val(i) {
        cout << "SmallInt_Init" << endl;
    }
    // 转换运算符：从 SmallInt 转换为 int
    operator int() const {
        cout << "Int_Transform" << endl;
        return val;
    }
    void print() { cout << val << endl; }
private:
    size_t val;
};
int main() {
    SmallInt si;
    si = 4.10;
    si = si + 3;
    si.print();
    return 0;
}
```

输出：
```text
SmallInt_Init      // SmallInt si，调用构造函数
SmallInt_Init      // si = 4.10，double->int->SmallInt
Int_Transform      // si + 3，SmallInt->int
SmallInt_Init      // si = si + 3，int->SmallInt
7                  // si.print()
```

#strong[详细执行流程：]

#table(
  columns: (auto, 1fr, 1fr),
  align: left + horizon,
  stroke: 0.5pt,
  [*语句*], [*转换过程*], [*输出*],
  [`SmallInt si;`], [默认构造函数，`val=0`], [`SmallInt_Init`],
  [`si = 4.10;`], [`4.10`→`4`(double→int)→`SmallInt(4)`→赋值], [`SmallInt_Init`],
  [`si + 3`], [`si`→`int`（调用 `operator int()`）→ `7`], [`Int_Transform`],
  [`si = 7`], [`7`→`SmallInt(7)`→赋值], [`SmallInt_Init`],
  [`si.print()`], [输出 `val`], [`7`],
)

#rect(
  fill: rgb("#f0f8ff"),
  stroke: blue,
  inset: 10pt,
  radius: 4pt,
  width: 100%
)[
  *思考题解答：为什么 `si = si + 3` 不是把 `3` 转换为 `SmallInt` 再加呢？*

  因为 `operator+` 是内置的整数加法运算符，不是 `SmallInt` 的成员函数！

  执行过程：
  + 编译器看到 `si + 3`，首先检查 `SmallInt` 是否有 `operator+`
  + 没有找到，于是尝试将 `si` 转换为能和 `int` 相加的类型
  + 发现 `operator int()`，将 `si` 转换为 `int`，得到 `0 + 3 = 3`（初始 `val=0`）
  + 然后赋值 `si = 3`，调用构造函数将 `3` 转换为 `SmallInt`

  如果想让 `3` 转换为 `SmallInt` 再加，需要重载 `operator+`：
  ```cpp
  SmallInt operator+(const SmallInt& other) const {
      return SmallInt(val + other.val);
  }
  ```
  这样 `si + 3` 就会：`3`→`SmallInt(3)`→`si.operator+(SmallInt(3))`
]

==== 禁止自动类型转换

如果用 `explicit` 修饰类型转换运算符或类型转换构造函数，则相应的类型转换必须*显式*进行：

```cpp
// 方法一：explicit 修饰转换运算符
explicit operator Dst() const;

// 方法二：explicit 修饰构造函数
explicit Dst(const Src& s);
```

使用 `explicit` 后：

```cpp
int main() {
    Src s;
    Dst d1(s);               // ✓ 可以执行，被认为是显式初始化
    // Dst d2 = s;           // ✗ 错误，隐式转换被禁止
    // Transform(s);         // ✗ 错误，隐式转换被禁止
    Dst d2 = static_cast<Dst>(s);  // ✓ 显式转换
    Transform(static_cast<Dst>(s)); // ✓ 显式转换
    return 0;
}
```

==== 强制类型转换

C++ 提供四种强制类型转换：

#table(
  columns: (auto, 1fr, 1fr),
  align: left + horizon,
  stroke: 0.5pt,
  [*关键字*], [*功能*], [*应用场景*],
  [`const_cast`], [去除 `const` 或 `volatile` 属性], [修改常量指针的指向内容],
  [`static_cast`], [静态类型转换，类似 C 风格], [基本类型转换、void*转其他指针*],
  [`dynamic_cast`], [动态类型转换（运行时检查）], [多态类型间的安全下行转换],
  [`reinterpret_cast`], [重新解释类型（不进行二进制转换）], [指针与整数互转、不相关指针互转],
)

#strong[详细说明：]

+ `const_cast`：唯一能去除常量性的转换
  ```cpp
  const int* p = &a;
  int* q = const_cast<int*>(p);  // 去除 const
  ```

+ `static_cast`：最常用的转换，编译时检查
  ```cpp
  double d = 3.14;
  int i = static_cast<int>(d);   // double -> int
  void* p = malloc(100);
  int* q = static_cast<int*>(p); // void* -> int*
  ```

+ `dynamic_cast`：安全的下行转换，需要多态支持（有虚函数）
  ```cpp
  Base* b = new Derived;
  Derived* d = dynamic_cast<Derived*>(b);  // 安全转换
  // 如果转换失败，指针返回 nullptr，引用抛出异常
  ```

+ `reinterpret_cast`：最危险的转换，直接重新解释内存
  ```cpp
  int* p = new int(42);
  long addr = reinterpret_cast<long>(p);  // 指针 -> 整数
  int* q = reinterpret_cast<int*>(addr);  // 整数 -> 指针
  ```

==== 强制类型转换示例

```cpp
int main() {
    Src s;
    Dst d1(s);                         // 显式初始化
    Dst d2 = static_cast<Dst>(s);      // 显式转换
    Transform(static_cast<Dst>(s));    // 显式转换
    return 0;
}
```

== 陆 组合与继承 #datetime(day:7,month:4,year:2026).display()
<陆-组合与继承-2026.4.7>

=== 一、对象(类)之间的关系

思考：这些是什么关系？
- 智能体：感知模块，思考模块，执行模块
- 智能体：科研智能体，编程智能体，写作智能体

+ *has-a*：感知，思考，执行模块是智能体的组成部分（"整体-部分"）
+ *is-a*：科研，编程，写作智能体是具有特殊能力的智能体（"一般-特殊"）

=== 二、组合

*has-a*：如果对象 a 是对象 b 的一个组成部分，则称 b 为 a 的整体对象，a 为 b 的部分对象。并把 b 和 a 之间的关系，称为"整体－部分"关系（也可称为"组合"或"has-a"关系）。

程序设计反映对客观世界的认知习惯。

对象组合的两种实现方法：
+ 已有类的对象作为新类的*公有*数据成员，这样通过允许直接访问子对象而"提供"旧类接口
+ 已有类的对象作为新类的*私有*数据成员。新类可以调整旧类的对外接口，可以不使用旧类原有的接口（相当于对接口作了转换）

==== 对象组合示例

```cpp
#include <iostream>
#include <string>
using namespace std;
class Perception{
    string _prompt;
public:
    void set(const string& prompt){_prompt=prompt;}
};
class Action{
    string _prompt;
public:
    void set(const string& prompt){_prompt=prompt;}
};
class Agent{
private:
    Perception p;
public:
    Action a; // 公有成员，直接访问其接口
    void setPerception(const string& prompt){p.set(prompt);} // 提供私有成员的访问接口
};
int main(){
    Agent agent;
    string prompt = "Hello, World";
    agent.a.set(prompt);
    agent.setPerception(prompt);
    return 0;
}
```

==== 子对象构造

子对象构造时若需要参数，则应在当前类的构造函数的初始化列表中进行。若使用默认构造函数来构造子对象，则不用做任何处理。

*对象构造与析构函数的次序：*
+ 先完成子对象构造，再完成当前对象构造
+ 子对象构造的次序仅由在类中声明的次序所决定
+ 析构函数的次序与构造函数相反

==== 对象组合示例：构造与析构

```cpp
#include <iostream>
using namespace std;
class S1 { //Single1类别
    int ID;
public:
    S1(int id) : ID(id) { cout << "S1(int)" << endl; }
    ~S1() { cout << "~S1()" << endl; }
};
class S2 {//Single2类别
public:
    S2() { cout << "S2()" << endl; }
    ~S2() { cout << "~S2()" << endl; }
};
class C3 {//Composite3类别
    int num;
    S1 sub_obj1; // 构造函数带参数
    S2 sub_obj2; // 构造函数不带参数
public:
    C3() : num(0), sub_obj1(123) { cout << "C3()" << endl; }
    C3(int n) : num(n), sub_obj1(123) { cout << "C3(int)" << endl; }
    C3(int n, int k) : num(n), sub_obj1(k) { cout << "C3(int, int)" << endl; }
    ~C3() { cout << "~C3()" << endl; }
};
int main(){
    C3 a, b(1), c(2), d(3, 4);
    return 0;
}
```

==== 对象组合运行结果

```text
S1(int)
S2()
C3()
S1(int)
S2()
C3(int)
S1(int)
S2()
C3(int)
S1(int)
S2()
C3(int, int)
~C3()
~S2()
~S1()
~C3()
~S2()
~S1()
~C3()
~S2()
~S1()
~C3()
~S2()
~S1()
```

*晚构造，先析构！*

==== 隐式定义的拷贝构造与赋值运算

回忆：如果调用拷贝构造函数且没有给类显式定义拷贝构造函数，编译器将提供"隐式定义的拷贝构造函数"。该函数的功能为：
+ 递归调用所有子对象的拷贝构造函数
+ 对于基础类型，采用位拷贝
+ 赋值运算的默认操作类似

==== 对象组合示例：拷贝与赋值

```cpp
#include <iostream>
using namespace std;
class C1{
public:
    int i;
    C1(int n):i(n){}
    C1(const C1 &other) // 显式定义拷贝构造函数
    {i=other.i; cout << "C1(const C1 &other)" << endl;}
};
class C2{
public:
    int j;
    C2(int n):j(n){}
    C2& operator= (const C2& right){ // 显式定义赋值运算符
        if(this != &right){
            j = right.j;
            cout << "operator=(const C2&)" << endl;
        }
        return *this;
    }
};
```

```cpp
class C3{
public:
    C1 c1;
    C2 c2;
    C3():c1(0), c2(0){}
    C3(int i, int j):c1(i), c2(j){}
    void print(){cout << "c1.i = " << c1.i << " c2.j = " << c2.j << endl;}
};
int main(){
    C3 a(1, 2);
    C3 b(a); // C1执行显式定义的拷贝构造，C2执行隐式定义的拷贝构造
    cout << "b: ";
    b.print();
    cout << endl;
    C3 c;
    cout << "c: ";
    c.print();
    c = a; // C1执行隐式定义的拷贝赋值，C2执行显式定义的拷贝赋值
    cout << "c: ";
    c.print();
    return 0;
}
```

运行结果：
```text
C1(const C1 &other)
b: c1.i = 1 c2.j = 2
c: c1.i = 0 c2.j = 0
operator=(const C2&)
c: c1.i = 1 c2.j = 2
```

=== 三、继承

*is-a*："一般－特殊"结构，也称"分类结构"，是由一组具有"一般－特殊"关系的类所组成的结构。

+ 如果类 A 具有类 B 全部的属性和服务，而且具有自己特有的某些属性或服务，则称 A 为 B 的特殊类，B 为 A 的一般类。
+ 如果类 A 的全部对象都是类 B 的对象，而且类 B 中存在不属于类 A 的对象，则 A 是 B 的特殊类，B 为 A 的一般类。

C++ 使用继承来表达类间的"一般－特殊结构"。例如"编程智能体"继承"智能体"。

==== 基本概念

+ 被继承的已有类，被称为*基类*（base class），也称"父类"。
+ 通过继承得到的新类，被称为*派生类*（derived class），也称"子类"、"扩展类"。

常见的继承方式：
+ `class Derived : public Base { ... };` — 公有继承
+ `class Derived : [private] Base { .. };` — 私有继承（缺省）
+ `class Derived : protected Base { ... };` — 保护继承（很少使用）

==== 什么不能被继承？

+ *构造函数*：创建派生类对象时，必须调用派生类的构造函数，派生类构造函数调用基类的构造函数，以创建派生对象的基类部分。C++11 新增了继承构造函数的机制（使用 `using`），但默认不继承。
+ *析构函数*：释放对象时，先调用派生类析构函数，再调用基类析构函数。
+ *赋值运算符*：编译器不会继承基类的赋值运算符（参数为基类）；但会自动合成隐式定义的赋值运算符（参数为派生类），其功能为调用基类的赋值运算符。
+ *友元函数*：不是类成员，不能被继承。

==== 继承示例

```cpp
#include <iostream>
using namespace std;
class Base{
public:
    int k = 0;
    void f(){cout << "Base::f()" << endl;}
    Base & operator= (const Base &right){
        if(this != &right){
            k = right.k;
            cout << "operator= (const Base &right)" << endl;
        }
        return *this;
    }
};
class Derive: public Base{};
int main(){
    Derive d, d2;
    cout << d.k << endl; //Base数据成员被继承
    d.f(); //Base::f()被继承
    Base e;
    //d = e; //编译错误，Base的赋值运算符不被继承
    d = d2; //调用隐式定义的赋值运算符
    return 0;
}
```

运行结果：
```text
0
Base::f()
operator= (const Base &right)
```

==== 派生类对象的构造与析构过程

基类中的数据成员，通过继承成为派生类对象的一部分，需要在构造派生类对象的过程中调用基类构造函数来正确初始化。

+ 若没有显式调用，则编译器会自动调用基类的默认构造函数。
+ 若想要显式调用，则只能在派生类构造函数的*初始化成员列表*中进行，既可以调用基类中不带参数的默认构造函数，也可以调用合适的带参数的其他构造函数。

*先执行基类的构造函数来初始化继承来的数据，再执行派生类的构造函数。*

对象析构时，*先执行派生类析构函数，再执行由编译器自动调用的基类的析构函数。*

==== 调用基类构造函数：隐式调用默认构造

```cpp
class Base
{
    int data;
public:
    Base() : data(0) { cout << "Base::Base(" << data << ")\n"; }
    Base(int i) : data(i) { cout << "Base::Base(" << data << ")\n"; }
};
class Derive : public Base {
public:
    Derive() { cout << "Derive::Derive()" << endl; }
    // 无显式调用基类构造函数，则调用基类默认构造函数
};
int main() {
    Derive obj;
    return 0;
}
```

运行结果：
```text
Base::Base(0)
Derive::Derive()
```

==== 调用基类构造函数：显式调用

若想要显式调用，则只能在派生类构造函数的初始化成员列表中进行。

```cpp
class Base
{
    int data;
public:
    Base() : data(0) { cout << "Base::Base(" << data << ")\n"; }
    Base(int i) : data(i) { cout << "Base::Base(" << data << ")\n"; }
};
class Derive : public Base {
public:
    Derive(int i) : Base(i) { cout << "Derive::Derive()" << endl; }
    // 显式调用基类构造函数
};
int main() {
    Derive obj(356);
    return 0;
}
```

运行结果：
```text
Base::Base(356)
Derive::Derive()
```

==== 继承基类构造函数（using）

在派生类中使用 `using Base::Base;` 来继承基类构造函数，相当于给派生类"定义"了相应参数的构造函数。

```cpp
class Base
{
    int data;
public:
    Base(int i) : data(i) { cout << "Base::Base(" << i << ")\n"; }
};
class Derive : public Base {
public:
    using Base::Base; //相当于 Derive(int i):Base(i){};
};
int main() {
    Derive obj(356);
    return 0;
}
```

运行结果：
```text
Base::Base(356)
```

===== 继承基类构造函数（多个构造函数）

当基类存在多个构造函数时，使用 `using` 会给派生类自动构造多个相应的构造函数。

```cpp
class Base
{
    int data;
public:
    Base(int i) : data(i) { cout << "Base::Base(" << i << ")\n"; }
    Base(int i, int j)
    { cout << "Base::Base(" << i << "," << j << ")\n";}
};
class Derive : public Base {
public:
    using Base::Base; //相当于 Derive(int i):Base(i){};
                     //加上 Derive(int i, int j):Base(i，j){};
};
int main() {
    Derive obj1(356);
    Derive obj2(356, 789);
    return 0;
}
```

运行结果：
```text
Base::Base(356)
Base::Base(356,789)
```

===== 继承基类构造函数（注意事项）

+ 如果基类的某个构造函数被声明为私有成员函数，则不能在派生类中声明继承该构造函数。
+ 如果派生类使用了继承构造函数，编译器就不会再为派生类生成隐式定义的默认构造函数。

==== 如何选择继承方式？

===== public 继承

+ 基类中公有成员仍能在派生类中保持公有。原接口可沿用。最常用。
+ is-a：基类对象能使用的地方，派生类对象也能使用。

===== private 继承

+ is-implementing-in-terms-of（照此实现）：用基类接口实现派生类功能。移除了 is-a 关系。
+ 通常不使用，用组合替代。可用于隐藏/公开基类的部分接口。公开方法：`using` 关键字。

==== 成员访问权限

+ 基类中的*私有成员*，不允许在派生类成员函数中访问，也不允许派生类的对象访问它们。真正体现"基类私有"，对派生类也不开放其权限！
+ 基类中的*公有成员*：
  - 允许在派生类成员函数中被访问
  - 若是使用 public 继承方式，则成为派生类公有成员，可以被派生类的对象访问
  - 若是使用 private/protected 继承方式，则成为派生类私有/保护成员，不能被派生类的对象访问。若想让某成员能被派生类的对象访问，可在派生类 public 部分用关键字 `using` 声明它的名字
+ 基类中的*保护成员*：
  - 保护成员允许在派生类成员函数中被访问，但不能被外部函数访问

===== 公有继承：基类公有成员的访问

```cpp
#include <iostream>
using namespace std;
class Base {
public:
    void baseFunc() { cout << "in Base::baseFunc()..." << endl; }
};
class Derive1: public Base {}; // public继承
int main() {
    Derive1 obj1;
    cout << "calling obj1.baseFunc()..." << endl;
    obj1.baseFunc(); // 基类接口成为派生类接口的一部分，派生类对象可调用
    return 0;
}
```

===== 私有继承：基类公有成员的访问

```cpp
#include <iostream>
using namespace std;
class Base {
public:
    void baseFunc() { cout << "in Base::baseFunc()..." << endl; }
};
class Derive2: private Base {
// 私有继承，is-implementing-in-terms-of：用基类接口实现派生类功能
public:
    void deriveFunc() {
        cout << "in Derive2::deriveFunc(), calling Base::baseFunc()..." << endl;
        baseFunc(); // 私有继承时，基类接口在派生类成员函数中可以使用
    }
};
int main() {
    Derive2 obj2;
    cout << "calling obj2.deriveFunc()..." << endl;
    obj2.deriveFunc();
    //obj2.baseFunc(); ERROR: 基类接口不允许从派生类对象调用
    return 0;
}
```

===== 私有继承：用 using 打开基类公有成员的访问权限

```cpp
#include <iostream>
using namespace std;
class Base {
public:
    void baseFunc() { cout << "in Base::baseFunc()..." << endl; }
};
class Derive3: private Base {
public:
    using Base::baseFunc; // 私有继承时，在派生类public部分声明基类成员名字
};
int main() {
    Derive3 obj3;
    cout << "calling obj3.baseFunc()..." << endl;
    obj3.baseFunc(); // 基类接口在派生类public部分声明，则派生类对象可调用
    return 0;
}
```

===== 私有继承：基类私有、保护成员访问

```cpp
#include <iostream>
using namespace std;
class Base{
private:
    int a{0};
protected:
    int b{0};
};
class Derive : private Base{
public:
    void getA(){cout<<a<<endl;} // 编译错误，不可访问基类中私有成员
    void getB(){cout<<b<<endl;} // 可以访问基类中保护成员
};
int main()
{
    Derive d;
    d.getB();
    //cout<<d.b; // 编译错误，派生类对象不可访问基类中保护成员
    return 0;
}
```

```cpp
#include <iostream>
using namespace std;
class Base {
private:
    int data{0};
public:
    int getData(){ return data;}
    void setData(int i){ data=i;}
};
class Derive1 : private Base {
public:
    using Base::getData;
};
int main() {
    Derive1 d1;
    cout<<d1.getData();
    //d1.setData(10); // 隐藏了基类的setData函数，不可访问
    //Base& b = d1; // 不允许私有继承的向上转换
    //b.setData(10); // 否则可以绕过D1，调用基类的setData函数
    return 0;
}
```

===== 基类成员访问权限与三种继承方式

+ *public 继承*：基类的公有成员、保护成员、私有成员作为派生类的成员时，都保持原有的状态。
+ *private 继承*：基类的公有成员、保护成员、私有成员作为派生类的成员时，都作为私有成员。
+ *protected 继承*：基类的公有成员、保护成员作为派生类的成员时，都成为保护成员，基类的私有成员仍然是私有的。

继承权限表：

// 派生类成员函数能否访问基类成员
#table(
  columns: (auto, 1fr, 1fr, 1fr),
  align: center + horizon,
  stroke: 0.5pt,
  table.cell(colspan: 4)[*派生类成员函数能否访问基类成员*],
  [], [public 继承], [private 继承], [protected 继承],
  [基类 public 成员], [✓], [✓], [✓],
  [基类 private 成员], [✗], [✗], [✗],
  [基类 protected 成员], [✓], [✓], [✓],
)

// 基类成员在派生类中的访问属性
#table(
  columns: (auto, 1fr, 1fr, 1fr),
  align: center + horizon,
  stroke: 0.5pt,
  table.cell(colspan: 4)[*基类成员在派生类中的成员类型 / 派生类对象能否访问*],
  [], [public 继承], [private 继承], [protected 继承],
  [基类 public 成员], [public / ✓], [private / ✗], [protected / ✗],
  [基类 private 成员], [private / ✗], [private / ✗], [private / ✗],
  [基类 protected 成员], [protected / ✗], [private / ✗], [protected / ✗],
)

*类似集合交运算：成员类型与继承类型之间取交。*Order: public > protected > private。

==== 组合与继承的对比

*优点：*支持增量开发。允许引入新代码而不影响已有代码正确性。

*相似：*
+ 实现代码重用
+ 将子对象引入新类
+ 使用构造函数的初始化成员列表初始化

*不同：*
+ 组合：
  - 嵌入一个对象以实现新类的功能
  - has-a 关系
+ 继承：
  - 沿用已存在的类提供的接口
  - public 继承：is-a
  - private 继承：is-implementing-in-terms-of

===== 组合示例：has-a

```cpp
#include <iostream>
using namespace std;
class Perception{
public:
    void init(){ cout<<"Perception::init"<<endl; }
};
class Action{
public:
    void init(){ cout<<"Action::init"<<endl; }
    void stop(){}
};
class Agent{
public:
    Perception perception;
    Action action;
};
int main()
{
    Agent agent;
    agent.perception.init();
    agent.action.init();
    return 0;
}
```

运行结果：
```text
Perception::init
Action::init
```

===== 继承示例：is-a

```cpp
#include <iostream>
using namespace std;
class Agent{
public:
    void init(){cout<<"Agent init"<<endl;}
    void act(){cout<<"Agent act"<<endl; }
};
class Coder: public Agent{
public:
    void act(){cout<<"Coder act"<<endl;}
};
int main()
{
    Coder coder;
    coder.init();
    coder.act();
    return 0;
}
```

运行结果：
```text
Agent init
Coder act
```

=== 四、重写隐藏与重载

==== 重载（overload）

+ 目的：提供同名函数的不同实现，属于静态多态。
+ 函数名必须相同，函数参数必须不同，作用域相同（如位于同一个类中；或同名全局函数）。

==== 重写隐藏（redefining）

+ 目的：在派生类中重新定义基类函数，实现派生类的特殊功能。
+ *屏蔽了基类的所有其它同名函数。*
+ 函数名必须相同，函数参数可以不同。

重写隐藏发生时，基类中该成员函数的其他重载函数都将被屏蔽掉，不能提供给派生类对象使用。

可以在派生类中通过 `using 类名::成员函数名;` 在派生类中"恢复"指定的基类成员函数（即去掉屏蔽），使之重新可用。

==== 函数重写隐藏示例

```cpp
#include <iostream>
using namespace std;
class T {};
class Base {
public:
    void f() { cout << "B::f()\n"; }
    void f(int i) { cout << "Base::f(" << i << ")\n"; } // 重载
    void f(double d) { cout << "Base::f(" << d << ")\n"; } // 重载
    void f(T) { cout << "Base::f(T)\n"; } // 重载
};
class Derive : public Base {
public:
    void f(int i) { cout << "Derive::f(" << i << ")\n"; } // 重写隐藏
};
int main() {
    Derive d;
    d.f(10);
    d.f(4.9); // 编译警告。执行自动类型转换。
    //d.f(); // 被屏蔽，编译错误
    //d.f(T()); // 被屏蔽，编译错误
    return 0;
}
```

运行结果：
```text
Derive::f(10)
Derive::f(4)
```
$4.9 -> 4$：自动类型转换，因为基类的 `f(double)` 被屏蔽了，只能匹配派生类的 `f(int)`。

==== 恢复基类成员函数示例

使用 `using 基类名::函数名;` 恢复基类函数：

```cpp
#include <iostream>
using namespace std;
class T {};
class Base {
public:
    void f() { cout << "Base::f()\n"; }
    void f(int i) { cout << "Base::f(" << i << ")\n"; }
    void f(double d) { cout << "Base::f(" << d << ")\n"; }
    void f(T) { cout << "Base::f(T)\n"; }
};
class Derive : public Base {
public:
    using Base::f;
    void f(int i) { cout << "Derive::f(" << i << ")\n"; }
};
int main() {
    Derive d;
    d.f(10);
    d.f(4.9);
    d.f();
    d.f(T());
    return 0;
}
```

运行结果：
```text
Derive::f(10)
Base::f(4.9)
Base::f()
Base::f(T)
```

==== using 关键字总结

`using` 关键字可用于：
+ 继承基类构造函数：`using Base::Base;`
+ 恢复被屏蔽的基类成员函数：`using Base::f;`
+ 指示命名空间：`using namespace std;`
+ 将另一个命名空间的成员引入当前命名空间：`using std::cout;`
+ 定义类型别名：`using a = int;`

=== 五、多重继承

派生类同时继承多个基类。

应用场景：
```cpp
class File{};
class InputFile: public File{};
class OutputFile: public File{};
class IOFile: public InputFile, public OutputFile{};
```

==== 多重继承的问题

+ *数据存储*：如果派生类 D 继承的两个基类 A, B 是同一基类 Base 的不同继承，则 A, B 中继承自 Base 的数据成员会在 D 有*两份独立的副本*，可能带来数据冗余。
+ *二义性*：如果派生类 D 继承的两个基类 A, B 有同名成员 a，则访问 D 中 a 时，编译器无法判断要访问的哪一个基类成员。

==== 多重继承示例

```cpp
#include <iostream>
using namespace std;
class Base {
public:
    int a{0};
};
class MiddleA : public Base {
public:
    void addA() { cout << "a=" << ++a << endl; };
    void bar() { cout << "A::bar" << endl; };
};
class MiddleB : public Base {
public:
    void addB() { cout << "a=" << ++a << endl; };
    void bar() { cout << "B::bar" << endl; };
};
class Derive : public MiddleA, public MiddleB{
};
```

MiddleA 和 MiddleB 各有一份独立的 `Base::a`，Derive 继承了两份。

```cpp
int main() {
    Derive d;
    d.addA(); // 输出 a=1
    d.addB(); // 仍然输出 a=1（另一份副本）
    d.addB(); // 输出 a=2
    //cout << d.a; // 编译错误，MiddleA和MiddleB都有成员a
    cout << d.MiddleA::a << endl; // 输出A中的成员a的值 1
    //d.bar(); // 编译错误，MiddleA和MiddleB都有成员函数bar
    cout << d.MiddleB::a << endl; // 输出B中的成员a的值 2
    return 0;
}
```

*解决二义性：*用 `类名::成员名` 显式指定访问哪个基类的成员。

=== 六、课后练习

一家工厂生产飞机、汽车和摩托车。一架飞机需要三个轮子和两个机翼；一辆汽车需要四个轮子；一辆摩托车需要两个轮子。

这些交通工具都具有一个 `run` 函数，其中汽车和摩托车调用时输出 "I am running"，但是飞机调用时输出 "I am running and flying"。

编写以下几个类：`Plane`，`Motor`，`Car`，`Wing`，`Wheel`，`Vehicle`（交通工具），设计合理的继承、组合关系以及使用函数的继承与重写实现 `add_wing`，`add_wheel`，`finished` 以及 `run` 函数。

测试代码：

```cpp
#include <iostream>
#include "Car.h"
#include "Plane.h"
#include "Motor.h"
#include "Wing.h"
#include "Wheel.h"
int main() {
    int m;
    std::cin >> m;
    Plane planes = new Plane[100];
    Car cars = new Car[100];
    Motor motors = new Motor[100];
    int i_p = 0, i_c = 0, i_m = 0;
    for (int i = 0; i < m; ++i) {
        int op;
        std::cin >> op;
        if (op == 0) {// plane
            int part;
            std::cin >> part;
            if (part == 0) planes[i_p].add_wing(new Wing());
            else planes[i_p].add_wheel(new Wheel());
            if (planes[i_p].finished()) planes[i_p++].run();
        }
        else if (op == 1) { // car
            cars[i_c].add_wheel(new Wheel());
            if (cars[i_c].finished()) cars[i_c++].run();
        }
        else { // motor
            motors[i_m].add_wheel(new Wheel());
            if (motors[i_m].finished())motors[i_m++].run();
        }
    }
    return 0;
}
```

输入：
```text
0 0
0 0
0 1
0 1
0 1
1
1
2
2
1
1
```

输出：
```text
I am running and flying
I am running
I am running
```

== 柒 虚函数 #datetime(day:14,month:4,year:2026).display()
<柒-虚函数-2026.4.14>

=== 一、向上类型转换

派生类对象/引用/指针转换成基类对象/引用/指针，称为*向上类型转换*。只对public继承有效，对private、protected继承无效。

向上类型转换可以由编译器自动完成，是一种隐式类型转换。凡是接受基类对象/引用/指针的地方（如函数参数），都可以使用派生类对象/引用/指针。

```cpp
class Base {
public:
    void print() { cout << "Base::print()" << endl; }
};
class Derive : public Base {
public:
    void print() { cout << "Derive::print()" << endl; }
};
void fun(Base obj) { obj.print(); }
int main() {
    Derive d;
    d.print();    // Derive::print()
    fun(d);       // Base::print() —— 早绑定！
    return 0;
}
```

=== 二、对象切片

当派生类的*对象*（不是指针或引用）被转换为基类的对象时，派生类的对象被*切片*为对应基类的子对象。派生类新定义的数据和方法会丢失。

```cpp
class Pet {
public: int att_i;
    Pet(int x=0): att_i(x) {};
};
class Dog: public Pet {
public: int att_j;
    Dog(int x=0, int y=0): Pet(x), att_j(y) {}
};
int main() {
    Pet p(1);
    Dog g(2,3);
    cout << p.att_i << endl;        // 1
    cout << g.att_i << " " << g.att_j << endl; // 2 3
    p = g; // 对象切片，只赋值基类数据
    cout << p.att_i << endl;        // 2
    //cout << p.att_j << endl;      // 编译错误，没有该参数
    return 0;
}
```

*对象切片两种情况：*函数传参（值传递）和赋值操作。都会丢失派生类新增的数据和方法。

=== 三、指针（引用）的向上转换

当派生类的指针（引用）被转换为基类指针（引用）时，*不会创建新的对象*，但只保留基类的接口。引用向上转换后修改基类存在的数据，会影响派生类。

```cpp
Dog g(2,3);
Pet& p = g;       // 引用向上转换
cout << p.att_i << endl;  // 2
p.att_i = 1;              // 修改基类存在的数据
cout << g.att_i << " " << g.att_j << endl; // 1 3，影响派生类
```

但引用向上转换后，函数调用仍是*早绑定*：

```cpp
class Instrument {
public:
    void play() { cout << "Instrument::play" << endl; }
};
class Wind : public Instrument {
public:
    void play() { cout << "Wind::play" << endl; }
};
void tune(Instrument& i) { i.play(); }
int main() {
    Wind flute;
    tune(flute);    // Instrument::play —— 早绑定！
    Instrument &inst = flute;
    inst.play();    // Instrument::play —— 早绑定！
    return 0;
}
```

=== 四、函数调用捆绑

把函数体与函数调用相联系称为*捆绑*(binding)。

+ *早捆绑*(early binding)：捆绑在程序运行之前（由编译器和连接器）完成。上面的程序中 `tune` 里的 `i.play()` 与 `Instrument::play()` 绑定就是早捆绑。
+ *晚捆绑*(late binding)：捆绑根据对象的实际类型，发生在程序运行时，又称动态捆绑或运行时捆绑。*晚捆绑只对类中的虚函数起作用，使用 `virtual` 关键字声明。*

=== 五、虚函数和虚函数表

对于被派生类重新定义的成员函数，若它在基类中被声明为*虚函数*，则通过基类指针或引用调用该成员函数时，编译器将根据所指（或引用）对象的实际类型决定调用哪个函数。

```cpp
class Instrument {
public:
    virtual void play() { cout << "Instrument::play" << endl; }
};
class Wind : public Instrument {
public:
    void play() { cout << "Wind::play" << endl; } // 重写覆盖
};
void tune(Instrument& ins) { ins.play(); }
int main() {
    Wind flute;
    tune(flute); // Wind::play —— 晚绑定！
    return 0;
}
```

*晚绑定只对指针和引用有效！*值传递会产生对象切片，仍是早绑定：

```cpp
void tune(Instrument ins) { ins.play(); } // 值传递，对象切片，早绑定
```

==== 虚函数表（VTABLE）

+ *虚函数表*(VTABLE)：每个包含虚函数的类用于存储虚函数地址的表（唯一性，即使没有重写虚函数也有自己的表）。
+ *虚函数指针*(VPTR)：每个包含虚函数的类对象中，编译器秘密放一个指针，指向这个类的VTABLE。
+ 编译期间：建立VTABLE，记录每个类或其基类中所有已声明的虚函数入口地址。
+ 运行期间：建立VPTR，在构造函数中发生，指向相应的VTABLE。

```cpp
class B{
    int i; float j;
public:
    virtual void fun1() { cout << "B::fun1()" << endl; }
    virtual void fun2() { cout << "B::fun2()" << endl; }
};
class D: public B{
public:
    double k;
    virtual void fun1() { cout << "D::fun1()" << endl; }
};
int main() {
    B b; D d;
    B *pB = &d;
    pB->fun1(); // D::fun1() —— 通过VPTR查找VTABLE，晚绑定
    return 0;
}
```

==== 存放类型信息

```cpp
class NoVirtual{ int a; public: void f1() const {} int f2() const {return 1;} };
class OneVirtual{ int a; public: virtual void f1() const {} int f2() const {return 1;} };
class TwoVirtual{ int a; public: virtual void f1() const {} virtual int f2() const {return 1;} };
// 64位机器：
// sizeof(int) = 4
// sizeof(NoVirtual) = 4
// sizeof(void*) = 8
// sizeof(OneVirtual) = 12  (int 4 + VPTR 8)
// sizeof(TwoVirtual) = 12  (多个虚函数共享同一个VTABLE)
```

=== 六、虚函数和构造函数、析构函数

==== 虚函数与构造函数

+ 构造函数*不能也不必*是虚函数。不能：如果构造函数是虚函数，创建对象时需要先知道VPTR，但VPTR在构造函数调用前未初始化。不必：构造函数调用时明确指定要创建对象的类型。
+ 在构造函数中调用虚函数，被调用的只是这个函数的*本地版本*（当前类的版本），即虚机制在构造函数中不工作。
+ 原因：基类的构造函数比派生类先执行，调用基类构造函数时派生类中的数据成员还没有初始化。

```cpp
class Base {
public:
    virtual void foo(){cout<<"Base::foo"<<endl;}
    Base(){foo();} // 构造函数中调用虚函数
    void bar(){foo();};
};
class Derived : public Base {
public:
    int _num;
    void foo(){cout<<"Derived::foo"<<_num<<endl;}
    Derived(int j):Base(),_num(j){}
};
int main() {
    Derived d(0); // 输出 Base::foo（构造函数中虚机制不工作）
    Base &b = d;
    b.bar();      // 输出 Derived::foo0
    b.foo();      // 输出 Derived::foo0
    return 0;
}
```

==== 虚函数与析构函数

+ 析构函数*能是虚的，且常常是虚的*。虚析构函数仍需定义函数体。
+ 若基类析构不是虚函数，则删除基类指针所指派生类对象时，编译器仅自动调用基类的析构函数，可能导致*内存泄漏*。
+ 在析构函数中调用虚函数，虚机制同样不工作。

*重要原则：总是将基类的析构函数设置为虚析构函数！*

```cpp
class Base1 { public: ~Base1() { cout << "~Base1()\n"; } };
class Derived1 : public Base1 { public: ~Derived1() { cout << "~Derived1()\n"; } };
class Base2 { public: virtual ~Base2() { cout << "~Base2()\n"; } };
class Derived2 : public Base2 { public: ~Derived2() { cout << "~Derived2()\n"; } };
int main() {
    Base1* bp = new Derived1;
    delete bp;   // ~Base1() —— 只调用了基类析构！内存泄漏！
    Base2* b2p = new Derived2;
    delete b2p;  // ~Derived2() ~Base2() —— 虚析构，正确调用
    return 0;
}
```

=== 七、重写覆盖与重写隐藏

==== 三者对比

#table(
  columns: (auto, 1fr, 1fr, 1fr),
  align: center + horizon,
  stroke: 0.5pt,
  table.cell(colspan: 4)[*重载、重写隐藏与重写覆盖*],
  [], [重载(overload)], [重写隐藏(redefining)], [重写覆盖(override)],
  [作用域], [相同（同一个类中，或均为全局函数）], [不同（派生类和基类）], [不同（派生类和基类）],
  [函数名], [相同], [相同], [相同],
  [函数参数], [不同], [相同/不同], [相同],
  [返回值], [不能仅返回值不同], [无要求], [相同或协变的],
  [其他要求], [—], [若参数相同，则基类函数不能为虚函数], [基类函数为虚函数],
)

*关键区别：*重写覆盖要求基类的函数是虚函数且参数相同；重写隐藏是参数不同或基类函数不是虚函数。重写覆盖会使派生类虚函数表中基类的虚函数指针被派生类的虚函数指针覆盖；重写隐藏不会。

==== 重写覆盖示例

```cpp
class Base{
public:
    virtual void foo(){cout<<"Base::foo()"<<endl;}
    virtual void foo(int){cout<<"Base::foo(int)"<<endl;} // 重载
};
class Derived1 : public Base {
public:
    void foo(int){cout<<"Derived1::foo(int)"<<endl;} // 重写覆盖
};
class Derived2 : public Base {
public:
    void foo(float){cout<<"Derived2::foo(float)"<<endl;} // 参数写错，是重写隐藏！
};
int main() {
    Derived1 d1; Derived2 d2;
    Base* p1 = &d1; Base* p2 = &d2;
    p1->foo(3);   // Derived1::foo(int) —— 重写覆盖
    p2->foo(3.0); // Base::foo(int) —— 重写隐藏，虚函数表中是基类的
    return 0;
}
```

=== 八、override 和 final 关键字

==== override

`override` 关键字明确告诉编译器一个函数是对基类中虚函数的重写覆盖，编译器将对各项条件进行检查。如果没有 `override` 但满足条件，也能实现重写覆盖——它只是编译器的一个检查。

```cpp
class Derived3 : public Base {
public:
    void foo(int) override {cout<<"Derived3::foo(int)"<<endl;}; // 正确
    //void foo(float) override {}; // 参数不同，编译错误
    //void bar() override {};     // bar非虚函数，编译错误
};
```

==== final

`final` 关键字：在虚函数声明中使用时，确保函数不可被派生类重写；在类定义中使用时，指定此类不可被继承。

```cpp
class Base{ virtual void foo(){}; };
class A: public Base {
    void foo() final {}; // 重写覆盖，且是最终覆盖
    //void bar() final {}; // bar非虚函数，编译错误
};
class B final : public A{
    //void foo() override {}; // A::foo已是最终覆盖，编译错误
};
//class C : public B{}; // B不能被继承，编译错误
```

=== 九、const 对重写覆盖的影响（课后探究）

使用 `const` 修饰成员函数，可能导致重写覆盖失效（变成重写隐藏）：

```cpp
class Base1{
public:
    virtual void f() {cout << "Base1::f" << endl;}
};
class Derive1: public Base1{
public:
    void f() const {cout << "Derive1::f" << endl;} // 重写覆盖失效，其实是重写隐藏
    using Base1::f; // 恢复被隐藏的基类函数
};
int main(){
    Derive1 a; const Derive1 b;
    a.f(); // Base1::f（非常量对象优先匹配Base1::f）
    b.f(); // Derive1::f（常量对象调用Derive1::f）
    return 0;
}
```

=== 十、虚函数的返回值（课后探究）

一般来说，派生类虚函数的返回类型应该和基类相同；或者，是*协变*(Covariant)的——基类和派生类的指针/引用是协变的。

```cpp
class Instrument {
public:
    virtual Instrument& getObj() { return *this; }
};
class Wind : public Instrument {
public:
    virtual Wind& getObj() { return *this; } // Wind&和Instrument&协变
};
```

协变条件：都是指针（不能是多级指针）、都是左值引用或都是右值引用，且基类返回类型中被引用的类是派生类返回类型中被引用的类的祖先类。

=== 十一、课后练习

根据以下代码实现 Animal、Bird、Fish 类：

```cpp
void action(Animal* pAnimal) {
    pAnimal -> sing();
    pAnimal -> swim();
}
int main(){
    Animal *myBird = new Bird();
    Animal *myFish = new Fish();
    action(myBird);
    action(myFish);
    delete myBird;
    delete myFish;
    return 0;
}
```

参考输出：
```text
bird is singing.
bird can't swim.
fish can't sing.
fish is swimming.
bird has gone.
fish has gone.
```

=== 附录：利用返回值优化提高执行效率

返回值优化（RVO）条件：
+ 返回的值类型与函数签名的返回值类型相同
+ 返回的是一个局部对象的左值

```cpp
Test fn1(){ Test tmp; return tmp; } // 满足RVO条件
Test&& fn2(){ Test tmp; return move(tmp); } // 不建议：d指向被析构的tmp
int main(){
    const Test& a = fn1();  // (4) 常量左值引用接收
    Test&& b = fn1();       // (5) 右值引用接收
    Test c = fn1();         // (6) 构造新对象接收
    // Test&& d = fn2();    // (7) 运行错误
    return 0;
}
```

== 捌 多态与模板 #datetime(day:21,month:4,year:2026).display()
<捌-多态与模板-2026.4.21>

=== 一、纯虚函数与抽象类

虚函数还可以进一步声明为*纯虚函数*：

```cpp
virtual 返回类型 函数名(形式参数) = 0;
```

包含纯虚函数的类被称为*抽象类*。抽象类*不允许定义对象*，主要用途是为派生类规定共性"接口"。

```cpp
class A {
public:
    virtual void f() = 0; // 可在类外定义函数体提供默认实现
};
A obj; // 编译错误！不准抽象类定义对象！
```

抽象类特点：
+ 不允许定义对象
+ 只能为派生类提供接口
+ 能避免对象切片：保证只有指针和引用能被向上类型转换

基类纯虚函数被派生类重写覆盖之前仍是纯虚函数。因此当继承一个抽象类时，除纯虚析构函数外，必须实现所有纯虚函数，否则继承出的类也是抽象类。

```cpp
class Pet {
public:
    virtual void motion()=0;
};
void Pet::motion(){ cout << "Pet motion: " << endl; }
class Dog: public Pet {
public:
    void motion() override {Pet::motion(); cout << "dog run" << endl; }
};
class Bird: public Pet {
public:
    void motion() override {Pet::motion(); cout << "bird fly" << endl; }
};
int main() {
    Pet* p = new Dog;
    p->motion(); // Pet motion: dog run
    p = new Bird;
    p->motion(); // Pet motion: bird fly
    return 0;
}
```

=== 二、纯虚析构函数

析构函数也可以是纯虚函数：
+ 纯虚析构函数*仍然需要函数体*
+ 目的：使基类成为抽象类，不能创建基类的对象

```cpp
class Base { public: virtual ~Base()=0; };
Base::~Base() {} // 必须有函数体
class Derive : public Base {};
int main() {
    //Base b;  // 编译错误，基类是抽象类
    Derive d1; // 派生类不必实现纯虚析构函数
    return 0;
}
```

*与一般纯虚函数的区别：*对于纯虚析构函数，即便派生类中不显式实现，编译器也会自动合成默认析构函数。因此只要派生类覆盖了其他纯虚函数，该派生类就不是抽象类。

=== 三、向下类型转换

基类指针/引用转换成派生类指针/引用，称为*向下类型转换*。

为什么要向下类型转换？当我们用基类指针表示各种派生类时，保留了共性但丢失了特性。使用向下类型转换可以表现特性。

==== dynamic_cast

安全的向下类型转换，使用虚函数表中的信息判断实际类型：

```cpp
T2* pObj = dynamic_cast<T2*>(obj_p);    // 运行时失败返回nullptr
T2& refObj = dynamic_cast<T2&>(obj_r);  // 运行时失败抛出bad_cast异常
```

T1必须是多态类型（声明或继承了至少一个虚函数的类）。

==== static_cast

编译时静态浏览类层次，只检查继承关系，*不安全*：

```cpp
D* pd1 = static_cast<D*>(&b);  // 有继承关系就允许，但不安全
D* pd2 = dynamic_cast<D*>(&b); // 运行时检查，安全
```

==== dynamic_cast 与 static_cast 对比

#table(
  columns: (auto, 1fr, 1fr),
  align: left + horizon,
  stroke: 0.5pt,
  [], [dynamic_cast], [static_cast],
  [检查时机], [运行时], [编译时],
  [安全性], [安全（失败返回nullptr/异常）], [不安全（不保证指向正确类型）],
  [性能], [较慢（需要RTTI）], [较快],
  [要求], [类必须有虚函数], [只需有继承关系],
)

*重要原则：*
+ 指针或引用的向上转换总是安全的
+ 向下转换时用 `dynamic_cast`，安全检查
+ 避免对象之间的转换

==== 向下类型转换示例

```cpp
class Pet { public: virtual ~Pet() {} };
class Dog : public Pet { public: void run() { cout << "dog run" << endl; } };
class Bird : public Pet { public: void fly() { cout << "bird fly" << endl; } };
void action(Pet* p) {
    auto d = dynamic_cast<Dog*>(p);
    auto b = dynamic_cast<Bird*>(p);
    if (d) d->run();
    else if(b) b->fly();
}
int main() {
    Pet* p[2];
    p[0] = new Dog;
    p[1] = new Bird;
    for (int i = 0; i < 2; ++i) action(p[i]);
    return 0;
}
```

=== 四、多重继承中的虚函数

Best Practice：
+ 最多继承一个非抽象类（is-a）
+ 可以继承多个抽象类（接口）

这样避免了多重继承的二义性，且一个对象可以实现多个接口。

```cpp
class WhatCanSpeak {
public:
    virtual ~WhatCanSpeak() {}
    virtual void speak() = 0;
};
class WhatCanMotion {
public:
    virtual ~WhatCanMotion() {}
    virtual void motion() = 0;
};
class Human : public WhatCanSpeak, public WhatCanMotion {
    void speak() { cout << "say" << endl; }
    void motion() { cout << "walk" << endl; }
};
void doSpeak(WhatCanSpeak* obj) { obj->speak(); }
void doMotion(WhatCanMotion* obj) { obj->motion(); }
int main() {
    Human human;
    doSpeak(&human); // say
    doMotion(&human); // walk
    return 0;
}
```

=== 五、多态（Polymorphism）

按照基类的接口定义，调用指针或引用所指对象的接口函数，函数执行过程因对象实际所属派生类的不同而呈现不同的效果——这就是"多态"。

+ 利用基类指针/引用调用函数时：虚函数在*运行时*确定执行哪个版本；非虚函数在*编译时*绑定
+ 利用类的对象直接调用函数时：无论什么函数，均在*编译时*绑定

*产生多态效果的条件：继承 && 虚函数 && (引用 或 指针)*

多态使得C++可以用一段相同的代码，在运行时完成不同的任务。好处：
+ 通过基类定好接口后，不必对每一个派生类特殊处理，大大提高程序的可复用性
+ 不同派生类对同一接口的实现不同，提高了程序可拓展性和可维护性

```cpp
class Animal{
public:
    void action() { speak(); motion(); }
    virtual void speak() { cout << "Animal speak" << endl; }
    virtual void motion() { cout << "Animal motion" << endl; }
};
class Bird : public Animal {
public:
    void speak() { cout << "Bird singing" << endl; }
    void motion() { cout << "Bird flying" << endl; }
};
class Fish : public Animal {
public:
    void speak() { cout << "Fish cannot speak ..." << endl; }
    void motion() { cout << "Fish swimming" << endl; }
};
int main() {
    Animal *pBase1 = new Fish;
    Animal *pBase2 = new Bird;
    pBase1->action(); // Fish cannot speak ... / Fish swimming
    pBase2->action(); // Bird singing / Bird flying
    return 0;
}
```

==== Template Method 设计模式

在接口的一个方法中定义算法的骨架，将一些步骤的实现延迟到子类中，使得子类可以在不改变算法结构的情况下重新定义算法中的某些步骤。

```cpp
class Base{
public:
    void action() { step1(); step2(); step3(); } // 算法骨架
    virtual void step1() { cout << "Base::step1" << endl; }
    virtual void step2() { cout << "Base::step2" << endl; }
    virtual void step3() { cout << "Base::step3" << endl; }
};
class Derived1 : public Base{
    void step1() { cout << "Derived1::step1" << endl; }
};
class Derived2 : public Base{
    void step2() { cout << "Derived2::step2" << endl; }
};
int main(){
    Base* ba[] = {new Base, new Derived1, new Derived2};
    for (int i = 0; i < 3; ++i) ba[i]->action();
    return 0;
}
```

=== 六、函数模板和类模板

继承与组合提供了重用*对象代码*的方法，而C++的模板特征提供了重用*源代码*的方法。

==== 函数模板

将函数的参数类型也定义为一种特殊的"参数"：

```cpp
template <typename T>
T sum(T a, T b) { return a + b; }
// typename 也可换为 class
```

编译器能自动推导出实际参数的类型（实例化）：

```cpp
cout << sum(9, 3);     // int
cout << sum(2.1, 5.7); // double
// cout << sum(9, 2.1); // 编译错误，类型不一致
cout << sum<int>(9, 2.1); // 手工指定类型
```

==== 函数模板示例

```cpp
template<class T>
void sort(T* data, int len) {
    for(int i = 0; i < len; i++){
        for(int j = i + 1; j < len; j++) {
            if(data[i] > data[j])
                std::swap(data[i], data[j]);
        }
    }
}
template<class T>
void output(T* data, int len) {
    for(int i = 0; i < len; i++)
        std::cout << data[i] << " ";
    std::cout << std::endl;
}
int main() {
    int arr_a[] = {3,2,4,1,5};
    sort(arr_a, 5); output(arr_a, 5);
    float arr_b[] = {3.2, 2.1, 4.3, 1.5, 5.7};
    sort(arr_b, 5); output(arr_b, 5);
    return 0;
}
```

模板也可以支持自定义类型，只要类型满足函数的要求（如定义了 `operator>`）：

```cpp
class MyInt {
public:
    int data;
    MyInt(int val): data(val) {};
    bool operator>(const MyInt& b){ return data > b.data; }
    friend std::ostream& operator<<(std::ostream& out, const MyInt& obj){
        out << obj.data; return out;
    }
};
```

==== 模板原理

对模板的处理是在*编译期*进行的。每当编译器发现对模板的一种参数的使用，就生成对应参数的一份代码。

这也带来了问题：模板库*必须在头文件中实现*，不可以分开编译。因为分开编译时，`.cpp` 文件只看到模板声明，看不到定义，无法实例化，链接时会找不到定义。

==== 类模板

将类中的类型信息抽取出来用模板参数替换：

```cpp
template <typename T> class A {
    T data;
public:
    A(T _data): data(_data) {}
    void print();
};
template<typename T>
void A<T>::print() { cout << data << endl; } // 类外定义
int main() {
    A<int> a(1);
    a.print();
    return 0;
}
```

类模板的模板参数：
+ *类型参数*：使用 `typename` 或 `class` 标记
+ *非类型参数*：整数、枚举、指针、引用。无符号整数比较常用

```cpp
template<typename T, unsigned size>
class array { T elems[size]; };
array<char, 10> array0;
```

所有模板参数必须在编译期确定，不可以使用变量（可以使用常量或具体数值）。

==== 类模板示例

```cpp
template<class T, unsigned size>
class MyArr {
    T data[size];
public:
    void sort(){
        for(int i = 0; i < size; i++)
            for(int j = i + 1; j < size; j++)
                if(data[i] > data[j])
                    std::swap(data[i], data[j]);
    }
    void output(){
        for(int i = 0; i < size; i++)
            std::cout << data[i] << " ";
        std::cout << std::endl;
    }
    void input(){
        for(int i = 0; i < size; i++)
            std::cin >> data[i];
    }
};
int main() {
    MyArr<int, 5> arr_a;
    arr_a.input(); arr_a.sort(); arr_a.output();
    MyArr<float, 5> arr_b;
    arr_b.input(); arr_b.sort(); arr_b.output();
    return 0;
}
```

=== 七、模板与多态

模板也是多态的一种体现，但模板的关联是在*编译期*处理，称为*静多态*。

#table(
  columns: (auto, 1fr, 1fr),
  align: left + horizon,
  stroke: 0.5pt,
  [], [静多态（模板）], [动多态（虚函数）],
  [处理时机], [编译期], [运行时],
  [特点], [高效，省去函数调用；编译后代码增多], [灵活方便；存在函数调用；侵入式，必须继承],
  [关联方式], [泛型标记+函数重载], [继承+虚函数],
)

=== 八、成员函数模板（自学）

普通类的成员函数也可以定义为模板函数：

```cpp
class normal_class {
public:
    int value;
    template<typename T> void set(T const& v) { value = int(v); }
    template<typename T> T get();
};
template<typename T>
T normal_class::get() { return T(value); }
```

模板类的成员函数也可以有额外的模板参数：

```cpp
template<typename T0> class A {
    T0 value;
public:
    template<typename T1> void set(T1 const& v) { value = T0(v); }
    template<typename T1> T1 get();
};
template<typename T0> template<typename T1> // 注意：不能写成 template<typename T0, typename T1>
T1 A<T0>::get(){ return T1(value); }
int main() {
    A<int> a;
    a.set(5);                    // 自动推导
    double t = a.get<double>();  // 手动指定返回值类型
    return 0;
}
```

=== 九、课后练习

==== 练习1

重载、重写、虚函数重写的情况下，编译器如何处理返回值不同的函数？

```cpp
class Base {
public:
    virtual void f() {std::cout << "Call Base void f() " << std::endl;}
    virtual void g() {std::cout << "Call Base void g() " << std::endl;}
    void h() {std::cout << "Call Base void h()" << std::endl;}
};
class Derived : public Base {
public:
    void f() { std::cout << "Call Derive void f() " << std::endl; } // 重写覆盖
    int g() { std::cout << "Call Derive int g()" << std::endl; return 0; } // 编译错误！
    int h() { std::cout << "Call Base int h()" << std::endl; return 0; } // 重写隐藏
};
```

==== 练习2

仿照 C++ 的 vector 实现一个 `Vector` 类，要求使用模板以支持任意类型的元素，并且至少具有以下成员函数：

+ `void push_back();`
+ `void pop_back();`
+ `int size();`
+ `operator[]();`

== 玖 模板与STL初步 #datetime(day:28,month:4,year:2026).display()
<玖-模板与STL初步-2026.4.28>

=== 一、命名空间

为了避免在大规模程序中使用各种C++库时标识符命名冲突，C++引入了 `namespace`（命名空间）。

标准C++库中所有内容（常量、变量、结构、类和函数等）都被定义在命名空间 `std` 中。

定义命名空间：

```cpp
namespace A {
    int x, y;
}
```

使用命名空间：

```cpp
A::x = 3;
A::y = 6;
```

使用 `using` 声明简化：

```cpp
using namespace A;    // 使用整个命名空间，所有成员直接可用
x = 3; y = 6;

using A::x;           // 使用部分成员
x = 3; A::y = 6;
```

#strong[任何情况下，都不应出现命名冲突。]

=== 二、STL简介

标准模板库（Standard Template Library，STL）是高效的C++软件库，包含4个组件：*算法、容器、函数、迭代器*。

关键理念：将"在数据上执行的操作"与"要执行操作的数据"分离。

+ STL的命名空间是 `std`
+ 一般使用 `std::name` 来使用STL的函数或对象
+ 也可以使用 `using namespace std`（不推荐在大型工程中使用，容易污染命名空间）

=== 三、STL容器

容器是包含、放置数据的工具，通常为数据结构。包括：简单容器、序列容器、关系容器。

==== pair

最简单的容器，由两个单独数据组成：

```cpp
template<class T1, class T2> struct pair {
    T1 first;
    T2 second;
};
```

使用：

```cpp
std::pair<int, int> t;
t.first = 4; t.second = 5;
// 创建：使用 make_pair，自动推导类型
auto t = std::make_pair("abc", 7.8);
```

pair 支持小于、等于等比较运算符：先比较 first，后比较 second。

```cpp
std::make_pair(1, 4) < std::make_pair(2, 3);  // true
std::make_pair(1, 4) > std::make_pair(1, 2);  // true
```

==== tuple（C++11）

pair的扩展，由若干成员组成的元组类型：

```cpp
template<class ...Types> class tuple;
```

创建：`make_tuple` 和 `tie` 函数：

```cpp
auto t = std::make_tuple("abc", 7.8, 123, '3');
// tie 返回左值引用的元组
std::string x; double y; int z;
std::tie(x, y, z) = std::make_tuple("abc", 7.8, 123);
```

通过 `std::get` 获取数据（下标需在编译时确定）：

```cpp
auto v0 = std::get<0>(t);
int i = 0;
// v = std::get<i>(t); // 编译错误！下标必须编译时常量
```

tuple 常用于函数多返回值的传递：

```cpp
std::tuple<int, double> f(int x) {
    return std::make_tuple(x, double(x) / 2);
}
int main() {
    int xval; double half_x;
    std::tie(xval, half_x) = f(7);
    return 0;
}
```

==== vector

会自动扩展容量的数组，STL中最基本的序列容器：

```cpp
template<class T, class Allocator = std::allocator<T>>
class vector;
```

常用操作：

```cpp
std::vector<int> x;       // 创建
x.size();                  // 当前长度
x.clear();                 // 清空
x.push_back(1);            // 末尾添加（高速）
x.pop_back();              // 末尾删除（高速）
x.insert(x.begin()+1, 5);  // 中间添加（低速）
x.erase(x.begin()+1);      // 中间删除（低速）
```

==== vector原理

除了 `size`，另保存 `capacity`（最大容量限制）。如果 `size` 达到了 `capacity`，则另申请一片 `capacity*2` 的空间，并整体迁移内容。

+ `push_back` 等修改 vector 大小的方法可能会使*所有迭代器失效*（因为整体迁移）
+ `insert/erase` 后，所修改位置之后的所有迭代器失效
+ 时间复杂度为均摊 O(1)

=== 四、迭代器

一种检查容器内元素并遍历元素的数据类型，为遍历不同的聚合结构提供统一的接口。使用上类似指针。

以 vector 为例：

```cpp
vector<int>::iterator iter; // 定义迭代器
x.begin();  // 第一个元素的迭代器
x.end();    // 最后一个元素之后的位置的迭代器
// begin 和 end 构成左闭右开区间
```

迭代器操作：

+ `++iter` / `--iter`：下一个/上一个元素
+ `iter += n` / `iter -= n`：移动 n 个元素
+ `*iter`：解引用，返回左值引用
+ `iter1 - iter2`：元素位置差

遍历 vector：

```cpp
// 迭代器遍历
for (auto it = vec.begin(); it != vec.end(); ++it)
    *it *= 2;
// C++11 按范围遍历（等价）
for (auto& x : vec)
    x *= 2;
```

==== 迭代器失效

当迭代器不再指向本应指向的元素时，称此迭代器*失效*。

+ `insert/erase` 后，所修改位置之后的所有迭代器失效
+ `push_back` 等修改 vector 大小的方法可能会使所有迭代器失效（整体迁移）
+ 修改容器后，#strong[不使用之前的迭代器]（绝对安全的准则）

=== 五、STL其他容器

==== list

链表容器（底层实现是双向链表）：

```cpp
std::list<int> l;
l.push_front(1);     // 插入前端
l.push_back(2);      // 插入末端
std::find(l.begin(), l.end(), 2); // 查询，返回迭代器
l.insert(it, 4);     // 在迭代器位置插入
```

+ 不支持下标等随机访问
+ 支持在任意位置高速插入/删除
+ 插入和删除操作不会导致迭代器失效（除指向被删除元素的迭代器外）

==== set

不重复元素构成的集合（内部按大小顺序排列）：

```cpp
std::set<int> s;
s.insert(val);              // 插入（不允许重复）
s.find(val);                // 查询，返回迭代器
s.erase(s.find(val));       // 删除
s.count(val);               // val的个数，总是0或1
```

注意：set 的"无序"是指不保持插入顺序，内部按元素大小排列。

==== map

关联数组，将一个数据项映射到另一个数据项。值类型为 `pair<Key, T>`，key必须互不相同。

```cpp
std::map<std::string, int> s;
s["Monday"] = 1;            // 下标访问（key不存在则创建）
s.insert(std::make_pair(std::string("Tuesday"), 2));
s.find(key);                // 查询，返回迭代器
s.count(key);               // 返回0或1
s.erase(s.find(key));       // 删除
```

map 常用作稀疏数组或以字符串为下标的数组：

```cpp
std::map<std::string, std::string> M;
M["fp"] = "c";
M["oop"] = M["fp"] + "++"; // M["oop"] = "c++"
```

==== 关联容器原理

set 和 map 底层数据结构都是红黑树（一种二叉平衡树），几乎所有操作复杂度均为 O(log n)。

==== 容器总结

#table(
  columns: (auto, 1fr, 1fr),
  align: left + horizon,
  stroke: 0.5pt,
  [], [vector], [list],
  [底层结构], [动态数组], [双向链表],
  [随机访问], [支持（高速）], [不支持],
  [中间插入/删除], [低速], [高速],
  [迭代器失效], [操作位置之后全部失效], [仅被删除元素失效],
)

#table(
  columns: (auto, 1fr, 1fr),
  align: left + horizon,
  stroke: 0.5pt,
  [], [set], [map],
  [底层结构], [红黑树], [红黑树],
  [特点], [不重复有序集合], [键值映射],
  [操作复杂度], [O(log n)], [O(log n)],
)

选择容器的参考：
+ 频繁在中间插入/删除 → `list`，否则 → `vector`
+ 需要按值快速查找 → `set`、`map`
+ 希望迭代器尽量不失效 → `list`、关联容器

=== 六、string字符串类

STL提供的变长字符串类型，比 C 风格的 `char` 数组更方便：

```cpp
string fullname = firstname + " " + lastname; // 简洁拼接
cout << fullname << endl;
```

==== 构造方式

```cpp
string s0("Initial string");            // 从C风格字符串构造
string s1;                              // 默认空字符串
string s2(s0, 8, 3);                    // 截取："str"（从index 8开始，长度3）
string s3("Another character sequence", 12); // 截取："Another char"
string s4(10, 'x');                     // 复制字符："xxxxxxxxxx"
string s5(s0.begin(), s0.begin()+7);    // 迭代器范围复制："Initial"
```

转为C风格字符串：`str.c_str()`（返回 `const char*`）。

==== 常用函数

与 vector 类似：`str[i]`、`str.size()`、`str.clear()`、`str.empty()`、`str.push_back('a')`、`str.append(s2)`。

不同之处：
+ 查询长度也可以用 `str.length()`，与 `size()` 返回值相同
+ 向尾部增加也可以用 `str += 'a'` 或 `str += s2`

==== 输入方式

```cpp
cin >> firstname;                       // 读到空格为止
getline(cin, fullname);                 // 读一行
getline(cin, fullnames, '#');           // 读到指定分隔符为止（可读入换行符）
```

==== 拼接与比较

```cpp
// 拼接
string fullname = firstname + " " + lastname;
// 注意：拼接时间复杂度为生成字符串长度
// 多次拼接应使用 operator+= 或 stringstream
for (int i = 0; i < n; i++)
    allname = allname + name[i] + "\n"; // O(n^2 * L)，很慢！
allname += name[i] + "\n";              // 改用 += 更高效

// 比较：按字典序
string a = "alice", b = "bob";
a == b;  // false
a < b;   // true
```

==== 数值转换

```cpp
// 数值 → 字符串
to_string(1);            // "1"
to_string(3.14);         // "3.14"

// 字符串 → 数值
int a = stoi("2001");                          // a = 2001
std::string::size_type sz;
int b = stoi("50 cats", &sz);                  // b = 50, sz = 2
int c = stoi("40c3", nullptr, 16);             // c = 0x40c3（十六进制）
int d = stoi("0x7f", nullptr, 0);              // d = 0x7f（自动检查进制）
double e = stod("34.5");                       // e = 34.5
```

=== 七、同义词查询库（自学）

使用 `map<string, vector<string>>` 构建词语与同义词的映射：

```cpp
class SynonymBase {
    map<string, vector<string>> synonyms;
public:
    void add(string word, string synonym) {
        synonyms[word].push_back(synonym);
    }
    void query(string word) {
        if (synonyms.find(word) == synonyms.end())
            cout << "no synonyms found" << endl;
        else
            for (auto& x : synonyms[word]) cout << x << endl;
    }
};
```

增加判定两个词是否为同义词的需求时，将 `vector` 改为 `set` 以提高查找效率：

```cpp
class SynonymBase {
    map<string, set<string>> synonyms;
public:
    bool _has_synonym(string word1, string word2) {
        return synonyms.find(word1) != synonyms.end() &&
               synonyms[word1].find(word2) != synonyms[word1].end();
    }
    bool isSynonyms(string word1, string word2) {
        if (word1 == word2) return true;
        return _has_synonym(word1, word2) || _has_synonym(word2, word1);
    }
};
```

=== 八、函数模板与类模板特化（自学）

==== 函数模板特化

对模板在某种具体类型下进行特殊处理：

```cpp
template<class T>
T div2(const T& val) {
    cout << "using template" << endl;
    return val / 2;
}
template<>
int div2(const int& val) {  // 函数模板特化
    cout << "better solution!" << endl;
    return val >> 1;         // 右移取代除以2
}
```

注意：函数模板有多个模板参数时，特化必须提供#strong[所有]参数的特例类型，不能部分特化。但可以用重载来替代。

函数模板重载解析顺序：
+ 类型匹配的普通函数 → 基础函数模板 → 全特化函数模板
+ 先从基础模板中选择最匹配的，再查看有无对应的全特化版本

#strong[重要：]函数模板的全特化版本匹配优先级可能低于重载的非特化基础模板，因此最好直接使用重载函数而非全特化。

==== 类模板特化

类模板可以进行全部特化和部分特化：

```cpp
// 通用模板
template<typename T1, typename T2> class A { ... };
// 全部特化：指定所有类型
template<> class A<int, int> { ... };
// 部分特化：只限制部分类型
template<typename T1> class A<T1, int> { ... };
```

全部特化示例：

```cpp
template<typename T1, typename T2>
class Sum {
public:
    Sum(T1 a, T2 b) { cout << "Sum general: " << a+b << endl; }
};
template<>
class Sum<int, int> {
public:
    Sum(int a, int b) { cout << "Sum specific: " << a+b << endl; }
};
Sum<int, int> s1(1, 2);         // Sum specific: 3
Sum<int, double> s2(1, 2.5);    // Sum general: 3.5
```

部分特化示例：

```cpp
template<typename T1>
class Sum<T1, int> {
public:
    Sum(T1 a, int b) { cout << "Sum specific: " << a+b << endl; }
};
Sum<double, int> s1(1.5, 2);        // Sum specific: 3.5
Sum<double, double> s2(1.5, 2.5);   // Sum general: 4
```

==== 模板特化总结

+ 类模板可以部分特化或全部特化，编译器根据类型参数自动选择
+ 函数模板只能全部特化，但可通过重载代替部分特化
+ 函数模板全特化匹配优先级可能低于重载的非特化基础模板，最好直接用重载