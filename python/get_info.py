import os
import sys
import usb
from socket import error as socket_error
#import getopt
#import errno

usbip_server = '10.0.1.1'

# Function for printing out the device vlaues
def print_value(title_primary, value_primary, title_secondary='', value_secondary=''):
    output = title_primary + ': ' + value_primary
    if title_secondary:
        output += ', ' + title_secondary + ': ' + value_secondary
    sys.stdout.write(output + '\n')

# The main function
def main():
    os.environ['USBIP_SERVER'] = usbip_server

    try:
        devices = usb.core.find(find_all=True)
    except socket_error as serr:
        print('ERROR: Unable to connect to ' + usbip_server)
        return serr.errno

    #print(devices)

    for device in devices:
        #if device is None:
        #    print "Device Not Found"
        #    continue

        #print(device.iManufacturer)
        device.set_configuration()

        # Get the Device Descriptors
        sys.stdout.write('Device\n')
        print_value('\tManufacturer', usb.util.get_string(device, 256, device.iManufacturer))
        print_value('\tProduct', usb.util.get_string(device, 256, device.iProduct))
        print_value('\tSerial Number', usb.util.get_string(device, 64, device.iSerialNumber))
        print_value('\tVendorID', hex(device.idVendor), 'ProductID', hex(device.idProduct))

        # Get the Configuration Descriptors
        print_value('\tConfigurations', str(device.bNumConfigurations))
        for configurationDescriptor in device:
            print_value('\t\tConfiguration Value', str(configurationDescriptor.bConfigurationValue))
            #print_value('\t\tConfiguration', usb.util.get_string(configurationDescriptor, 256, configurationDescriptor.iConfiguration))
            print_value('\t\tMax Power Consumption', str(configurationDescriptor.bMaxPower))
            #print_value('\t\tConfiguration', configurationDescriptor.iConfiguration)

            print_value('\t\tInterfaces', str(configurationDescriptor.bNumInterfaces))

            # Get the Interface Descriptors
            for interfaceDescriptor in configurationDescriptor:
                print_value('\t\t\tInterface Number', str(interfaceDescriptor.bInterfaceNumber), 'Alternate Setting', str(interfaceDescriptor.bAlternateSetting))

                #for endpointDescriptor in interfaceDescriptor:
                #    print_value('\t\t\tEndpoints', str(endpointDescriptor.bmAttributes))
                #    sys.stdout.write('\t\t' + str(endpointDescriptor.bEndpointAddress) + '\n')


if __name__ == "__main__":
    main()