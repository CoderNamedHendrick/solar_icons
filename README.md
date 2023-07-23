<!--
This README describes the package. If you publish this package to pub.dev,
this README's contents appear on the landing page for your package.

For information about how to write a good package README, see the guide for
[writing package pages](https://dart.dev/guides/libraries/writing-package-pages).

For general information about developing packages, see the Dart guide for
[creating packages](https://dart.dev/guides/libraries/create-library-packages)
and the Flutter guide for
[developing packages and plugins](https://flutter.dev/developing-packages).
-->
[![codecov](https://codecov.io/gh/CoderNamedHendrick/solar_icons/branch/master/graph/badge.svg)](https://codecov.io/gh/CoderNamedHendrick/solar_icons)
[![Test](https://github.com/CoderNamedHendrick/solar_icons/actions/workflows/test.yaml/badge.svg?branch=master)](https://github.com/CoderNamedHendrick/solar_icons/actions/workflows/test.yaml)
[![pub package](https://img.shields.io/pub/v/solar_icons.svg?color=success&style=flat-square)](https://pub.dartlang.org/packages/solar_icons)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-success.svg?style=flat-square)](https://github.com/CoderNamedHendrick/solar_icons/pulls)

# SolarIcons
Solar Icons is Solar icons which is 7000+ icons in different styles or 1200+ icons for each style available as a dart/flutter package.

Made from [SolarIcons](https://www.figma.com/community/file/1166831539721848736).

## 🏅 Installation
Update dependencies of your pubspec.yaml, add the following line

```yaml
solar_icons: 
```

## 🏗️ Usage

```dart
import 'package:solar_icons/solar_icons.dart';
import 'package:flutter/material.dart';

class IconWidget extends StatelessWidget {
  
  
  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(SolarIconsBold.notificationUnread),
          const SizedBox(height: 10),
          Text('Bold Notification unread Icon')
        ],
      ),
    );
  }
}
```

## Example

View the flutter app in the `example` directory

## Screenshot

<img src="https://raw.githubusercontent.com/CoderNamedHendrick/solar_icons/master/ss/example.png" alt="example screenshot">

## 🐛 Bugs/Requests

If you encounter any problems feel free to open an issue. If you feel the library is
missing a feature, please raise a ticket on GitHub and I'll look into it.
Pull request are also welcome.

## 🤓 Developer(s)

[<img src="https://github.com/CoderNamedHendrick.png" width="180" />](https://github.com/CoderNamedHendrick)
#### **Sebastine Odeh**
<p>
<a href="https://twitter.com/H3ndrick_"><img src="https://github.com/aritraroy/social-icons/blob/master/twitter-icon.png?raw=true" width="60"></a>
<a href="https://www.linkedin.com/in/sebastine-odeh-1081a318b/"><img src="https://github.com/aritraroy/social-icons/blob/master/linkedin-icon.png?raw=true" width="60"></a>
<a href="https://medium.com/@sebastinesoacatp"><img src="https://github.com/aritraroy/social-icons/blob/master/medium-icon.png?raw=true" width="60"></a>
</p>