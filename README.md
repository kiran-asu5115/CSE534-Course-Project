# CSE534-Course-Project


This project will set up a routing experiment with a  programmable switch topology dynamically configured using the P4 language. We will modify routing tables on the switches in real-time using direct P4 routing commands, forming the basis for examining the packet flow between two hosts connected via multiple routing paths. 
This topology will be deployed as a slice on the FABRIC testbed infrastructure and integrated with the MFLib API to collect and use device-level and overall slice-level metrics such as the packet-drop rate for a particular route, the bandwidth of the route and TCP/ICMP/UDP in/out packets on that route to determine the optimal routing path between two given hosts. 
The objective is to maximize the topology's overall throughput and link utilization and minimize the latency between the two hosts.

### Execute the following command to deploy the slice on FABRIC:
1. Create a _config_ folder and use your ssh keys generated from FABRIC
2. _pip install --user -r requriments.txt_
3. python3 main.py

The above script will submit your slice and initialize MFLib 
and will start monitoring the slice.

