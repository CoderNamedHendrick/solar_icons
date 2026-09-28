import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:solar_icons/solar_icons.dart';

const fontPackage = 'solar_icons';
const fontFamily = 'SolarIcons';

void main() {
  group(SolarIconsBold, () {
    test('Test bold icons are generated', () {
      const icon = IconData(0xe000, fontFamily: fontFamily, fontPackage: fontPackage);

      expect(icon, equals(SolarIconsBold.forward));
      expect(icon.codePoint, 0xe000);
      expect(icon.fontFamily, SolarIconsBold.forward.fontFamily);
    });
  });

  group(SolarIconsOutline, () {
    test('Test that outline icons are generated', () {
      const icon = IconData(0xea00, fontFamily: fontFamily, fontPackage: fontPackage);
      expect(icon, equals(SolarIconsOutline.forward));
      expect(icon.codePoint, 0xea00);
      expect(icon.fontFamily, SolarIconsOutline.forward.fontFamily);
    });
  });

  group(SolarIconsBroken, () {
    test('Test that broken icons are generated', () {
      const icon = IconData(0xe500, fontFamily: fontFamily, fontPackage: fontPackage);
      expect(icon, equals(SolarIconsBroken.multipleForwardLeft));
      expect(icon.codePoint, 0xe500);
      expect(icon.fontFamily, SolarIconsBroken.multipleForwardLeft.fontFamily);
    });
  });
}
