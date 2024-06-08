
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
    print(f"spinning ...\t speed : {percent} %")


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
    """ Déplace la tête à la position spécifiée
    :param generator: Objet PulseGenerator.
    """
    # Activer les steppers
    GPIO.output(STEPPERS_ENABLE_PIN, GPIO.HIGH)
    
    prev = 0
    st = time.time()
    k = 0
    k0 = 0

    US_IN_SECONDS = 1e-3

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
        
        pins = []
        m = None
        for i, pin in zip((tx, ty, tz, te), (STEPPER_STEP_PIN_X, STEPPER_STEP_PIN_Y, STEPPER_STEP_PIN_Z, STEPPER_STEP_PIN_E)):
            if i is not None:
                pins.append(pin)
                if m is None or i < m:
                    m = i
        
        k = int(round(m * US_IN_SECONDS))
        if k - prev > 0:
            pass
            #time.sleep((k - prev) * US_IN_SECONDS)
        
        for pin in pins:
            GPIO.output(pin, GPIO.HIGH)
        
        time.sleep(STEPPER_PULSE_LENGTH_US * US_IN_SECONDS / len(pins))
        
        for pin in pins:
            GPIO.output(pin, GPIO.LOW)
        
        prev = k + STEPPER_PULSE_LENGTH_US
    
    pt = time.time()
    logging.info("préparé en " + str(round(pt - st, 2)) + "s, estimé en "
                 + str(round(generator.total_time_s(), 2)) + "s")
    
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