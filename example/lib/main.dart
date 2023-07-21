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
      icon: SolarIconsBold.Notification_Unread,
      name: 'Bold Notification Unread icon',
    ),
    IconModel(
      icon: SolarIconsOutline.Notification_Unread,
      name: 'Outline Notification Unread icon',
    ),
    IconModel(icon: SolarIconsBold.Document, name: 'Bold Document icon'),
    IconModel(icon: SolarIconsOutline.Document, name: 'Outline Document icon'),
    IconModel(icon: SolarIconsBold.Send_Square, name: 'Bold Send Square icon'),
    IconModel(
      icon: SolarIconsOutline.Send_Square,
      name: 'Outline Send Square icon',
    ),
    IconModel(icon: SolarIconsBold.Heart, name: 'Bold Heart icon'),
    IconModel(icon: SolarIconsOutline.Heart, name: 'Outline Heart icon'),
    IconModel(icon: SolarIconsBold.Cup_Hot, name: 'Bold Cup Hot icon'),
    IconModel(icon: SolarIconsOutline.Cup_Hot, name: 'Outline Cup Hot icon'),
    IconModel(icon: SolarIconsBold.Palette, name: 'Bold Palette icon'),
    IconModel(icon: SolarIconsOutline.Palette, name: 'Outline Palette icon'),
    IconModel(icon: SolarIconsBold.Diploma, name: 'Bold Diploma icon'),
    IconModel(icon: SolarIconsOutline.Diploma, name: 'Outline Diploma icon'),
    IconModel(icon: SolarIconsBold.Fire, name: 'Bold Fire icon'),
    IconModel(icon: SolarIconsOutline.Fire, name: 'Outline Fire icon'),
    IconModel(
      icon: SolarIconsBold.User_Rounded,
      name: 'Bold User Rounded icon',
    ),
    IconModel(
      icon: SolarIconsOutline.User_Rounded,
      name: 'Outline User Rounded icon',
    ),
    IconModel(
      icon: SolarIconsBold.Text_Cross_Circle,
      name: 'Bold Text Cross Circle icon',
    ),
    IconModel(
      icon: SolarIconsOutline.Text_Cross_Circle,
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
