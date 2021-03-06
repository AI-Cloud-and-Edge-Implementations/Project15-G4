import subprocess


def handle_copy(function):
    def wrapper(*args, **kwargs):
        source_path, destination_path, logger = function(*args, **kwargs)
        logger.info(
            "Sending file from {} to {}".format(
                source_path, destination_path
            )
        )
        command_to_run = [
            'azcopy', '--source', source_path, '--destination', destination_path, '--recursive'
        ]
        logger.info('We ran this command: {0}'.format(' '.join(command_to_run)))
        p1 = subprocess.run(command_to_run)
        logger.info("Completed Copying File: {}".format(source_path))
        return p1

    return wrapper
