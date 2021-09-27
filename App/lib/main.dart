import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(App());
}

// ignore: use_key_in_widget_constructors
class App extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '1LO app',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const HomePage(),
    );
  }
}

class Article {
  final String title;
  final String date;
  final String img;
  final String content;

  Article(this.title, this.date, this.img, this.content);
}

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
            title: const TextField(
          cursorColor: Colors.white,
          textAlign: TextAlign.center,
          style: TextStyle(color: Colors.white),
          decoration: InputDecoration(
              hintText: 'Wyszukaj artykułu', suffixIcon: Icon(Icons.search)),
        )),
        body: Center(
            child: GridView.count(
          padding: const EdgeInsets.all(20.0),
          mainAxisSpacing: 15.0,
          crossAxisCount: 1,
          children: const <Widget>[News()],
        )));
  }
}

class News extends StatelessWidget {
  const News({Key? key}) : super(key: key);

  request() async {
    var r = await http.get(
        Uri.parse("https://1LO-server.kacperek0.repl.co/article/latest/5"));
    var json = jsonDecode("[" + const Utf8Decoder().convert(r.bodyBytes) + "]");
    List<Article> articles = [];

    for (var x in json) {
      for (var i = 0; i < 5; i++) {
        Article article = Article(x['$i']['title'], x['$i']['date'],
            x['$i']['img'], x['$i']['content']);
        articles.add(article);
      }
    }
    return articles;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: request(),
      builder: (BuildContext context, AsyncSnapshot snapshot) {
        if (snapshot.data == null) {
          return const Text("Ładowanie...");
        } else {
          return ListView.builder(
              itemCount: 5,
              itemBuilder: (context, i) {
                return Container(
                    margin: const EdgeInsets.all(10.0),
                    padding: const EdgeInsets.all(10.0),
                    decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: const BorderRadius.only(
                            topLeft: Radius.circular(7),
                            topRight: Radius.circular(7),
                            bottomLeft: Radius.circular(7),
                            bottomRight: Radius.circular(7)),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.grey.withOpacity(0.4),
                            spreadRadius: 3,
                            blurRadius: 3,
                            offset: const Offset(
                                0, 3), // changes position of shadow
                          ),
                        ]),
                    child: ListTile(
                      title: Text(snapshot.data[i].title),
                      subtitle: Column(children: <Widget>[
                        Image.network(snapshot.data[i].img),
                        Text(snapshot.data[i].content)
                      ]),
                      trailing: Text(snapshot.data[i].date),
                    ));
              });
        }
      },
    );
  }
}
