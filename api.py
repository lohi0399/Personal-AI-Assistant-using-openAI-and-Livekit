import enum
from typing import Annotated
from livekit.agents import llm
import logging



logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)

class Zone(enum.Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    OFFICE = "office"

class AssistantFunc (llm.FunctionContext): # We can extent the functionality of our current llm by let it caall our own function which can be added to this class
    def __init__(self) -> None:
        super().__init__() # To mae=ke sure the parent class is getting setup correctly
        self._temperature = {
            Zone.LIVING_ROOM: 22,
            Zone.BEDROOM: 20,
            Zone.BATHROOM: 23,
            Zone.OFFICE: 21,
        }
    
    @llm.ai_callable(description="get the temperature in a specfic room") # The custoom function we define can be wraapped inside this decorter which add our functionality to this class. We need to provide a good enough description so that the AI is able to distinguish which functions actually use what
    def get_temperature(self, zone: Annotated[Zone,llm.TypeInfo(description="The specific zone")]): # Need to annotate them properly so that python and the LLM know what data to take in correctly
        logger.info("get temp - zone %s", zone)
        temp = self._temperature[Zone(zone)]

        return f"The temperature in the {zone} is {temp}C"