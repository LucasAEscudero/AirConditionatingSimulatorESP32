# ❄️ Air Conditioner Simulator (FSM) with ESP32 / ESP32-C3

This project simulates the behavior of an **air conditioner** using a **Finite State Machine (FSM)** implemented in **MicroPython**, running on **ESP32** or **ESP32-C3** boards. It connects to **Adafruit IO** using **MQTT** to remotely monitor and control temperature settings.

---

## ▶️ Wokwi Simulations

- **ESP32:** [View Simulation](https://wokwi.com/projects/436400312573176833)
- **ESP32-C3:** [View Simulation](https://wokwi.com/projects/436032823973740545)

---

## 🔧 Features

- NTC thermistor sensor (simulated via ADC).
- FSM-based control with 3 states:
  - **Cooling** (fan on via PWM)
  - **Ideal** (target temperature)
  - **Heating** (below threshold)
- Adjustable temperature threshold via MQTT.
- Real-time status reporting to Adafruit IO dashboard.
- Actuators represented using LEDs and a PWM output.
- NTC temperature calculate using the simplified B-parameter equation, derived from the Steinhart-Hart model

---

## 📡 MQTT Setup with Adafruit IO

The following MQTT feeds are used:

| Feed                          | Description                      |
|-------------------------------|----------------------------------|
| `lucasescud/feeds/NTCSensor`         | Current temperature readings     |
| `lucasescud/feeds/TempUmbral`        | Current temperature threshold    |
| `lucasescud/feeds/TempUmbralControl` | External control of threshold (`1`, `-1`, or `0`) |

> ⚠️ **Important:** `TempUmbralControl` must send integer values `1`, `-1`, or `0`.

---

## ⚙️ Requirements

- ESP32 or ESP32-C3 with MicroPython firmware.
- Internet access (Wi-Fi).
- [Adafruit IO account](https://io.adafruit.com/).
- MQTT support via `umqtt.simple`.

---

## 🔐 Adafruit IO Credentials (⚠️ Required)

Before running the code, **you must configure the Adafruit IO password (AIO Key)**.

> ✅ The script expects the AIO Key to be available in an **environment variable** named: ADAFRUIT_IO_KEY
> 
If you're running the script on a local computer or using a tool like Thonny, make sure to set the environment variable appropriately. For example:

**Linux/macOS:**
```bash
export ADAFRUIT_IO_KEY="your-adafruit-aio-key"
```
**Windows (CMD):**
```bash
set ADAFRUIT_IO_KEY=your-adafruit-aio-key
```
**Windows (PowerShell):**
```bash
$env:ADAFRUIT_IO_KEY = "your-adafruit-aio-key"
```
