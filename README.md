# CustomerCounter

CustomerCounter is a Python program that attempts to count the current number of people inside a building using mainly the probe request frame as well as other frames such as RTS (Request To Send).

Some aditionnal information will be displayed on a TUI (Terminal User Interface) as shown below.

![tui](https://github.com/0xHexPloit/CustomerCounter/blob/master/assets/tui.png?raw=true)

**Disclaimer: This project was developed as part of a school project. It is intended for educational use only.** 

## Installation

To use our program, you must first create a Docker image. To do this, please follow the steps below.


First , clone our project inside your Kali Linux machine

```
git clone https://github.com/0xHexPloit/CustomerCounter.git
```

Then change the current working directory

```
cd ./CustomerCounter
```

Finally, build the Docker image (we expect that Docker is installed on your machine).

```
docker build -t customercounter .
```

## Usage

Before running our program, make sure that your Wifi dongle is in `monitor` mode. To so do, you can execute the following command:

```
sudo iwconfig <interface> set monitor
```

Then to launch our TUI, execute the command:

```
docker run --rm -it --privileged --network="host" customercounter <interface>
```
