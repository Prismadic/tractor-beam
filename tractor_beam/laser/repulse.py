from magnet.ic.field import Charge

class RepulsionBeam:
    def __init__(self, mothershipIP:str = None):
        """
        initializes the object, takes in a copy of the ip of the ship.
        general class to send things out
        instantly connects to server if configured to
        """
        self.defaultMotherShip = mothershipIP
        

    def __del__(self):
        """
        disconnect from NATs before closing
        """


    def ToMotherShip(self, fileLocation:str):
        """
        Sends a copy of the file to a NATs server somewhere via magnet
        """
        print("Repulse"+fileLocation)
