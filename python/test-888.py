import os
import usb.core

usbip_server = "10.0.1.1"


def normalize(value):
    norm_value = value / 4.096
    return int(norm_value)


# The main function
def main():

    print("Testing Phidget InterfaceKit 8-8-8 P/N 1018")
    os.environ["USBIP_SERVER"] = usbip_server

    # Find the device you want to work with
    device = usb.core.find(address=int("0022bdcf5bc0", 16))  # Find using mac address
    #device = usb.core.find(idVendor=0x06c2, idProduct=0x007d)  # Find using USB Vendor/Product

    if device is None:
        raise ValueError('Device not found')

    # begin generic usb initialization
    device.set_configuration()
    print(usb.util.get_string(device, 256, 1))
    print(usb.util.get_string(device, 256, 2))
    print(usb.util.get_string(device, 256, 3))

    while True:
        data = device.read(1, 64)
        if (data[0x00] & 0x0f) == 0x0f:
            data0 = data[0x0b] | ((data[0x0c] & 0xf0) << 4)
            data1 = data[0x0d] | ((data[0x0c] & 0x0f) << 8)
            data2 = data[0x0e] | ((data[0x0f] & 0xf0) << 4)
            data3 = data[0x10] | ((data[0x0f] & 0x0f) << 8)
            data4 = data[0x11] | ((data[0x12] & 0xf0) << 4)
            data5 = data[0x13] | ((data[0x12] & 0x0f) << 8)
            data6 = data[0x14] | ((data[0x15] & 0xf0) << 4)
            data7 = data[0x16] | ((data[0x15] & 0x0f) << 8)

            # Print out the raw data
            print(data0, data1, data2, data3, data4, data5, data6, data7)

if __name__ == "__main__":
    main()