### About

Converting data from MSCONS (EDIFACT) format to CSV.

### Dependencies

* Python 2.7
* docopt

```
pip install -r requirements.txt
```

### Usage
```
# 
python msconsconverter.py '../data/' 'MSCONS_TL_SAMPLE01.txt,MSCONS_TL_SAMPLE02.txt' --verbose

# running sample
python msconsconverter.py --sample
```

### Materials MSCONS (EDIFACT)

* [EDIFACT - English](https://en.wikipedia.org/wiki/EDIFACT)
* [EDIFACT - German](https://de.wikipedia.org/wiki/EDIFACT)
* [EDI@Energy MSCONS](http://www.edi-energy.de/files2/MSCONS_MIG_2_2e_Lesefassung_2015_09_15_2015_09_11.pdf) - format description
* http://www.edi-energy.de/
