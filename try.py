import namednodes as _namednodes

try:
    _sv = _namednodes.sv.get_manager(["socket"])
except:
    print("WARNING: Socket discovery failed to find any sockets")

try:
    cpu = _sv.socket.get_all()[0]
except:
    print("WARNING: Your PythonSV doesn't seem to have the cpu component loaded. Some scripts may fail due to this.")


if __name__ == '__main__':
    print("DTS")
    print("1")
    print("1")
    cpu.cdie.taps.cdie_dts1.dtsfusecfg.lvrref_en = 0x0
    print("2")