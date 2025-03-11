# pypylon library for interfacing with Basler cameras
from pypylon import pylon

class Basler_Cls:
    def __init__(self, config=None):
        """
        Description:
            Initialize and configure the Basler camera with a given configuration dictionary.

        Args:
            (1) config [dict]: Dictionary containing camera parameters like exposure time, gain, and balance ratios.
        """
        self.camera = None
        
        self.tl_factory = pylon.TlFactory.GetInstance()
        self.devices = self.tl_factory.EnumerateDevices()
    
        if not self.devices:
            raise Exception('No Basler cameras detected. Check the connection!')
        
        for device_i in self.devices:
            print(f'Model: {device_i.GetModelName()}, IP: {device_i.GetIpAddress()}, Serial: {device_i.GetSerialNumber()}')
            
        self.camera = pylon.InstantCamera(self.tl_factory.CreateFirstDevice())

        try:
            self.camera.Open()
            print(f'Connected to: {self.camera.GetDeviceInfo().GetModelName()} '
                  f'({self.camera.GetDeviceInfo().GetIpAddress()})')
        except Exception as e:
            self.camera = None
            raise Exception(f'Failed to connect: {e}')

        # Default configuration
        self.default_config = {
            'exposure_time': 10000,
            'gain': 10,
            'balance_ratios': {'Red': 1.5, 'Green': 1.0, 'Blue': 1.0},
            'pixel_format': 'BayerRG8'
        }

        # Use user-provided config or fall back to default values
        self.config = config if config else self.default_config

        self.__Configure()

        # Setup converter for Bayer to BGR conversion
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        # Initialize the image as None
        self.image = None

    def __Configure(self):
        """
        Description:
            Apply camera settings from the provided configuration dictionary.
        """

        self.camera.Gain.SetValue(self.config['gain'])
        # Disable Auto White Balance
        self.camera.BalanceWhiteAuto.SetValue('Off')

        # Set manual white balance ratios
        for color, value in self.config['balance_ratios'].items():
            self.camera.BalanceRatioSelector.SetValue(color)
            self.camera.BalanceRatio.SetValue(value)

        # Set Pixel Format
        self.camera.PixelFormat.SetValue(self.config['pixel_format'])

        # Disable Auto Exposure
        self.camera.ExposureAuto.SetValue('Off')

        # Set the exposure time in microseconds
        self.camera.ExposureTime.SetValue(self.config['exposure_time'])
        print(f'Exposure Time set to: {self.config["exposure_time"]} µs')

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        self.camera.MaxNumBuffer.Value = 5

    def Is_Grabbing(self):
        """
        Description:
            Function to check whether the camera is currently in the process of acquiring images.
        """

        return self.camera.IsGrabbing()
    
    def Capture(self):
        """
        Description:
            Capture a single image and store it in the 'image' class parameter.
        """

        # Check if the camera is currently grabbing
        if not self.camera.IsGrabbing():
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if result.GrabSucceeded():
            self.image = self.converter.Convert(result).GetArray()
            print(f'Captured image with shape: {self.image.shape} and dtype: {self.image.dtype}')
            result.Release()

            return self.image
        else:
            print(f'Error capturing image. Code: {result.ErrorCode}, Description: {result.ErrorDescription}')
            result.Release()

            return None

    def __Close(self):
        """
        Description:
            Release the camera resources.
        """

        if self.camera is not None:
            if self.camera.IsGrabbing():
                self.camera.StopGrabbing()
            if self.camera.IsOpen():
                self.camera.Close()
            print('Camera resources released.')

    def __del__(self):
        """
        Description:
            Ensure resources are released when the object is destroyed.
        """

        self.__Close()
