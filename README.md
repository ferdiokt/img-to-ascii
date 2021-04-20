# img-to-ascii
Converting image or picture to be displayed in your terminal in ASCII character.

## Usage

### Capturing image from webcam and display it in ASCII character.
```
python convert.py
```

### Converting image file and display it in ASCII character.
```
python convert.py [image filename or image path] [optional: brightness intensity algorithm] [optional: print ASCII in green a.k.a The Matrix style]
```

### Additional argument to add after filename:

#### Brightness algorithm (default: luminosity)
```
a | average
m | min_max
l | luminosity
e | enhanced luminosity
```
**Explanation:**
- Average algorithm
Converting RGB value to brightness intensity by averaging the RGB value
(R + G + B) / 3
- Min-max algorithm
Converting RGB value to brightness intensity by averaging the maximum number of the RGB tuple:
(max(R, G, B) + min(R, G, B)) / 2
- Luminosity
Converting RGB value to brightness intensity by taking a weighted average of the R, G and B values to account for human perception:
0.21 R + 0.72 G + 0.07 B
- Luminosity Enhanced
Same as the luminosity algorithm but give more weight to Red and Green value:
0.299 R + 0.587 G + 0.114* B

Source: [RGB to Luminance](https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color)

#### Style (default: white text)
```
m
```
If you want the ASCII char to be printed in green color a.k.a The Matrix style/
