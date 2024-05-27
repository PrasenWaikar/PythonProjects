#include <U8g2lib.h>

U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

void setup() {
  u8g2.begin();
}

void drawArc(int cx, int cy, int r, int thickness, int start_angle, int end_angle, int offset) {
  for (int i = 0; i < thickness * 2; i++) { // Double the thickness
    int radius = r + i / 2; // Increase the radius by half the thickness
    int start = start_angle;
    int end = end_angle;

    while (start <= end) {
      float rad = start * 3.141592 / 180;
      int px = cx + int(radius * cos(rad));
      int py = cy + int(radius * sin(rad)) - offset; // Apply vertical offset
      u8g2.drawPixel(px, py);
      start++;
    }
  }
}

void loop() {
  u8g2.clearBuffer();          // clear the internal memory

  // Draw a wider and double thickness smiley arc at the center of the display
  drawArc(u8g2.getWidth() / 2, u8g2.getHeight() / 15 - 2, 48, 7, 32, 145, 2); // Arc centered at the middle of the display with a small vertical offset

  u8g2.sendBuffer();           // transfer internal memory to the display
  delay(1000);                 // delay for a second
}
