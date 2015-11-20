

import random
import socket
from threading import Thread
import time

class gossiping_process:
   
    infected_nodes = []
    
    def __init__(currentnode, port, connected_nodes):
        currentnode.node = socket.socket(type=socket.SOCK_DGRAM)
        currentnode.hostname = socket.gethostname()
        currentnode.port = port       
        currentnode.node.bind((currentnode.hostname, currentnode.port))       
        currentnode.susceptible_nodes = connected_nodes
        print("Node B started on port {0}".format(currentnode.port))
        print("Susceptible nodes =>", currentnode.susceptible_nodes)
        Thread(target=currentnode.input_message).start()
        Thread(target=currentnode.receive_message).start()


    def input_message(currentnode):
        while True:
            message_to_send = input("Enter a message to send:\n")
            currentnode.transmit_message(message_to_send.encode('ascii'))

    def receive_message(currentnode):
        while True:
            message_to_forward, address = currentnode.node.recvfrom(1024)
            currentnode.susceptible_nodes.remove(address[1])
            gossiping_process.infected_nodes.append(address[1])
            time.sleep(3)
            print("Receiving message......\n")
            print("\nMessage received is: {0}.\nReceived at [{1}] from [{2}]\n"
                  .format(message_to_forward.decode('ascii'), time.ctime(time.time()), address[1]))
            currentnode.transmit_message(message_to_forward)

    def transmit_message(currentnode, message):
        while currentnode.susceptible_nodes:
            selected_port = random.choice(currentnode.susceptible_nodes)
            print("\n")
            print("="*100)
            print("Susceptible nodes =>", currentnode.susceptible_nodes)
            print("Infected nodes =>", gossiping_process.infected_nodes)
            print("Port selected is [{0}]".format(selected_port))
            currentnode.node.sendto(message, (currentnode.hostname, selected_port))
            # currentnode.susceptible_nodes.remove(address[1])
            # gossiping_process.infected_nodes.append(address[1])
            print("{0} is being send to [{1}].".format(message.decode('ascii'), selected_port))
            print("="*100)
            time.sleep(3)

            print("\n")
    
class initializevalues:
     gossiping_process
     port = 1001
     connected_nodes = [1000, 1003, 1004]
     node = gossiping_process(port, connected_nodes)
