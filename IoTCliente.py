# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import sys

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
import Adafruit_ADS1x15

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=monitorCardiacoRECC.azure-devices.net;DeviceId=raspberryRECC;SharedAccessKey=1p1+lXvLzZUNpQnxCrEyKxoh9qrZhRZD3dblrb+X+0A="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
MSG_TXT = "{\"temperature\": %.2f,\"humidity\": %.2f}"
GAIN = 1
def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
		
		
		
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
	adc = Adafruit_ADS1x15.ADS1115()
        while True:
            # Build the message with simulated telemetry values.
            temperature = adc.read_adc(0, gain=GAIN)
            humidity = adc.read_adc(1, gain=GAIN)
            msg_txt_formatted = MSG_TXT % (temperature, humidity)
            message = IoTHubMessage(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            prop_map = message.properties()
            if temperature > 17896:
              prop_map.add("temperatureAlert", "true")
	      message = IoTHubMessage("Alerta")
            else:
              prop_map.add("temperatureAlert", "false")

            # Send the message.
            print( "Sending message: %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(1)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()