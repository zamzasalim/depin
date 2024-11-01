<p style="font-size:14px" align="right">
<a href="https://t.me/airdropasc" target="_blank">Join our telegram <img src="https://user-images.githubusercontent.com/50621007/183283867-56b4d69f-bc6e-4939-b00a-72aa019d1aea.png" width="30"/></a>
</p>

<p align="center">
  <img height="300" height="auto" src="https://user-images.githubusercontent.com/109174478/209359981-dc19b4bf-854d-4a2a-b803-2547a7fa43f2.jpg">
</p>

# FARMING GRASS SEASON 2 WITH VPS
## Register Grass Account
- Signup [Here](https://s.id/getgrass)
- Register with email & verify
- Login to Dashboard
## How to Get UID Grass
- Login Dashboard Grass
- klik kanan inspect
- Pilih Menu Aplication
- Local Storage
- userid sebelah kanan salin & paste on notepad
## Install Python & Screen (Kalo belum punya)
```
sudo apt update
sudo apt install -y wget build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```
```
wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz
tar -xf Python-3.13.0.tgz
cd Python-3.13.0
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
```
```
apt-get install screen
```
```
sudo ufw allow ssh
sudo ufw enable
sudo ufw status
```
## Download Repositori
```
git clone https://github.com/zamzasalim/depin.git
```
## Run Grass on VPS with Screen
```
cd depin/grass
```
```
python3 -m pip install -r requirements.txt
```
```
screen -S grass
```
```
python3 main.py
```
