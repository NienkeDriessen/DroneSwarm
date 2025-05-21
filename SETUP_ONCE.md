# 🛠️ One-Time Setup (Laptop)

Follow these steps once to prepare your laptop for the drone demo.

---

## 1. Clone the Repository

Open a terminal (e.g. CMD, PowerShell, or Terminal on Mac) and run:

```bash
git clone https://github.com/NienkeDriessen/DroneSwarm.git
cd DroneSwarm
```

Sudo apt install npm
npm install

## 2. Install Python Requirements

Ensure Python 3.10+ is installed. Then, create a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
```

Install the required packages:

```bash
pip install -r requirements.txt
```

You're done! You only need to do this setup once per machine.

# If new laptop

The IP address will be different,
Connect the laptop to the router

### The app uses a static IP address so we need to set this up again

you have to go into the router settings,

(on browser navigate to (enter in address bar) 192.168.1.1)
A login screen will be shown, the password is 'admin'
Then click on the configuration tab
Click on connectivity menu, under local network,
Click on DHCP reservation button

While your device is connected to the router, you can see the device, select it and add client.

THen in 'Clients already reserved'
You can assign an IP address, change it to

192.168.1.145 (TODO CHECK)
And remove the old one that was assigned
