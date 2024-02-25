from magnet.ic.field import Charge
import asyncio

class RepulsionBeam:
    def __init__(self, mothershipIP:str = None):
        """
        initializes the object, takes in a copy of the ip of the ship.
        general class to send things out
        """
        self.defaultMotherShip = mothershipIP
        self.charge = Charge(mothershipIP)
        

    def __del__(self):
        """
        disconnect from NATs before closing
        """
        asyncio.ensure_future(self.charge.off());

    async def Contact(self, category: str = 'no_category', stream: str = 'documents', create: bool = False):
        """
        turns on the charge
        """
        await self.charge.on(category,stream, create)

    async def ToMotherShip(self, fileLocation:str):
        """
        Sends a copy of the file to a NATs server somewhere via magnet
        Pulse to mother ship
        """
        print("Repulse: "+fileLocation)
        #Get the file
        _file = open(fileLocation, "r").read()
        #send it over
        await self.charge.pulse(_file);

    async def off(self):
        """
        turns off the charge
        """
        await self.charge.off()
