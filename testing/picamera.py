from picamera import PiCamera
from time import sleep
from pyzbar import pyzbar

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        # 1
        # utf-8 is byte string 
        barcode_info = barcode.data.decode('utf-8')

        # 2
        # Draw a rectangle around the barcode
        draw.rectangle((x, y, x+w, y+h), outline=(0, 255, 0))
        
        # 3
        # Display the barcode information on the screen
        draw.text((x, y-20), barcode_info, fill=(255, 255, 255))
        
        # 4
        # Save the barcode information to a text file
        with open("barcode_result.txt", mode='w') as file:
            filewrite("Recognized Barcode:" + barcode_info)
            
    return frame

def main():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 24

    with picamera.array.PiRGBArray(camera) as stream:
        while True:
            camera.capture(stream, 'rgb')
            frame = stream.array
            frame = read_barcodes(frame)
            # Show the frame on screen
            img = Image.fromarray(frame, 'RGB')
            img.show()

            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()

            # Check for the Esc key to exit
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

    camera.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

