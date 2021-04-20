from PIL import Image
from colorama import Fore, Style
import numpy as np
import sys, cv2, queue, threading


# define ASCII char
ASCII_CHAR = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
# value to normalize the image
MAX_PIXEL_VAL = 255

# taking args in cmd
user_arg = sys.argv[1:]


# extra class to capturing last frame only
# special thanks to Ulrich Stern: 
# https://stackoverflow.com/questions/43665208/how-to-get-the-latest-frame-from-capture-device-camera-in-opencv
class VideoCapture:

    def __init__(self, name):
        self.capture = cv2.VideoCapture(name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # Read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # Discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


def get_pixel(img):
    # convert img object to 3d array
    scale_percentage = round((320/img.width), 2)
    scaled_size = (int(img.width*scale_percentage), int(img.height*scale_percentage))
    new_img = img.resize(scaled_size)
    pixel_matrix = np.asarray(new_img)
    return pixel_matrix


def get_intensity(pixel, algorithm = 'luminosity'):
    # converting RGB color to brightness intensity
    intensity_matrix = []
    for x in pixel:
        intensity_row = []
        for y in x:
            if algorithm == 'average' or algorithm == 'a':
                intensity = (y[0] + y[1] + y[2])/3
            elif algorithm == 'max_min' or algorithm == 'm':
                intensity = (max(y) + min(y))/2
            elif algorithm == 'luminosity' or algorithm == 'l':
                intensity = 0.21*y[0] + 0.72*y[1] + 0.07*y[2]
            elif algorithm == 'luminosity_enh' or algorithm == 'e':
                intensity = 0.299*y[0] + 0.587*y[1] + 0.114*y[2]
            else:
                raise Exception(f"Unrecognized algorithm name: {algorithm}")
            
            intensity_row.append(intensity)
        
        intensity_matrix.append(intensity_row)
    
    return intensity_matrix        


def normalize_intensity(matrix):
    # scaling the intensity to match maximum and minimum number of pixel value (0-255)
    normalized_matrix = []
    min_pixel = min(map(min, matrix))
    max_pixel = max(map(max, matrix))
    for x in matrix:
        normalized_row = []
        for y in x:
            normalized = MAX_PIXEL_VAL * (y - min_pixel) / float(max_pixel - min_pixel)
            normalized_row.append(normalized)
        
        normalized_matrix.append(normalized_row)
    
    return normalized_matrix

def convert_ascii(matrix, ascii_char):
    # converting the intensity matrix to ascii matrix
    n_matrix = normalize_intensity(matrix)
    ascii_matrix = []
    for x in n_matrix:
        ascii_row = []
        for y in x:
            scaled = ascii_char[int(y*len(ascii_char)/MAX_PIXEL_VAL) - 1]
            ascii_row.append(scaled)
        
        ascii_matrix.append(ascii_row)
    
    return ascii_matrix


def print_ascii_img(matrix, text_color = 'd'):
    # print the ascii img in the terminal
    for row in matrix:
        line = [y + y + y for y in row]
        if text_color == 'm':
            print(Fore.GREEN + "".join(line))
        else:
            print("".join(line))    
    
    print(Style.RESET_ALL)


def convert_capture():
    # taking image from the webcam snapshot
    frame_capture = VideoCapture(0)
    while True:        
        frame = frame_capture.read()
        cv2.imshow("frame", frame)
        
        if chr(cv2.waitKey(1)&255) == 'q':
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            last_frame = Image.fromarray(cv2.cvtColor(frame_gray, cv2.COLOR_BGR2RGB), 'RGB')
            break
    
    img_array = get_pixel(last_frame)
    print("What kind of algorithm do you want to use?")
    print("Type a for average, m for min_max, l for luminosity, e for enhanced luminosity")
    algo_name = input("Answer: ").lower()
    
    if algo_name == 'a':
        img_intensity = get_intensity(img_array)
    elif algo_name == 'm':
        img_intensity = get_intensity(img_array, 'max_min')
    elif algo_name == 'l':
        img_intensity = get_intensity(img_array, "luminosity")
    elif algo_name == 'e':
        img_intensity = get_intensity(img_array, "luminosity_enh")
    else:
        print("You didn't answer correctly, default is chosen")
        img_intensity = get_intensity(img_array)   
        
    img_ascii = convert_ascii(img_intensity, ASCII_CHAR)
    ask_style = input("Do you want it to be printed in The Matrix Style [Y/N]? ").upper()
    
    if ask_style == 'Y':
        print_ascii_img(img_ascii, 'tm')
    elif ask_style == 'N':
        print_ascii_img(img_ascii)
    else:
        print("You didn't get the question, default is chosen")
        print_ascii_img(img_ascii)
    
    print("Now zoom out your terminal to see the image, enjoy!")

def convert_img(filepath, algorithm = 'luminosity', style = 'd'):
    # main program, converting image and print it in the terminal
    img = Image.open(filepath)
    img_array = get_pixel(img)
    img_intensity = get_intensity(img_array, algorithm)
    img_ascii = convert_ascii(img_intensity, ASCII_CHAR)
    print_ascii_img(img_ascii, style)
    print("Now zoom out your terminal to see the image, enjoy!")


if len(user_arg) > 0:
    filepath = user_arg[0]
    try:
        convert_img(filepath)
    except:
        print("File not found or something bad happened")

elif len(user_arg) > 1:
    filepath = user_arg[0]
    algorithm = user_arg[1]
    try:
        convert_img(filepath, algorithm)
    except:
        print("File not found or something bad happened")

elif len(user_arg) > 2:
    filepath = user_arg[0]
    algorithm = user_arg[1]
    style = user_arg[2]
    try:
        convert_img(filepath, algorithm, style)
    except:
        print("File not found or something bad happened")

elif len(user_arg) == 0 and __name__ == ('__main__'):
    convert_capture()
