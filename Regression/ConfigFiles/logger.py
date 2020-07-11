import inspect
import logging
import os.path
import os
import uuid


def genericLogger(logLevel=logging.DEBUG):
    # Gets the name of the class / method from where this method is called
    loggerName = inspect.stack()[1][3]
    logger = logging.getLogger(loggerName)
    # By default, log all messages
    logger.setLevel(logging.DEBUG)

    log_dir = os.path.dirname(os.path.dirname(__file__))
    log_file = os.path.join(log_dir, "logs", "automation.log")
    fileHandler = logging.FileHandler(log_file, mode='a')

    fileHandler.setLevel(logLevel)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    return logger


def save_screenshot_and_raise(exception, driver, payload):
    run_version = os.environ.get('BUILD_ID', 'manual')
    filename = "./failed/{}/test_valid_email_{}_{}.png".format(
        run_version,
        payload.tc, uuid.uuid4()
    )
    driver.save_screenshot(filename)
    host = os.environ.get('JOB_URL', 'not jenkins')
    # JOB_URL=http://ci.nrgpl.us:8080/job/regression_ecc_qa/
    display_name = '{}ws/Regression/{}'.format(
        host,
        filename,
    )
    # will be like
    # http://ci.nrgpl.us:8080/job/regression_ecc_qa/ws/Regression/failed/
    print("Saving screenshot of failed test -- ", payload.tc)
    print("filename:", filename)
    print("link:", display_name)
    print(str(exception))
    raise exception
