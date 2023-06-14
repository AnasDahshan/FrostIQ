# FrostIQ

<!-- [![Watch the video]] -->
https://github.com/AnasDahshan/FrostIQ/assets/107579439/2b226819-c8de-432f-8c6d-fdc4eb76abb1

FrostIQ is a device designed to remotely observe the status and condition of your fridge and maximize food inventory utilization. It provides real-time tracking and generates inclusive recipes to minimize food wastage.

## Objectives
The main objectives of FrostIQ are:
- Remotely observe the fridge's status and condition.
- Maximize and utilize the food inventory efficiently.
- Provide real-time tracking of fridge temperature, humidity, and door status.
- Generate inclusive recipes based on the stored food items.

## Introduction
### Problem Definition
Even with the evolution of home appliances and the integration of new, advanced technology, fridges may malfunction without users being alerted in a timely manner. Additionally, food stored in fridges often gets forgotten and ends up being spoiled and wasted, leading to poor food management.

### Proposed Solution
FrostIQ aims to address these issues by providing real-time data on the fridge's status and enabling better food management. The device is placed inside the fridge and connects to a service's database and a user-friendly graphical interface (GUI). It tracks temperature, humidity, and door status, providing real-time information to the user. Moreover, FrostIQ utilizes computer vision to track the stored food items, allowing users to view, delete, and generate recipes based on the available ingredients.

## Features
- Real-time monitoring of fridge temperature and humidity.
- Alert for open fridge door through a buzzer.
- Barcode scanning for tracking inventory.
- Computer vision-based detection of non-barcoded food items.
- User-friendly interface for managing and generating recipes.

## System Model
The FrostIQ system consists of three main components:
1. Device: Includes a Raspberry Pi 4 as the microcontroller and sensors/actuators for data collection.
2. Server: Processes data retrieved from the device and interacts with the database.
3. User Interface (UI): Displays real-time data and allows user interaction.

## Getting Started
To start using FrostIQ, follow these steps:
1. Purchase a FrostIQ device.
2. Connect the FrostIQ device to your fridge following the provided instructions.
3. Set up the device using the user-friendly interface.
4. Monitor your fridge's status, track food items, and generate recipes through the interface.

## Contributing
We welcome contributions from the community to enhance FrostIQ. If you would like to contribute, please follow these steps:
1. Fork the FrostIQ repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes to your branch.
4. Submit a pull request to the FrostIQ repository.

## Credits
FrostIQ was developed by Anas Dahshan as a project for learning Python and IoT. We would like to thank the following libraries:
- Adafruit CircuitPython
- OpenAI API
- NumPy

## License
FrostIQ is licensed under the MIT License. See LICENSE.txt for more information.
