// Example 4 - Receive a number as text and convert it to an int
#include <FastLED.h>

#define LED_PIN     11
#define NUM_LEDS    299
#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];
extern CRGBPalette16 myRedWhiteBluePalette;
extern const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM;

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;

int dataNumber = 0;             // new for this version

void setup() {
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
}

void loop() {
    recvWithEndMarker();
    showNewNumber();
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
    
    if (Serial.available() > 0) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}
int r,g,b;

void showNewNumber() {
    if (newData == true) {
        dataNumber = 0;             // new for this version
        dataNumber = atoi(receivedChars);   // new for this version
        Serial.print("This just in ... ");
        Serial.println(receivedChars);
        newData = false;
        r=(receivedChars[0]-'0')*100+(receivedChars[1]-'0')*10+(receivedChars[2]-'0');
        g=(receivedChars[3]-'0')*100+(receivedChars[4]-'0')*10+(receivedChars[5]-'0');
        b=(receivedChars[6]-'0')*100+(receivedChars[7]-'0')*10+(receivedChars[8]-'0');
        Serial.println(r);
        for( int i = 0; i < 100; ++i) {
          leds[i].setRGB(r,0,0);
        }
        for( int i = 100; i < 200; ++i) {
          leds[i].setRGB(0,g,0);
        }
        for( int i = 200; i <300; ++i) {
          leds[i].setRGB(0,0,b);
        }
        FastLED.show();
    }

}