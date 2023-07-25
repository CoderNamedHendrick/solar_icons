import 'package:flutter_test/flutter_test.dart';
import 'package:solar_icons/solar_icons.dart';

void main() {
  group(SolarIconsBold, () {
    test('Test bold icons are generated', () {
      String fontFamily = 'SolarIconsBold';
      SolarIconsData icon = SolarIconsData(0xe900, fontFamily: fontFamily);
      expect(icon, equals(SolarIconsBold.forward));
      expect(icon.codePoint, 0xe900);
      expect(icon.fontFamily, SolarIconsBold.forward.fontFamily);
    });
  });

  group(SolarIconsOutline, () {
    test('Test that outline icons are generated', () {
      String fontFamily = 'SolarIconsOutline';
      SolarIconsData icon = SolarIconsData(0xe900, fontFamily: fontFamily);
      expect(icon, equals(SolarIconsOutline.forward));
      expect(icon.codePoint, 0xe900);
      expect(icon.fontFamily, SolarIconsOutline.forward.fontFamily);
    });
  });

  group(SolarIconsBroken, () {
    test('Test that broken icons are generated', () {
      String fontFamily = 'SolarIconsBroken';
      SolarIconsData icon = SolarIconsData(0xe900, fontFamily: fontFamily);
      expect(icon, equals(SolarIconsBroken.multipleForwardLeft));
      expect(icon.codePoint, 0xe900);
      expect(icon.fontFamily, SolarIconsBroken.multipleForwardLeft.fontFamily);
    });
  });
}
