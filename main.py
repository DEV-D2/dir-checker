import config
import datetime 
import dir_checker
import os
import sys

# run script from main as per best practice    
if __name__ == "__main__":
    cfg = config.load_config()

    # get the contents of the directory
    contents = dir_checker.get_directory_contents(cfg.directoryToMonitor)
    if len(contents) == 0:  # do nothing
        print("There are no files in the specified folder. Exiting. Biyeee!")
        sys.exit()

    now = datetime.datetime.now()
    # there are files so time to notify someone about it
    dirName = os.path.basename(os.path.normpath(cfg.directoryToMonitor))
    emailText = (
        "There are {} files in the directory '{}' that are ready to be"
        " reviewed as of {}.".format(
            len(contents),
            dirName,
            now.strftime("%b %d %Y %H:%M:%S"),
        )
    )
    emailSent = dir_checker.send_email(cfg, emailText)
    if not emailSent:
        print("Unable to send email. See log for errors.")
    else:
        print("Email sent successfully. Goodbye!")   