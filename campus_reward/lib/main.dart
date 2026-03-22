import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'welcome',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          onPressed: () => {},
          icon: Icon(Icons.add_to_photos),
        ),
        title: Text('appbar'),
        actions: <Widget>[
          IconButton(
            onPressed: () => {},
            icon: Icon(Icons.add),
            tooltip: 'add',
          ),
          IconButton(
            onPressed: () => {},
            icon: Icon(Icons.delete),
            tooltip: 'delete',
          ),
          IconButton(
            onPressed: () => {},
            icon: Icon(Icons.search),
            tooltip: 'search',
          ),
        ],
      ),
      body: Container(
        alignment: Alignment.center,
        constraints: BoxConstraints.expand(width: 100, height: 80),
        decoration: BoxDecoration(
          border: Border.all(
            color: Colors.yellowAccent,
            style: BorderStyle.solid,
            width: 5,
          ),
          image: null,
          borderRadius: BorderRadius.all(Radius.circular(30)),
          boxShadow: [
            BoxShadow(
              color: Colors.redAccent,
              offset: Offset(20, 20),
              blurRadius: 10,
            ),
          ],
        ),
        transform: Matrix4.rotationZ(.3),
        child: Text('dat'),
      ),
    );
  }
}
