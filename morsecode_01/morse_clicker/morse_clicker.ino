/*
 * Author: Jørgen Bele Reinfjell
 * Date: 26.08.2019 [dd.mm.yyyy]
 * File: morse_clicker.ino
 * Description:
 *   Arduino code for assignment 1 of Plab2 2019
 */
#include <SPI.h>

#include "led.h"

enum {
  DASH_LED_PIN =  8, /* GREEN */
  DOT_LED_PIN  =  9, /*  RED  */
  BTN_PIN      = 10,
};

LED dot_led = LED(DOT_LED_PIN);
LED dash_led = LED(DASH_LED_PIN);

unsigned long start_press = 0;    // ms of press start
unsigned long start_release = 0;  // ms of release start
bool prev_pressed = false;        // pressed state at last loop iter
bool did_print_pause = false;     // state variable, see comment in loop()
bool has_started = false;         // state variable used to busy loop until first button press.

void setup()
{
  Serial.begin(9600);

  pinMode(BTN_PIN, INPUT);
  dot_led.init();
  dash_led.init();

  dot_led.set(LED::OFF);
  dash_led.set(LED::OFF);

  start_press = start_release = millis();

  // Print a welcome message.
  Serial.print("011020100201210002001112320120002000200211021021120210212320111123211211120102000202321010211121002023");
}

//#define T 300
#define T 50
//#define LONG_PAUSE 20*T
#define LONG_PAUSE 40*T
#define MEDIUM_PAUSE 4.5*T
#define SHORT_PAUSE 1.5*T

#define DASH_DURATION 3*T
#define DOT_DURATION T
#define RESET_DURATION 1000

#define DOT_STR "0"
#define DASH_STR "1"
#define MEDIUM_PAUSE_STR "2"
#define LONG_PAUSE_STR "3"
#define RESET_STR "4"

#define PRINTOUT Serial.print

void loop()
{
  bool pressed = digitalRead(BTN_PIN) == HIGH;
  if (!has_started) {
    // simplify code: start on first press
    while (!pressed) {
      pressed = digitalRead(BTN_PIN) == HIGH;
    }
    has_started = true;
  }

  // check if the delay period for a long pause
  // has been exceeded and print it now if not already
  // done previously. This is needed to make sure that
  // the pause is written to output without needing to
  // wait until next the button press.
  unsigned long now = millis();
  if (!did_print_pause && !prev_pressed && !pressed) {
    unsigned long release_duration = now - start_release;

    if (release_duration >= LONG_PAUSE) {
      PRINTOUT(LONG_PAUSE_STR);
      did_print_pause = true;
    }
  }

  // send a reset string when the button is pressed down for
  // longer than RESET_DURATION and reset current state.
  if (!did_print_pause && prev_pressed && pressed && now - start_press > RESET_DURATION) {
    PRINTOUT(RESET_STR);
    did_print_pause = true;
    start_press = 0;
    start_release = 0;
    prev_pressed = false;
    did_print_pause = false;
    has_started = false;
    return;
  }

  if (pressed && !prev_pressed) {
    start_press = now; // start of press
    did_print_pause = false;

    unsigned long release_duration = now - start_release;
    if (release_duration >= MEDIUM_PAUSE) {
      PRINTOUT(MEDIUM_PAUSE_STR);
    }

  } else if (!pressed && prev_pressed) {

    start_release = millis(); // end of press

    // Check if this is a dot or a dash, set leds and
    // print to serial accordingly
    unsigned long press_duration = start_release - start_press;
    if (press_duration >= DASH_DURATION) {
      PRINTOUT(DASH_STR);
      dash_led.set(LED::ON);
      dot_led.set(LED::OFF);
    } else if (press_duration >= DOT_DURATION) {
      PRINTOUT(DOT_STR);
      dash_led.set(LED::OFF);
      dot_led.set(LED::ON);
    }
  }
  prev_pressed = pressed;
}
