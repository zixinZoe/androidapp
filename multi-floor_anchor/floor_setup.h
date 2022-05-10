

/*
   Copyright (c) 2020 by Ashutosh Dhekne <dhekne@gatech.edu>
   Peer-peer protocol

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


   @file PeerProtocol_test01.ino


*/

#include <SPI.h>
#include <math.h>
//#include <DW1000.h>
//#include "ProtocolConsts.h"
#include "genericFunctions.h"
#include "RangingContainer.h"
#include "Neighbor.h"
#include "Adafruit_LSM9DS1.h"
#include <SdFat.h>

//#include "sdios.h"
#include <time.h>
#include <TimeLib.h>
#include "RTClib.h"
#include <Wire.h>
//#include<chrono>
//#include<iostream>

#define VBATPIN A2
#define LED_PIN 12
#define NOISE_PIN 11
#define GOOD_PIN 6
#define SILENCE_PIN 5
#define DEV_INDICATOR_PIN 13
// Yunzhi CIR Code
#define NCIR_FULL 1016
#define RX_TIME_FP_INDEX_OFFSET 5
int packet_count = 1;
int packet_type = 0;

int AlarmNoise = 0; // = rx_packet[LED_IDX] & 0x01;
int AlarmLed = 0;   // = rx_packet[LED_IDX] & 0x02;

#define INIT_RTC_ALWAYS 0

#define SWITCH_INITIATOR 1
#define PRINT_CIR 0
#define USB_CONNECTION 0
//#define INITIATOR 1         /******CHANGE THIS******/
int INITIATOR = 0;
#define IGNORE_IMU 1
Adafruit_LSM9DS1 lsm = Adafruit_LSM9DS1();
#define IMU_READINGS_MAX 18 * 4
byte imu_buffer[IMU_READINGS_MAX];
#define IMU_SINGLE_READING_BUFF_SIZE 6
int disable_imu = 1;
// int chck =2390;

#define DEBUG_PRINT 1
// connection pins
#define OUR_UWB_FEATHER 1
#define AUS_UWB_FEATHER 0

#if (OUR_UWB_FEATHER == 1)
const uint8_t PIN_RST = 9;  // reset pin
const uint8_t PIN_IRQ = 17; // irq pin
const uint8_t PIN_SS = 19;  // spi select pin
#endif

// DEBUG packet sent status and count
volatile boolean received = false;
volatile boolean error = false;
volatile int16_t numReceived = 0; // todo check int type
volatile boolean sendComplete = false;
volatile boolean RxTimeout = false;
String message;

byte beep_msg[MAX_BEEP_LEN] = {BEEP_MSG_TYPE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; // for assigning group id
// byte tx_poll_msg[MAX_POLL_LEN] = {POLL_MSG_TYPE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
// byte rx_resp_msg[MAX_RESP_LEN] = {RESP_MSG_TYPE, 0x02, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
// byte tx_final_msg[MAX_FINAL_LEN] = {FINAL_MSG_TYPE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
// byte exchange_msg[MAX_EXCHANGE_LEN] = {EXCHANGE_MSG_TYPE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
// byte start_msg[MAX_START_LEN] = {START_MSG_TYPE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

// only consider same floor for now
int round = 0;

// to be determined
int start_beep = 0;

if (myDevID == 0)
{
  start_beep = 1;
}

std::multimap<int, int> rounds;

uint8_t pw_threshold = 95;

Ranging thisRange;

// char rx_msg_char[200];
byte rx_packet[128];
// uint8_t myAcc[1000];

typedef enum states
{
  STATE_BEEP,
  STATE_TIGHT_LOOP,
  STATE_PRESYNC,
  STATE_SYNC,
  STATE_ANCHOR,
  STATE_TAG,
  STATE_FIRST_START,
  STATE_OBLIVION,
} STATES;

volatile uint8_t current_state = STATE_BEEP;
// volatile uint8_t current_state = STATE_WAIT;
unsigned long silenced_at = 0;
#define SILENCE_PERIOD 120
long randNumber;
int currentSlots = 8;

// Timer for implementing timeouts
#define CPU_HZ 48000000
#define TIMER_PRESCALER_DIV 1024

void startTimer(int frequencyHz);
void setTimerFrequency(int frequencyHz);

void TC3_Handler();

#define MAX_TIMEOUTS 2
volatile boolean timeout_established[MAX_TIMEOUTS];
volatile boolean timeout_triggered[MAX_TIMEOUTS];
volatile boolean timeout_overflow[MAX_TIMEOUTS];
volatile uint64_t timeout_time[MAX_TIMEOUTS];

SdFat sd;
SdFile store_distance; // The root file system useful for deleting all files on the SDCard
char filename[14];
int filenum = 0;
int entries_in_file = 0;
int SDChipSelect = 10;

int SDEnabled = 1;
int SDLOG = 0;

#define DIST_ALARM 1500
#define DIST_WARN 2500

// Time
RTC_PCF8523 rtc;

void receiver(uint16_t rxtoval = 0)
{
  received = false;
  DW1000.newReceive();
  DW1000.setDefaults();
  // we cannot don't need to restart the receiver manually
  DW1000.receivePermanently(false);
  if (rxtoval > 0)
  {
    DW1000.setRxTimeout(rxtoval);
  }
  else
  {
    // Serial.print("Resetting Timeout to  ");
    // Serial.println(rxtoval);
    DW1000.setRxTimeout(rxtoval);
  }
  DW1000.startReceive();
  // Serial.println("Started Receiver");
}

void setup()
{
  pinMode(LED_PIN, OUTPUT);
  pinMode(NOISE_PIN, OUTPUT);
  pinMode(GOOD_PIN, OUTPUT);
  pinMode(DEV_INDICATOR_PIN, OUTPUT);
  pinMode(SILENCE_PIN, INPUT_PULLUP);
  digitalWrite(GOOD_PIN, HIGH);
  analogReadResolution(10);
  // DEBUG monitoring
  Serial.begin(115200);
  while (!Serial)
  {
    delay(10);
#if (USB_CONNECTION == 0)
    break;
#endif
  }
  Serial.print("Waiting...");
  delay(5000);
  Serial.print("Should see this...");
  // Setting up the RTC Clock
  if (!rtc.begin())
  {
    Serial.println("Couldn't find RTC");
    // while (1);
  }

  if (!rtc.initialized())
  {
    Serial.println("RTC is NOT running!");
    // following line sets the RTC to the date & time this sketch was compiled
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    Serial.println("Setting new time");
    // This line sets the RTC with an explicit date & time, for example to set
    // January 21, 2014 at 3am you would call:
    rtc.adjust(DateTime(2020, 10, 17, 19, 40, 0));
  }

  // In production, INIT_RTC_ALWAYS should be 0.
  // Only turn this to 1 when testing
#if (INIT_RTC_ALWAYS == 1)
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
#endif
  // rtc.adjust(DateTime(2019, 11, 13, 10, 06, 00));
  // SoftRTC.begin(rtc.now());  // Initialize SoftRTC to the current time

  // while(1) {
  Serial.println("Current Time");
  DateTime now = rtc.now();
  Serial.print(now.year());
  Serial.print("/");
  Serial.print(now.month());
  Serial.print("/");
  Serial.print(now.day());
  Serial.print(" ");
  Serial.print(now.hour());
  Serial.print(":");
  Serial.print(now.minute());
  Serial.print(":");
  Serial.print(now.second());
  delay(1000);
  //}
  Serial.print("Initializing SD card...");
  // delay(1000);
  if (!sd.begin(SDChipSelect, SPI_FULL_SPEED))
  {
    Serial.println("SDCard Initialization failed!");
    SDEnabled = 0;
  }
  else
  {
    Serial.println("SDCard Initialization done.");
    SDEnabled = 1;
  }

  if (SDEnabled == 1)
  {
    myDevID = SDGetline();
    Serial.print("myDevID");
    Serial.println(myDevID);
  }

  if (SDEnabled == 1)
  {
    sprintf(filename, "dist%03d.txt", filenum);
    if (!store_distance.open(filename, O_WRITE | O_CREAT))
    {
      Serial.println("Could not create file");
      delay(10000);
    }

    Serial.println(filename);
  }
  randomSeed(analogRead(0));
  Serial.println(F("Peer-peer ranging protocol"));
  Serial.println("Free memory: ");
  Serial.println(freeMemory());
  // initialize the driver
  DW1000.begin(PIN_IRQ, PIN_RST);
  DW1000.select(PIN_SS);
  Serial.println(F("DW1000 initialized ..."));
  // general configuration
  DW1000.newConfiguration();
  DW1000.setDefaults();
  DW1000.setDeviceAddress(6);
  DW1000.setNetworkId(10);
  DW1000.enableMode(DW1000.MODE_LONGDATA_RANGE_LOWPOWER);
  DW1000.commitConfiguration();
  Serial.println(F("Committed configuration ..."));
  // DEBUG chip info and registers pretty printed
  char msg[128];
  DW1000.getPrintableDeviceIdentifier(msg);
  Serial.print("Device ID: ");
  Serial.println(msg);
  DW1000.getPrintableExtendedUniqueIdentifier(msg);
  Serial.print("Unique ID: ");
  Serial.println(msg);
  DW1000.getPrintableNetworkIdAndShortAddress(msg);
  Serial.print("Network ID & Device Address: ");
  Serial.println(msg);
  DW1000.getPrintableDeviceMode(msg);
  Serial.print("Device mode: ");
  Serial.println(msg);
  // attach callback for (successfully) received messages
  DW1000.attachReceivedHandler(handleReceived);
  DW1000.attachReceiveTimeoutHandler(handleRxTO);
  DW1000.attachReceiveFailedHandler(handleError);
  DW1000.attachErrorHandler(handleError);
  DW1000.attachSentHandler(handleSent);
  // start reception

  for (int i = 0; i < MAX_TIMEOUTS; i++)
  {
    timeout_established[i] = false;
    timeout_triggered[i] = false;
    timeout_overflow[i] = false;
    timeout_time[i] = 0;
  }

  if (INITIATOR)
  {

    while (!lsm.begin())
    {
      Serial.println("Oops ... unable to initialize the LSM9DS1. Check your wiring!");
      delay(1000);
#if IGNORE_IMU == 1
      disable_imu = 1;
      break;
#endif
    }
    if (disable_imu == 0)
    {
      Serial.println("Found LSM9DS1 9DOF");
      // 1.) Set the accelerometer range
      lsm.setupAccel(lsm.LSM9DS1_ACCELRANGE_2G);
      // 2.) Set the magnetometer sensitivity
      lsm.setupMag(lsm.LSM9DS1_MAGGAIN_4GAUSS);
      // 3.) Setup the gyroscope
      lsm.setupGyro(lsm.LSM9DS1_GYROSCALE_245DPS);
    }
  }
  //#endif
}

void handleSent()
{
  // status change on sent success
  sendComplete = true;
}

void handleReceived()
{
  RX_TO_COUNT = 0;
  // status change on reception success

  DW1000.getData(rx_packet, DW1000.getDataLength());
  //  Serial.println("Received something...");
  received = true;
  Serial.println("received is true");
  //  byte2char(rx_packet, 24);
  //  Serial.println(rx_msg_char);
}

void handleError()
{
  if (current_state == STATE_RECEIVE)
  {
    current_state = STATE_RECEIVE;
  }
  else if (current_state == STATE_ANCHOR)
  {
    current_state = STATE_ANCHOR;
  }
  else if (current_state == HOLD_STATE)
  {
    current_state = HOLD_STATE;
    // receiver(60);
  }
  else
  {
    current_state = STATE_IDLE;
  }
  RxTimeout = true;
  error = true;
  Serial.println("ERROR");
}

void handleRxTO()
{
  RX_TO_COUNT++;
  Serial.println("RXTO----------------------");
  if (current_state == STATE_RESP_EXPECTED)
  {
    current_state = STATE_FINAL_SEND;
  }
  else if (current_state == STATE_ANCHOR)
  {
    current_state = STATE_ANCHOR;
  }
  else if (current_state == HOLD_STATE)
  {
    current_state = HOLD_STATE;
  }
  else if (current_state == STATE_FINAL_EXPECTED)
  {
    current_state = STATE_FINAL_EXPECTED;
  }
  else
  {
    current_state = STATE_IDLE;
  }

  RxTimeout = true;
#if (DEBUG_PRINT == 1)
#endif
}

float gravity_f = 0.0f;
uint16_t seq = 0;
uint16_t recvd_poll_seq = 0;
uint16_t recvd_resp_seq = 0;
uint16_t recvd_final_seq = 0;

volatile int unlock_waiting = 0;
long loop_counter = 0;
volatile long waiting = 0;
DW1000Time currentDWTime;
uint64_t currentTime;
uint64_t final_sent_time;
uint64_t ex_sent_time;
uint64_t init_time;
double elapsed_time;
double TIME_UNIT = 1.0 / (128 * 499.2e6); // seconds
File file;

// Haige print RX and FP power only
void print_CIR_POWER()
{
  float RX_POWER = DW1000.getReceivePower();
  float FP_POWER = DW1000.getFirstPathPower();
  char buff[70];
  sprintf(buff, "RX_Power=%f dbm, FP_Power=%f dbm", RX_POWER, FP_POWER);
  Serial.println(buff);
}

// Yunzhi CIR Code
void print_CIR()
{
  //    packet_count++;
  char buff[140];
  char long_buff[1400];

  byte firstPath[2];
  DW1000.readBytes(RX_TIME, RX_TIME_FP_INDEX_OFFSET, firstPath, 2);
  uint16_t firstpath = uint16_t(firstPath[1] << 8 | firstPath[0]);
  uint16_t firstPath_integer = (firstpath & 0xFFC0) >> 6;
  uint16_t firstPath_fraction = (firstpath & 0x003F);
  float RX_POWER = DW1000.getReceivePower();
  float FP_POWER = DW1000.getFirstPathPower();

  sprintf(buff, "FP_IDX[%d,%d,%d]   FP_POWER[%d,%f,%f]", packet_count, firstPath_integer, firstPath_fraction, packet_count, RX_POWER, FP_POWER);
  //    sprintf(buff, "FP_IDX[%d,%d,%d,%d]  FP_POWER[%d,%d,%f,%f]", packet_type,packet_count, firstPath_integer, firstPath_fraction, packet_type, packet_count,RX_POWER,FP_POWER);
  Serial.println(buff);

  uint8_t myAcc[4 * NCIR_FULL + 6];
  int starttap = 720;
  int endtap = 816;
  int16_t RealData = 0;
  int16_t ImaginaryData = 0;

  strcpy(long_buff, "CIR");
  DW1000.getAccMem(myAcc, 0, endtap + 1); // myAcc will contain 16 bit real imaginary pairs

  for (int i = starttap; i < endtap; i++)
  {
    RealData = myAcc[(i * 4) + 2] << 8 | myAcc[(i * 4) + 1];
    ImaginaryData = myAcc[(i * 4) + 4] << 8 | myAcc[(i * 4) + 3];
    // int16_t RealData = myAcc[(i * 4) + 1] << 8 | myAcc[(i * 4)];
    // int16_t ImaginaryData = myAcc[(i * 4) + 3] << 8 | myAcc[(i * 4) + 2];
    // Question
    sprintf(buff, "[%d,%d,%d,d%d]", packet_count, RealData, ImaginaryData, i + 1);
    strcat(long_buff, buff);
  }
  Serial.println(long_buff);
}

void nchoosek(int n, int k, int *out)
{
  int arr[n];
  for (int i = 0; i < n; i++)
  {
    arr[i] = i;
  }

  for (int i = 0; i < n; i++)
  {
    int pos = random(n);
    int t = arr[i];
    arr[i] = arr[pos];
    arr[pos] = t;
  }

  for (int i = 0; i < k; i++)
  {
    out[i] = arr[i];
  }
  return;
};

void print_uint64_t(uint64_t num)
{

  char rev[128];
  char *p = rev + 1;

  while (num > 0)
  {
    *p++ = '0' + (num % 10);
    num /= 10;
  }
  p--;
  /*Print the number which is now in reverse*/
  while (p > rev)
  {
    Serial.print(*p--);
  }
}

void floor_setup(struct param)
{
  int gate = &param.gate;
  int gateID = &param.gateID;
  int group_id = &param.group_id;
  std::map<int, int> group_gates = &param.group_gates;
  int backup = &param.backup;
  std::multimap<int, int> group_sequence = &param.goup_sequence;

  int myDevID = &param.myDevID;
  int myDevFloor = &param.myDevFloor;
  int FIRST_INITIATOR = &param.FIRST_INITIATOR;
  
  void loop()
  {

    if (INITIATOR == 1)
    {
      digitalWrite(LED_PIN, HIGH);
    }
    else
    {
      digitalWrite(LED_PIN, LOW);
    }

    switch (current_state)
    {

    case BEEP:
    {
      if (start_beep == 1)
      {
        Serial.println("START BEEP");
        beep_msg[SRC_IDX] = myDevID; // id of FI
        beep_msg[START_FLOOR_IDX] = myDevFloor;
        beep_msg[ROUND_IDX] = round;

        generic_send(beep_msg, MAX_BEEP_LEN, BEEP_MSG_TX_TS_IDX, SEND_DELAY_FIXED);
        while (!sendComplete)
        {
        }
        sendComplete = false;

        if (round < 5)
        {
          round = round + 1;
          current_state = BEEP;
        }
        else
        {
          beeped.push_back(myDevID);
          current_state = COLLECT;
          receiver(0);
        }
      }
      else
      {
        receiver(20);
        if (RxTimeout == true)
        { // if no one near beeps, I beep
          RxTimeout = false;
          if (RX_TO_COUNT > 20)
          {
            start_beep = 1;
            current_state = BEEP;
          }
        }
      }
      // else{
      //   current_state = EXCHANGE_BEEP;
      // }
    }

    case LISTEN:
    {
      Serial.println("STATE LISTEN");
      // use multi-map of pairs(FI_ID,RX_PW)

      if (received)
      {
        if (rx_packet[0] == BEEP_MSG_TYPE && rx_packet[START_FLOOR_IDX] == myDevFloor)
        {
          FI_ID = rx_packet[SRC_IDX];
          rx_pw = DW1000.getReceivePower();
          rx_round = rx_packet[ROUND_IDX];

          rounds.insert(std::pair<int, int>(FI_ID, rx_pw));
        }
        current_state = LISTEN;
        receiver(0);
      }
    }

    case COLLECT:
    {
      Serial.println("STATE COLLECT");
    }
    }
  }
}

bool is_in_initiator_list(uint8_t id)
{
  for (int i = 0; i < num_initiators; i++)
  {
    if (initiator_list[i] == id)
    {
      return true;
    }
  }
  return false;
}

void show_packet(byte packet[], int num)
{
#if (DEBUG_PRINT == 1)
  for (int i = 0; i < num; i++)
  {
    Serial.print(packet[i], HEX);
    Serial.print(" ");
  }
  Serial.println("");
#endif
}

void show_packet_8B(byte packet[])
{

  long msg1 = 0;
  long msg2 = 0;
#if (DEBUG_PRINT == 1)
  for (int i = 0; i < 4; i++)
  {
    msg1 = msg1 << 8;
    msg2 = msg2 << 8;
    msg1 += packet[i];
    msg2 += packet[i + 4];
  }
  Serial.print(msg1, HEX);
  Serial.println(msg2, HEX);

#endif
}

void byte2char(byte packet[], int len)
{

  const char *hex = "0123456789ABCDEF";
  char msg[200];
  int i = 0;
  for (; i < len;)
  {
    msg[2 * i] = hex[packet[i] >> 4 & 0x0F];
    msg[2 * i + 1] = hex[packet[i] & 0x0F];
    i = i + 1;
  }
  msg[2 * i] = '\0';
  strcpy(rx_msg_char, msg);
}

// Timer Functions
// Timer functions.
void setTimerFrequency(int frequencyHz)
{
  int compareValue = (CPU_HZ / (TIMER_PRESCALER_DIV * frequencyHz)) - 1;

  TcCount16 *TC = (TcCount16 *)TC3;
  // Make sure the count is in a proportional position to where it was
  // to prevent any jitter or disconnect when changing the compare value.
  TC->COUNT.reg = map(TC->COUNT.reg, 0, TC->CC[0].reg, 0, compareValue);
  TC->CC[0].reg = compareValue;
  // Serial.println(TC->COUNT.reg);
  // Serial.println(TC->CC[0].reg);
  while (TC->STATUS.bit.SYNCBUSY == 1)
    ;
}

void startTimer(int frequencyHz)
{

  REG_GCLK_CLKCTRL = (uint16_t)(GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK0 | GCLK_CLKCTRL_ID_TCC2_TC3);

  while (GCLK->STATUS.bit.SYNCBUSY == 1)
    ; // wait for sync

  TcCount16 *TC = (TcCount16 *)TC3;

  TC->CTRLA.reg &= ~TC_CTRLA_ENABLE;
  while (TC->STATUS.bit.SYNCBUSY == 1)
    ; // wait for sync

  // Use the 16-bit timer
  TC->CTRLA.reg |= TC_CTRLA_MODE_COUNT16;
  while (TC->STATUS.bit.SYNCBUSY == 1)
    ; // wait for sync

  // Use match mode so that the timer counter resets when the count matches the compare register
  TC->CTRLA.reg |= TC_CTRLA_WAVEGEN_MFRQ;
  while (TC->STATUS.bit.SYNCBUSY == 1)
    ; // wait for sync

  // Set prescaler to 1024
  TC->CTRLA.reg |= TC_CTRLA_PRESCALER_DIV1024;
  while (TC->STATUS.bit.SYNCBUSY == 1)
    ; // wait for sync

  setTimerFrequency(frequencyHz);

  // Enable the compare interrupt
  TC->INTENSET.reg = 0;
  TC->INTENSET.bit.MC0 = 1;

  NVIC_SetPriority(TC3_IRQn, 3);
  NVIC_EnableIRQ(TC3_IRQn);

  TC->CTRLA.reg |= TC_CTRLA_ENABLE;
  while (TC->STATUS.bit.SYNCBUSY == 1)
    ; // wait for sync
}

void collect_imu_data(byte *imu_buff, int *imu_buffer_counter)
{
  if (disable_imu == 0)
  {
    lsm.readBuffer(XGTYPE, 0x80 | lsm.LSM9DS1_REGISTER_OUT_X_L_XL, IMU_SINGLE_READING_BUFF_SIZE, &imu_buff[(*imu_buffer_counter)]);
    (*imu_buffer_counter) += IMU_SINGLE_READING_BUFF_SIZE;

    lsm.readBuffer(MAGTYPE, 0x80 | lsm.LSM9DS1_REGISTER_OUT_X_L_M, IMU_SINGLE_READING_BUFF_SIZE, &imu_buff[(*imu_buffer_counter)]);
    (*imu_buffer_counter) += IMU_SINGLE_READING_BUFF_SIZE;

    lsm.readBuffer(XGTYPE, 0x80 | lsm.LSM9DS1_REGISTER_OUT_X_L_G, IMU_SINGLE_READING_BUFF_SIZE, &imu_buff[(*imu_buffer_counter)]);
    (*imu_buffer_counter) += IMU_SINGLE_READING_BUFF_SIZE;
  }
  else
  {
    (*imu_buffer_counter) += IMU_SINGLE_READING_BUFF_SIZE * 3;
  }
}

void set_imu_data(float data[], int type)
{
  float ax, ay, az;
  float acc_unit = 2 * 9.8 / 32768;
  float mag_unit = 0.14;
  float gyro_unit = 0.00875;
  int unit = 1;
  int imu_idx = 6 * type;
  if (type == 0)
  {
    data[0] = (int16_t)((imu_buffer[0 + imu_idx] + ((int16_t)imu_buffer[1 + imu_idx] << 8))) * acc_unit;
    data[1] = (int16_t)((imu_buffer[2 + imu_idx] + ((int16_t)imu_buffer[3 + imu_idx] << 8))) * acc_unit;
    data[2] = (int16_t)((imu_buffer[4 + imu_idx] + ((int16_t)imu_buffer[5 + imu_idx] << 8))) * acc_unit;
  }
  else if (type == 1)
  {
    data[0] = (int16_t)((imu_buffer[0 + imu_idx] + ((int16_t)imu_buffer[1 + imu_idx] << 8))) * mag_unit;
    data[1] = (int16_t)((imu_buffer[2 + imu_idx] + ((int16_t)imu_buffer[3 + imu_idx] << 8))) * mag_unit;
    data[2] = (int16_t)((imu_buffer[4 + imu_idx] + ((int16_t)imu_buffer[5 + imu_idx] << 8))) * mag_unit;
  }
  else
  {
    data[0] = (int16_t)((imu_buffer[0 + imu_idx] + ((int16_t)imu_buffer[1 + imu_idx] << 8))) * gyro_unit;
    data[1] = (int16_t)((imu_buffer[2 + imu_idx] + ((int16_t)imu_buffer[3 + imu_idx] << 8))) * gyro_unit;
    data[2] = (int16_t)((imu_buffer[4 + imu_idx] + ((int16_t)imu_buffer[5 + imu_idx] << 8))) * gyro_unit;
  }
}

void TC3_Handler()
{
  DW1000Time currectTS;
  uint64_t currentUWBTime;
  for (int i = 0; i < MAX_TIMEOUTS; i++)
  {
    if (timeout_established[i])
    {
      DW1000.getSystemTimestamp(currectTS);
      currentUWBTime = currectTS.getTimestamp();
      break; // Any timeout if established will populate the currentUWBTime
    }
  }
  for (int i = 0; i < MAX_TIMEOUTS; i++)
  {
    if (timeout_established[i])
    {
      if (currentUWBTime > timeout_time[i])
      {
        timeout_established[i] = false;
        timeout_time[i] = INFINITE_TIME;
        timeout_overflow[i] = false;
        timeout_triggered[i] = true;
      }
      else if (timeout_overflow[i] == true && currentUWBTime > (timeout_time[i] - 2 ^ 40))
      {
        timeout_established[i] = false;
        timeout_time[i] = INFINITE_TIME;
        timeout_overflow[i] = false;
        timeout_triggered[i] = true;
      }
    }
  }
}

void set_timeout(int whichTO, uint32_t delayTime)
{
  DW1000Time currectTS;
  uint64_t currentUWBTime;
  DW1000.getSystemTimestamp(currectTS);
  currentUWBTime = currectTS.getTimestamp();
  DW1000Time deltaTime = DW1000Time(delayTime, DW1000Time::MILLISECONDS);
  timeout_time[whichTO] = (currectTS + deltaTime).getTimestamp();
  if (timeout_time[whichTO] > 2 ^ 40)
  {
    timeout_overflow[whichTO] = true;
  }
  else
  {
    timeout_overflow[whichTO] = false;
  }
}

double get_time_us()
{
  DW1000.getSystemTimestamp(currentDWTime);
  currentTime = currentDWTime.getTimestamp();
  return currentTime * TIME_UNIT * 1e6;
}

uint64_t get_time_u64()
{
  DW1000.getSystemTimestamp(currentDWTime);
  return currentDWTime.getTimestamp();
}

// Utility functions
void dateTime(uint16_t *date, uint16_t *time_)
{
  DateTime now = rtc.now();
  // return date using FAT_DATE macro to format fields
  *date = FAT_DATE(now.year(), now.month(), now.day());

  // return time using FAT_TIME macro to format fields
  *time_ = FAT_TIME(now.hour(), now.minute(), now.second());
  printDateTime();
}

float getVoltage()
{

  float measuredvbat = analogRead(VBATPIN);
  measuredvbat *= 2;    // we divided by 2, so multiply back
  measuredvbat *= 3.3;  // Multiply by 3.3V, our reference voltage
  measuredvbat /= 1024; // convert to voltage
  return measuredvbat;
}

void printDateTime()
{
  DateTime now = rtc.now();
  Serial.print(now.year());
  Serial.print("/");
  Serial.print(now.month());
  Serial.print("/");
  Serial.print(now.day());
  Serial.print(" ");
  Serial.print(now.hour());
  Serial.print(":");
  Serial.print(now.minute());
  Serial.print(":");
  Serial.println(now.second());
}

#ifdef __arm__
// should use uinstd.h to define sbrk but Due causes a conflict
extern "C" char *sbrk(int incr);
#else  // __ARM__
extern char *__brkval;
#endif // __arm__

int freeMemory()
{
  char top;
#ifdef __arm__
  return &top - reinterpret_cast<char *>(sbrk(0));
#elif defined(CORE_TEENSY) || (ARDUINO > 103 && ARDUINO != 151)
  return &top - __brkval;
#else  // __arm__
  return __brkval ? &top - __brkval : &top - __malloc_heap_start;
#endif // __arm__
}

int SDGetline()
{

  File myfile = sd.open("ID.txt");
  int ret = -1;
  if (myfile)
  {
    ret = myfile.read() - '0';
    myfile.close();
  }
  else
  {
    Serial.println("error opening ID.txt");
  }
  //  Serial.println("SDGetLineresult:");
  //  Serial.print(ret);
  return ret;
}
