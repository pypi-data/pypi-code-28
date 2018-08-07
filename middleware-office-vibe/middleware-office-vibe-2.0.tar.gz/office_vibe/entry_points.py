import errno
import logging
import os



from middleware import model, config

def copy_file():
    from shutil import copyfile
    import office_vibe
    path = os.path.dirname(office_vibe.__file__)
    file = os.path.join(path, "abstract.py")
    file_path = os.path.join(os.getcwd(), 'providers', 'office_vibe_base.py')
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    if not os.path.exists(file_path):
        copyfile(file, file_path)

def init():
    config.initialize()
    copy_file()
    logging.info("Created abstract class for OfficeVibe provider")
    try:
        model.System.add_system(system_id=3, name="OfficeVibe", description="", sync_enabled=1)
    except Exception, msg:
        logging.warning("Command skipped: ", msg)
    logging.info("Applied new system")

