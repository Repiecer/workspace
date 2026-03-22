void main(List<String> args) {
  final time = DateTime.now();
  var press = "hello world";
  print(time);
  print(press.toUpperCase().split(' '));
  Map map = new Map()
    ..['name'] = 'name'
    ..['age'] = 11;
  print(map);
  Point po1 = new Point(5, 8);
  Point po2 = new Point(8, 9);
  print(po1 + po2);
  var num = 5;

  switch (num) {
    case 1:
      print('1');
      break;
    case 2:
      print('5');
      break;
  }
  List lisl = [1, 2, 3, 4];
  lisl.forEach(print);
}

class Point {
  var x, y;
  Point(this.x, this.y);
  operator +(p) => new Point(x + p.x, y + p.x);
  @override
  String toString() {
    return x.toString() + y.toString();
  }
}
