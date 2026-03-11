#import "../../module/myutils.typ":*

#show : conf

= 离散数学 2 作业 紫荆书院 紫荆 53 郭嘉乐

#outline()

== 第 2 次 #datetime(day:11,month:3,year:2026).display()

=== P14.14

#mgraph(captions:([1],[2],[3]),```
graph G {
  0 -- 1;
  0 -- 3;
  1 -- 3;
  2 -- 3;
}
```,
```
graph H {
  0 -- 3;
  1 -- 3;
  0 -- 1;
  0 -- 2; 
  2 -- 3;
}
```,
```
graph K {
  0 -- 2;
  2 -- 3;
  3 -- 1;
  1 -- 0;
}```,

)

=== P14.16

=== P14.17

=== P14.21