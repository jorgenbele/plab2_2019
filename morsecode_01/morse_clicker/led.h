/*
 * Author: Jørgen Bele Reinfjell
 * Date: 26.08.2019 [dd.mm.yyyy]
 * File: led.h
 * Description:
 *   Class used to simplify use of LEDs on the arduino.
 */

#ifndef __LED_H_
#define __LED_H_

enum { LED_STATUS_FAILURE = 0, LED_STATUS_OK = 1,
       LED_STATUS_WAITING = 2, LED_STATUS_NO_CHANGE = 3,
       LED_STATUS_NO_SLOTS = 4                           };

class LED
{
public:

  enum LED_state { ON = HIGH, OFF = LOW };

  LED(uint8_t pin) { this->pin = pin; }

  void init(void) { pinMode(pin, OUTPUT); cur_state = OFF; }

  void set(enum LED_state state) {
    if (cur_state == state) return;
    digitalWrite(pin, state);
    cur_state = state;
  }

  void toggle()
  {
    if (cur_state == ON) cur_state = OFF;
    else                 cur_state = ON;
    digitalWrite(pin, cur_state);
  }

private:
  uint8_t pin;
  enum LED_state cur_state;
};

#endif // __LED_H_
