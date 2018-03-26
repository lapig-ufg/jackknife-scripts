## Synopsis

An example on how to preprocess and normalize imagery time-series data for being used with Deep Learning

## Usage Example

One must first run the script that takes a list of unique-band VRT images with the same sufix (e.g. \*\_01.vrt) and stack them altogether in a VRT file which has one band for each of the files that share the same sufix:

>$ ./time_cube.sh

Next, the normalization itself, which spans data values into a range of 1 and center values around 0.

>$ python normalize_data.py

If everything went well, the script outputs one *img* file per spectrum band, that consists of a stack of images with length equals to the number of original images.

## License

This software is available under GNU GPLv3 license.
