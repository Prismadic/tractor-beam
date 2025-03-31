import magnet.ron.llm as magnetLLM
from magnet.utils.data_classes import AskParameters

class bio:

    def __init__(self, conf:dict = None):
        self.conf = conf
        self.data = []
        self.LastLLM:magnetLLM.LLM = None
        self.LastResult = None;


    async def mimicry(self, server: str = None, field = None, token: str = None, param:AskParameters = None):
        self.LastLLM = magnetLLM.LLM(server, field, token);
        self.LastResult = await self.llm.ask(param);
