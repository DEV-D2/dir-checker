import configparser
import keyring
import os
import sys

configFileName = "config.cfg"
SERVICE_ID = 'a45edde9-dee1-48a5-b097-989b29947736' # just use a GUID

class ConfigNames:
    host = "host"
    port = "port"
    sender = "sender"
    receiver = "receiver"
    username = "username"
    password = "password"
    subjectStem = "subjectstem"
    directoryToMonitor = "directorytomonitor"

class Config:
    host = ""
    port = 0
    sender = ""
    host = ""
    port = ""
    sender = ""
    receiver = ""
    username = ""
    subjectStem = ""
    directoryToMonitor = ""
    debugMode = True


def create_config(config):
    config["DEFAULT"] = {
        ConfigNames.host: "localhost",
        ConfigNames.port: "1025",
        ConfigNames.sender: "dev-sender",
        ConfigNames.receiver: "dev-receiver",
    }
    config["PROD"] = {
        ConfigNames.host: "",
        ConfigNames.port: "",
        ConfigNames.sender: "",
        ConfigNames.receiver: "",
        ConfigNames.username: "",
        ConfigNames.password: "",
        ConfigNames.subjectStem: "",
        ConfigNames.directoryToMonitor: "",
    }
    with open(configFileName, "w") as configfile:
        config.write(configfile)
        
def set_password_and_nuke(parser, username, password):
    if not password:
        print("Password is empty. Carry on then.")
        return
    keyring.set_password(SERVICE_ID, username, password)
    print("New password set on keyring for username: '{}'".format(username))    
    # nuke password from config file
    parser.set("PROD", ConfigNames.password, "")
    with open(configFileName, "w+") as configFile: 
        parser.write(configFile)
    print("Password has been overwritten in config file. Phew.")
    
def get_password(username):
    return keyring.get_password(SERVICE_ID, username)

# Loads the config file.
# If the config file does not exist, it will be generated then the program will exist
# so that you can either re-run the program and use the default config
# or update the config with Prod values.
def load_config():
    parser = configparser.ConfigParser(interpolation=None)
    currentPath = os.getcwd()
    configFilePath = os.path.join(currentPath, configFileName)
    if not os.path.exists(configFilePath):
        # read the config
        print("Config file does not exist. Writing config file to working directory.")
        create_config(parser)
        print(
            "Config file written to disk. Exiting program. Re-run to use in dev mode or"
            " enter your own config."
        )
        sys.exit()

    # config file exists
    parser.read(configFileName)
    cfg = Config()
    
    # populate the config obj 
    if len(parser["PROD"][ConfigNames.host]) < 1:
        print("No PROD configuration supplied. Loading in DEV_MODE! Make sure your local SMTP server is running. :)")
        cfg.host = parser["DEFAULT"][ConfigNames.host]
        cfg.port = parser["DEFAULT"][ConfigNames.port]
        cfg.subjectStem = parser["DEFAULT"][ConfigNames.subjectStem]
        cfg.sender = parser["DEFAULT"][ConfigNames.sender]
        cfg.receiver = parser["DEFAULT"][ConfigNames.receiver]
    else:
        # better set debug mode to false
        cfg.debugMode = False
        
        # load the config
        cfg.host = parser["PROD"][ConfigNames.host]
        cfg.port = parser["PROD"][ConfigNames.port]
        cfg.username = parser["PROD"][ConfigNames.username]
        cfg.sender = parser["PROD"][ConfigNames.sender]
        cfg.receiver = parser["PROD"][ConfigNames.receiver]
        cfg.subjectStem = parser["PROD"][ConfigNames.subjectStem]
        cfg.directoryToMonitor = parser["PROD"][ConfigNames.directoryToMonitor]
        
    # now that we have loaded the config, let's deal with the password situation if it has been supplied
    password = parser["PROD"][ConfigNames.password]
    if password:
        set_password_and_nuke(parser, cfg.username, password)
    
    # fallback to current working directory if one is not provided
    if not cfg.directoryToMonitor:
        # use current dir
        cfg.directoryToMonitor = os.path.join(os.getcwd(), "TestDir")

    return cfg