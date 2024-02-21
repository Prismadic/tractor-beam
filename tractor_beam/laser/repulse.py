from magnet.ic.field import Charge

class RepulsionBeam:
    def __init__(self, config:dict = None):
        """
        initalizes the object, takes in a copy of the config.
        general class to send things out
        instantly connects to server if configured to
        """
        self.config = config
        self.defaultMotherShip = self.config["settings"]

    def __del__(self):
        """
        disconnect from NATs before closing
        """


    def ToMotherShip(self, file):
        """
        Sends a copy of the file to a NATs server somewhere via magnet
        """
