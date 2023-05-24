# NGPrimeClaim

NGPrimeClaim is a python script that convert Neo Geo roms from Code Msytics implementations to romsets for Final Burn Alpha, MAME or FBNeo.

## Usage
1. Download the NGPrimeClaim.py file and the json folder and put all in the same directory.
2. Run with:
    > ./NGPrimeClaim.py game srcdir outdir

## Background and information
The script creates all file that match FBNeo CRC32. The original bash script is from lioneltrs https://github.com/lioneltrs/goNCommand. Original contributors are:

1. lineltrs
2. RedundantCich
3. Lx32

Other useful scripts to extract and convert games are available from:
+ https://gitlab.com/vaiski/romextract
+ https://github.com/ValadAmoleo/sf30ac-extractor/tree/mame
+ https://github.com/farmerbb/RED-Project
+ https://github.com/shawngmc/game-extraction-toolbox


## Contributing

Feel free to fork this code or the original bash one (and solve the Metal Slug 4 or the King of Fighters 2003 problems). Also there is to implement Super Sidekicks II in this version because the original script is a lot different.

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
