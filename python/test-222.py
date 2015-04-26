import os
import usb.core

usbip_server = "10.0.1.1"


def normalize(value):
    norm_value = value / 4.096
    return int(norm_value)


# The main function
def main():

    print("Testing Phidget InterfaceKit 2-2-2")
    os.environ["USBIP_SERVER"] = usbip_server

    # Find the device you want to work with
    #device = usb.core.find(address=int("0022bdcf5cc0", 16))  # Find using mac address
    device = usb.core.find(idVendor=0x06c2, idProduct=0x0036)  # Find using USB Vendor/Product

    if device is None:
        raise ValueError('Device not found')

    # Get the endpoint value of the device
    endpoint = device[0][(0,0)][0]

    # USB configuration initialization
    device.set_configuration()
    print(usb.util.get_string(device, 256, 1))
    print(usb.util.get_string(device, 256, 2))
    print(usb.util.get_string(device, 256, 3))

    while True:
        data = device.read(1, endpoint.wMaxPacketSize)
        data0 = (data[0x0b] | ((data[0x0c] & 0xf0) << 4))
        data1 = (data[0x0d] | ((data[0x0c] & 0x0f) << 8))

        # Print out the normalized data
        print(normalize(data0), normalize(data1))


if __name__ == "__main__":
    main()