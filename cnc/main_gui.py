from cnc.gcode import GCode, GCodeException
from cnc.gmachine import GMachine, GMachineException

machine = GMachine()

def do_line(line):
    try:
        g = GCode.parse_line(line)
        res = machine.do_command(g)
    except (GCodeException, GMachineException) as e:
        print('ERROR ' + str(e))
        return False
    if res is not None:
        print('OK ' + res)
    else:
        print('OK')
    return True