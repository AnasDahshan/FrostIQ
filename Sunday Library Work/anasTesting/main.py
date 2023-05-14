from camera_controller import CameraController

def main():
    camera_controller = CameraController(0)
    camera_controller.process_frames()

if __name__ == '__main__':
    main()
