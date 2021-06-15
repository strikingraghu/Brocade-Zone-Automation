# Brocade Zone Automation
Repository provides a light weight python code to automate Brocade zoning for SAN storage volume provisioning tasks

About This Code
This code describes the REST API (a programmable Web service interface) for Brocade Fabric OS. The REST API can manage Brocade SAN switches across a fabric.

REST Terminology
The following terms are used in this manual to describe REST and REST functionality contained in the Brocade FOS REST API.
base URI A base URI is specific to the Fabric OS server. All URIs accessing the same server use the same base URI.
For example, in the request “POST http://10.10.10.10/rest/login”, “http://10.10.10.10/rest/” is the base URI.
device Any host or target device with a distinct WWN. Devices may be physical or virtual.
D_Port A port configured as a diagnostic port on a switch or connected fabric switch, used to run diagnostic tests between
ports to test the link.
E_Port An interswitch link (ISL) port. A switch port that connects switches together to form a fabric.
F_Port A fabric port. A switch port that connects a host, host bus adapter (HBA), or storage device to a SAN.
fabric A fabric consists of interconnected nodes that look like a single logical unit when viewed collectively. This refers to a
consolidated high-performance network system consisting of coupled storage devices, networking devices, and
parallel processing high bandwidth interconnects such as 8Gb/s, 10Gb/s, 16Gb/s, or 32Gb/s Fibre Channel ports.
FCID A Fibre Channel ID (FCID) is a 24-bit (3 byte) field used to route frames through a Fibre Channel (FC) network. The
FOS REST API shows this as a decimal value, such as “14776283”.
REST Terminology
Brocade Fabric OS REST API Reference Manual, 8.2.x
8 FOS-82X-REST-API-RM101FCIP Fiber Channel over IP. This functionality allows connectivity between two remote fabrics that are separated by an IP
network. FCIP is |iff~r~n± from “IP over FC”. Refer to RFC 3821.
HTTP HyperText Transfer Protocol. An application protocol for distributed, collaborative, and hypermedia information
systems. Refer to RFC 7230.
Internet Protocol
(IP)
The principal communications protocol in the Internet Protocol suite. It conveys packets from a source host to a
destination host based on the IP addresses contained in the packet headers. Refer to RFC 791.
IPsec Internet Protocol security. A network protocol suite that authenticates and encrypts the packets of data sent over a
network, protecting data flows between a pair of hosts (host-to-host), a pair of security gateways (network-tonetwork), or between a security gateway and a host (network-to-host). Refer to RFC 4301, RFC 4303, and
RFC 4309.
JSON JavaScript Object Notation. JSON is an open-standard file format that uses human-readable text to transmit data
objects consisting of attribute–value pairs and array data types (or any other serializable value). It is a very common
data format used for asynchronous browser–server communication, including as a replacement for XML in some
AJAX-style systems. Refer to RFC 8259 and ECMA-404.
N_Port A node port. A N_Port presents a host or storage device to the fabric.
NETCONF NETwork CONFiguration protocol. A network management protocol developed and standardized by the IETF.
Refer to RFC 6241.
NPIV N_Port ID Virtualization. This is a Fibre Channel facility allowing multiple F_Port IDs to share a single physical
N_Port. Multiple F_Ports can be mapped to a single N_Port. This allows multiple Fibre Channel initiators to occupy
a single physical port, easing hardware requirements in storage area network design, especially for virtual SANs.
REST REpresentational State Transfer is a way of providing interoperability between computer systems in a network.
RESTCONF REST CONFiguration protocol. A RESTful protocol used to access data |~fin~| using the YANG language. Refer to
RFC 8040.
request URI A request URI is the URI used to perform a REST HTTP request such as GET, POST, PUT, DELETE, HEAD or
OPTIONS.
SNMP Simple Network Management Protocol (SNMP) is a set of protocols for managing complex networks. SNMP
protocols are application layer protocols. Using SNMP, devices within a network send messages, called protocol data
units (PDUs), to |iff~r~n± parts of a network. Refer to RFC 1157, RFC 3411, RFC 3412, RFC 3414 and RFC
3415.
TCP Transmission Control Protocol. One of the main protocols of the Internet Protocol (IP) suite. TCP provides reliable,
ordered, and error-checked delivery of a stream of data in octets between applications running on hosts
communicating by an IP network. Refer to RFC 1122 and RFC 7323.
VE_Port Virtual E_Port. Software mechanism for creating a logical E_Port connection to allow the Fibre Channel fabric
protocols to communicate over this virtual interface. Typically used for FCIP products.
YANG Yet Another Next Generation. A data modeling language for the definition of data sent over the NETCONF network
configuration protocol. Refer to RFC 7950.
XML eXtensible Markup Language. A markup language that defines a set of rules for encoding documents in a format
that is both human-readable and machine-readable through use of tags that can be created and |~fin~| by users.
Refer to the W3C XML standard.

dictionary at:
http://www.snia.org/education/dictionary
