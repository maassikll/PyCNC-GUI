
import RPi.GPIO as GPIO
import time
from cnc.pulses import *
from cnc.config import *
from time import sleep

# Set up the GPIO pin
GPIO.setmode(GPIO.BCM)

def init():
    """ Initialize GPIO pins and machine itself.
    """
    GPIO.cleanup()

    GPIO.setup(STEPPER_STEP_PIN_X, GPIO.OUT)
    GPIO.setup(STEPPER_STEP_PIN_Y, GPIO.OUT)
    GPIO.setup(STEPPER_STEP_PIN_Z, GPIO.OUT)
    GPIO.setup(STEPPER_STEP_PIN_E, GPIO.OUT)
    GPIO.setup(STEPPER_DIR_PIN_X, GPIO.OUT)
    GPIO.setup(STEPPER_DIR_PIN_Y, GPIO.OUT)
    GPIO.setup(STEPPER_DIR_PIN_Z, GPIO.OUT)
    GPIO.setup(STEPPER_DIR_PIN_E, GPIO.OUT)
    GPIO.setup(SPINDLE_PWM_PIN, GPIO.OUT)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    GPIO.setup(BED_HEATER_PIN, GPIO.OUT)
    GPIO.setup(STEPPERS_ENABLE_PIN, GPIO.OUT)
    GPIO.setup(EXTRUDER_HEATER_PIN, GPIO.OUT)
    GPIO.setup(ENDSTOP_PIN_X, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ENDSTOP_PIN_Y, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ENDSTOP_PIN_Z, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.output(SPINDLE_PWM_PIN, GPIO.LOW)
    GPIO.output(FAN_PIN, GPIO.LOW)
    GPIO.output(EXTRUDER_HEATER_PIN, GPIO.LOW)
    GPIO.output(BED_HEATER_PIN, GPIO.LOW)
    GPIO.output(STEPPERS_ENABLE_PIN, GPIO.LOW)

    


def spindle_control(percent):
    """ Spindle control implementation 0..100.
    :param percent: Spindle speed in percent.
    """
    logging.info("spindle control: {}%".format(percent))


def fan_control(on_off):
    """Cooling fan control.
    :param on_off: boolean value if fan is enabled.
    """
    if on_off:
        logging.info("Fan is on")
    else:
        logging.info("Fan is off")


# noinspection PyUnusedLocal
def extruder_heater_control(percent):
    """ Extruder heater control.
    :param percent: heater power in percent 0..100. 0 turns heater off.
    """
    pass


# noinspection PyUnusedLocal
def bed_heater_control(percent):
    """ Hot bed heater control.
    :param percent: heater power in percent 0..100. 0 turns heater off.
    """
    pass


def get_extruder_temperature():
    """ Measure extruder temperature.
    :return: temperature in Celsius.
    """
    return EXTRUDER_MAX_TEMPERATURE * 0.999


def get_bed_temperature():
    """ Measure bed temperature.
    :return: temperature in Celsius.
    """
    return BED_MAX_TEMPERATURE * 0.999


def disable_steppers():
    """ Disable all steppers until any movement occurs.
    """
    logging.info("hal disable steppers")


def calibrate(x, y, z):
    """ Move head to home position till end stop switch will be triggered.
    Do not return till all procedures are completed.
    :param x: boolean, True to calibrate X axis.
    :param y: boolean, True to calibrate Y axis.
    :param z: boolean, True to calibrate Z axis.
    :return: boolean, True if all specified end stops were triggered.
    """
    logging.info("hal calibrate, x={}, y={}, z={}".format(x, y, z))
    return True


# noinspection PyUnusedLocal
def move(generator):
    # Activer les steppers
    GPIO.output(STEPPERS_ENABLE_PIN, GPIO.HIGH)
    
    prev = 0
    st = time.time()
    k = 0
    k0 = 0



    for direction, tx, ty, tz, te in generator:

        if direction:  # Configurer les directions
            if tx is not None:
                GPIO.output(STEPPER_DIR_PIN_X, GPIO.HIGH if tx > 0 else GPIO.LOW)
            if ty is not None:
                GPIO.output(STEPPER_DIR_PIN_Y, GPIO.HIGH if ty > 0 else GPIO.LOW)
            if tz is not None:
                GPIO.output(STEPPER_DIR_PIN_Z, GPIO.HIGH if tz > 0 else GPIO.LOW)
            if te is not None:
                GPIO.output(STEPPER_DIR_PIN_E, GPIO.HIGH if te > 0 else GPIO.LOW)
            continue
        
    delay = 0.003
    for x in range(200):
        GPIO.output(STEPPER_STEP_PIN_X, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEPPER_STEP_PIN_X, GPIO.LOW)
        sleep(delay)
    
    # Désactiver les steppers
    GPIO.output(STEPPERS_ENABLE_PIN, GPIO.LOW)


def join():
    """ Wait till motors work.
    """
    logging.info("hal join()")


def deinit():
    """ De-initialise.
    """
    logging.info("hal deinit()")


def watchdog_feed():
    """ Feed hardware watchdog.
    """
    pass