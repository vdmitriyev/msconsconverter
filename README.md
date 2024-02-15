### About

Converting data from MSCONS (EDIFACT) format to CSV.

### Dependencies Overview

* Python > 3.6
* docopt

### Install Dependencies

```
pip install -r requirements.txt
```
* Or use ```scripts/cmdInitiateEnv.bat```

### Usage

```
cd msconsconverter
# providing data folder and data files as input
python msconsconverter.py '../data/' 'MSCONS_TL_SAMPLE01.txt,MSCONS_TL_SAMPLE02.txt' --verbose

# running sample
python msconsconverter.py --sample
```

#### Usage on Ubuntu

* Preparation and start (for further details see ```msconsconverter/run.sh```)
```
cd msconsconverter
apt-get install dos2unix -y
dos2unix run.sh
chmod +x run.sh
./run.sh
```

### Materials on MSCONS (EDIFACT)

* [EDIFACT - English](https://en.wikipedia.org/wiki/EDIFACT)
* [EDIFACT - German](https://de.wikipedia.org/wiki/EDIFACT)
* [EDI@Energy MSCONS](https://www.edi-energy.de/index.php?id=38) -> format description, see "Bewegungsdaten" section
* http://www.edi-energy.de/
* [Various Usages](https://www.bundesnetzagentur.de/DE/Service-Funktionen/Beschlusskammern/Beschlusskammer6/BK6_31_GPKE_und_GeLiGas/BK6_GPKE_undGeLi_Gas_node.html) -> see "GPKE" section
