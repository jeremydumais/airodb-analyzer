# airodb-analyzer

## Description
A python GUI project to analyze the airodb stored data

#### Version 1.0.0
##### *All the instructions below are for Ubuntu 18.04. It is currently the only OS that airodb has been tested on.

## Installation

```bash
sudo apt install -y python3.6 python3-pip git
git clone https://github.com/jeremydumais/airodb-analyzer.git
cd airodb-analyzer
sudo pip3 install -r requirements.txt
```

## How to use it
```bash
python3 airodb_analyzer/airodb_analyzer.py
```

Here's the main window:

<img src="https://github.com/jeremydumais/airodb-analyzer/raw/medias/MainWindow.png" alt="mainWindow">

The first step will be to open a recorded session via the File -> Open a session menu:

<img src="https://github.com/jeremydumais/airodb-analyzer/raw/medias/OpenSession.png" alt="openSession">

You then select the recorded session you want to analyze and click OK. From the main window you will see all the details for each discoverd access point, including the raw logs.

From the view menu, you can show/hide the hidden access points, or show/hide the trusted/untrusted APs.

### Manage your trusted access points

From the menu Manage -> Trusted access points, you can configure a list of the access points that you trust. That way, you can easily, from the View menu, display only the rogue access points or on the other side only the access points that you trust.

<img src="https://github.com/jeremydumais/airodb-analyzer/raw/medias/ManageTrustedAPs.png" alt="manageTrustedAPs">


## Prerequisite

#### Ensure the MongoDB service is running
```bash
sudo systemctl status mongodb
```
<img src="https://raw.githubusercontent.com/jeremydumais/airodb/medias/mongoDBRunning.png" alt="ifconfigExample">

#

