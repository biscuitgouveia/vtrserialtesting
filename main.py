import vdcp


def main():

    test_play = vdcp.VDCP()

    test_play.init_serial()

    test_play.open_port()

    test_play.select_port()

    test_play.get_port_status()

    test_play.active_id_request()

    # test_play.stop_port()

    test_play.get_port_status()

    test_play.serial_port.close()


if __name__ == '__main__':
    main()
