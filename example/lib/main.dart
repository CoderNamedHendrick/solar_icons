import 'package:flutter/material.dart';
import 'package:solar_icons/solar_icons.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'SolarIcons Demo'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  static const icons = [
    IconModel(
      icon: SolarIconsBold.notificationUnread,
      name: 'Bold Notification unread icon',
    ),
    IconModel(
      icon: SolarIconsOutline.notificationUnread,
      name: 'Outline Notification unread icon',
    ),
    IconModel(icon: SolarIconsBold.document, name: 'Bold Document icon'),
    IconModel(icon: SolarIconsOutline.document, name: 'Outline Document icon'),
    IconModel(icon: SolarIconsBold.sendSquare, name: 'Bold Send Square icon'),
    IconModel(
      icon: SolarIconsOutline.sendSquare,
      name: 'Outline Send Square icon',
    ),
    IconModel(icon: SolarIconsBold.heart, name: 'Bold Heart icon'),
    IconModel(icon: SolarIconsOutline.heart, name: 'Outline Heart icon'),
    IconModel(icon: SolarIconsBold.cupHot, name: 'Bold Cup Hot icon'),
    IconModel(icon: SolarIconsOutline.cupHot, name: 'Outline Cup Hot icon'),
    IconModel(icon: SolarIconsBold.palette, name: 'Bold Palette icon'),
    IconModel(icon: SolarIconsOutline.palette, name: 'Outline Palette icon'),
    IconModel(icon: SolarIconsBold.diploma, name: 'Bold Diploma icon'),
    IconModel(icon: SolarIconsOutline.diploma, name: 'Outline Diploma icon'),
    IconModel(icon: SolarIconsBold.fire, name: 'Bold Fire icon'),
    IconModel(icon: SolarIconsOutline.fire, name: 'Outline Fire icon'),
    IconModel(
      icon: SolarIconsBold.userRounded,
      name: 'Bold User Rounded icon',
    ),
    IconModel(
      icon: SolarIconsOutline.userRounded,
      name: 'Outline User Rounded icon',
    ),
    IconModel(
      icon: SolarIconsBold.textCrossCircle,
      name: 'Bold Text Cross Circle icon',
    ),
    IconModel(
      icon: SolarIconsOutline.textCrossCircle,
      name: 'Outline Text Cross Circle icon',
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: GridView.builder(
        itemCount: icons.length,
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 8,
        ),
        itemBuilder: (BuildContext context, int index) {
          return Card(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Icon(icons[index].icon, size: 50.0),
                const SizedBox(height: 30.0),
                Text(icons[index].name, textAlign: TextAlign.center),
              ],
            ),
          );
        },
      ),
    );
  }
}

class IconModel {
  final IconData icon;
  final String name;

  const IconModel({required this.icon, required this.name});
}
