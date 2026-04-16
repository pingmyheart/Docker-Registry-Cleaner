from configuration.logging_configuration import logger as log
from runner import jobs

if __name__ == '__main__':
    for job in jobs:
        log.info(f"Starting job: {job.__name__}")
        job.run()
