#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import socket
import asyncore
import struct
import sys
import ipaddress
import time


class requester(asyncore.dispatcher):

    def __init__(self, destination_address):
        asyncore.dispatcher.__init__(self)

        self.create_socket()
        self.timeout = 1
        self.destination_address = destination_address
        self.handle_write()

    def build_icmp_packet(self, icmp_identifier=1, icmp_sequence=1):

        def checksumm(packet):
            sum = 0
            countTo = (len(packet) / 2) * 2
            count = 0
            while count < countTo:
                thisVal = packet[count + 1] * 256 + packet[count]
                sum = sum + thisVal
                sum = sum & 0xFFFFFFFF
                count = count + 2

            if countTo < len(packet):
                sum = sum + packet[len(packet) + 1]
                sum = sum & 0xFFFFFFFF

            sum = (sum >> 16) + (sum & 0xFFFF)
            sum = sum + (sum >> 16)
            answer = ~sum
            answer = answer & 0xFFFF
            answer = answer >> 8 | (answer << 8 & 0xFF00)
            return answer

        icmp_header = struct.pack("!BBHHH", 8, 0, 0, icmp_identifier, icmp_sequence)
        # Данные пакеты - вкладываю время
        icmp_data = struct.pack("d", time.time())
        # Считаю контрольную сумму заголовка и вложенных данных
        icmp_checksum = checksumm(icmp_header + icmp_data)
        # Пересобираю заголовок пакета со значением контрольной суммы
        icmp_header = struct.pack("!BBHHH", 8, 0, icmp_checksum, icmp_identifier, icmp_sequence)
        # Переменная packet - сформированный пакет
        icmp_packet = icmp_header + icmp_data

        return icmp_packet


    def writable(self):
        pass


    def readable(self):
        self.readable_time = time.time() - self.time_sent

        if (not self.write and self.timeout < (self.readable_time)):  #
            self.close()
        return not self.write


    def handle_write(self):
        self.connect((self.destination_address, 0))
        self.packet = self.build_icmp_packet(icmp_identifier=1, icmp_sequence=1)
        # Время отправки
        self.time_sent = time.time()

        # Буферизуем данные для отправки:
        sent = self.send(self.packet)
        self.packet = self.packet[sent:]
        self.write = False


    def handle_read(self):
        packet = self.recv(1024)
        self.close()
        src_address, icmp_type, icmp_code, icmp_cheksum, icmp_identifier, icmp_sequence, time_stamp = self.ip_packet_analayser(
            packet)
        print(src_address, icmp_type, icmp_code, icmp_cheksum, icmp_identifier, icmp_sequence, time_stamp)


    def create_socket(self, family=socket.AF_INET, type=socket.SOCK_RAW):
        sock_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock_send.setblocking(0)
        self.set_socket(sock_send)


    def ip_packet_analayser(self, ip_packet):
        ip_address = struct.unpack('!BBBB', ip_packet[12:16])
        src_address = "%d.%d.%d.%d" % (ip_address[0], ip_address[1], ip_address[2], ip_address[3])
        icmp_packet = ip_packet[20:]
        icmp_header = icmp_packet[0:8]
        icmp_type, icmp_code, icmp_cheksum, icmp_identifier, icmp_sequence = struct.unpack("!BBHHH", icmp_header)
        try:
            time_stamp = struct.unpack("d", icmp_packet[8:])[0]
        except:
            time_stamp = 0

        return src_address, icmp_type, icmp_code, icmp_cheksum, icmp_identifier, icmp_sequence, time_stamp

if __name__ == "__main__":

    scan_object = {
        'ip address': '172.30.1.1'
    }

    requester(destination_address=scan_object['ip address'])
    asyncore.loop(timeout=1, use_poll=True)