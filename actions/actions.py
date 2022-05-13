from datetime import time
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, Form, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
# from database import DataUpdate1,DataUpdate2
import requests
import random

from rasa_sdk.forms import FormAction, REQUESTED_SLOT

from actions.weatherAPI import get_weather
from actions.zomato import Zomato

zomato = Zomato()


class ActionOrderId(Action):
    def name(self) -> Text:
        return "action_order_id"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        order_id = tracker.sender_id
        dispatcher.utter_message("Your Order Number is {}".format(order_id))
        return []


# class ActionFormInfoPizza(Action):
#     def name(self) -> Text:
#         return "form_info_pizza"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[EventType]:
#         required_slots = ["food","size","topping","crust_type","quantity","name"]

#         for slot_name in required_slots:
#             if tracker.slots.get(slot_name) is None:
#                 # The slot is not filled yet. Request the user to fill this slot next.
#                 return [SlotSet("requested_slot", slot_name)]

#         # All slots are filled.
#         return [SlotSet("requested_slot", None)]

# class ActionSubmitPizza(Action):
#     def name(self) -> Text:
#         return "action_submit_pizza"

#     def run(
#         self,
#         dispatcher,
#         tracker: Tracker,
#         domain: "DomainDict",
#     ) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(template="utter_food", quantity=tracker.get_slot('quantity'),size=tracker.get_slot('size'),food=tracker.get_slot('food'),topping=tracker.get_slot('topping'),
#                                  crust_type=tracker.get_slot('crust_type'))


# class ActionFormInfoSide(Action):
#     def name(self) -> Text:
#         return "form_info_side"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[EventType]:
#         required_slots = ["side","quantity","name"]

#         for slot_name in required_slots:
#             if tracker.slots.get(slot_name) is None:
#                 # The slot is not filled yet. Request the user to fill this slot next.
#                 return [SlotSet("requested_slot", slot_name)]

#         # All slots are filled.
#         return [SlotSet("requested_slot", None)]

# class ActionSubmitSide(Action):
#     def name(self) -> Text:
#         return "action_submit_side"

#     def run(
#         self,
#         dispatcher,
#         tracker: Tracker,
#         domain: "DomainDict",
#     ) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(template="utter_sideorder", quantity=tracker.get_slot('quantity'),side=tracker.get_slot('side')


class ActionFormInfoPizza(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_info_pizza"

    @staticmethod
    def required_slots(tracker: Tracker):
        # -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["food", "size", "topping", "crust_type", "quantity", "name", "number"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ):
        # -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_thanks", name=tracker.get_slot('name'),
                                 order=tracker.sender_id)
        dispatcher.utter_message(template="utter_food", quantity=tracker.get_slot('quantity'),
                                 size=tracker.get_slot('size'), food=tracker.get_slot('food'),
                                 topping=tracker.get_slot('topping'),
                                 crust_type=tracker.get_slot('crust_type'), location=tracker.get_slot("location"),
                                 restaurant_name=tracker.get_slot("restaurant_name"))
        # DataUpdate1(tracker.get_slot('name'),tracker.get_slot('number'),tracker.get_slot('vegpizza'),
        #            tracker.get_slot('nvegpizza'),tracker.get_slot('size'),tracker.get_slot('topping'),
        #            tracker.get_slot('crust_type'),tracker.get_slot('quantity'))
        return []

    def slot_mappings(self):
        # -> Dict[Text,Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "name": [self.from_entity(entity="name", intent='provide_name'),
                     self.from_text()],
            "food": [self.from_entity(entity="food", intent="food"),
                     self.from_text()],
            "size": [self.from_entity(entity="size", intent="psize"),
                     self.from_text()],
            "topping": [self.from_entity(entity="topping", intent="ptopping"),
                        self.from_text()],
            "crust_type": [self.from_entity(entity="crust_type", intent="pcrust"),
                           self.from_text()],
            "quantity": [self.from_entity(entity="quantity", intent="pquantity"),
                         self.from_text()],
            "number": [self.from_entity(entity="number", intent="provide_number"),
                       self.from_text()],
        }


class ActionFormInfoSide(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_info_side"

    @staticmethod
    def required_slots(tracker: Tracker):
        # -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["side", "quantity", "name", "number"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ):
        # -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_thanks", name=tracker.get_slot('name'),
                                 order=tracker.sender_id)

        dispatcher.utter_message(template="utter_sideorder", quantity=tracker.get_slot('quantity'),
                                 side=tracker.get_slot('side'),
                                 location=tracker.get_slot("location"),
                                 restaurant_name=tracker.get_slot("restaurant_name")
                                 )

        # DataUpdate2(tracker.get_slot('name'),tracker.get_slot('number'),tracker.get_slot('side'),
        #            )
        return []

    def slot_mappings(self):
        # -> Dict[Text,Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "name": [self.from_entity(entity="name", intent='provide_name'),
                     self.from_text()],
            "quantity": [self.from_entity(entity="quantity", intent="pquantity"),
                         self.from_text()],
            "side": [self.from_entity(entity="side", intent="order_side_menu"),
                     self.from_text()],
            "number": [self.from_entity(entity="number", intent="provide_number"),
                       self.from_text()],
        }


def get_trail_count(tracker):
    trail_count = tracker.get_slot("trail_count")
    if trail_count is None:
        return 1
    else:
        try:
            trail_count = int(trail_count) + 1
            return trail_count
        except:
            return 1


class ActionPizza(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_action_pizza"

    @staticmethod
    def required_slots(tracker: Tracker):
        # -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["location", "restaurant_name"]

    @staticmethod
    def _should_request_slot(tracker, slot_name):  # type: (Tracker, Text) -> bool
        """Check whether form action should request given slot"""
        return tracker.get_slot(slot_name) is None

    def request_next_slot(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: Dict[Text, Any],
    ):
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                trail_count = tracker.get_slot("trail_count")
                if slot == "location":
                    if trail_count is None:
                        print()
                        dispatcher.utter_message("May I know your location")
                    else:
                        dispatcher.utter_message("Enter valid location name")
                if slot == "restaurant_name":
                    location = tracker.get_slot("location")
                    weather_description = get_weather(location)
                    dispatcher.utter_message("It's feeling {} outside, a good pizza will make your day better".format(
                        weather_description))
                    dispatcher.utter_message(
                        "This are the restaurants found in the given location 1) Blaze Pizza"
                        " 2) Dominos Pizza 3) Mountain Mike 4) Pizza Hut 5) Curry Pizza")
                return [FollowupAction("action_listen"), SlotSet(REQUESTED_SLOT, slot)]

    def validate_location(self,
                          value: Text,
                          dispatcher: CollectingDispatcher,
                          tracker: Tracker,
                          domain: Dict[Text, Any], ):
        locations = zomato.get_cities(value)
        print(locations)
        if locations is not None and "id" in locations:
            location_id = locations.get("id")
            return {"location_id": location_id, "location": value}
        else:
            dispatcher.utter_message("")
            return {"location": None, "trail_count": get_trail_count(tracker)}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ):
        # -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        location = tracker.get_slot("location")
        restaurant_name = tracker.get_slot("restaurant_name")
        # dispatcher.utter_message("location : {} restaurant name {}".format(location, restaurant_name))
        dispatcher.utter_template("utter_veg_non_veg", tracker=tracker)

        # DataUpdate2(tracker.get_slot('name'),tracker.get_slot('number'),tracker.get_slot('side'),
        #            )
        return []

    def slot_mappings(self):
        # -> Dict[Text,Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "location": [self.from_entity(entity="location", intent='location_intent'),
                         self.from_entity(entity="GPE", intent='nlu_fallback'),
                         self.from_entity(entity="GPE", intent='vegetarian'),
                         self.from_entity(entity="GPE", intent='nonvegetarian'),
                         self.from_entity(entity="GPE", intent='order_vegpizza'),
                         self.from_entity(entity="GPE", intent='order_nvegpizza'),
                         self.from_text(),
                         ],
            "restaurant_name": [self.from_entity(entity="name", intent='provide_name'),
                                self.from_text()]
        }
