"""A skill for all kinds of chance - make a choice, roll a die, flip a coin, etc."""
from os.path import dirname
from random import randint

from icepool import Die, d6, d
from ovos_bus_client.message import Message
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill


class RandomnessSkill(OVOSSkill):
    """A skill for all kinds of chance - make a choice, roll a die, flip a coin, etc."""
    @intent_handler("make-a-choice.intent")
    def handle_make_a_choice_intent(self, message: Message):  # pylint: disable=unused-argument
        """Decide between two things."""
        first_choice = self.get_response("first-choice") or "the first one"
        second_choice = self.get_response("second-choice") or "the second one"
        try:
            result = Die([first_choice, second_choice]).sample()
        except TypeError:
            result = Die(first_choice, second_choice).sample()
        self.speak_dialog("choice-result", data={"choice": result})
        self.gui.show_text(result)
        self.enclosure.eyes_blink(2)
        self.enclosure.mouth_text(result)

    @intent_handler("pick-a-number.intent")
    def handle_pick_a_number(self, message: Message):
        """Pick a number between two numbers."""
        lower_bound = message.data.get("lower", "")
        upper_bound = message.data.get("upper", "")
        self.log.debug(f"Lower: {lower_bound}, Upper: {upper_bound}")
        try:
            upper_bound = round(float(upper_bound))
            lower_bound = round(float(lower_bound))
        except ValueError:
            lower_bound = 1
            upper_bound = 10
            self.speak_dialog("number-range-not-specified")
        result = randint(lower_bound, upper_bound)
        self.speak_dialog("number-result", data={"number": result})
        self.gui.show_text(str(result))
        self.enclosure.eyes_spin()
        self.enclosure.mouth_text(str(result))

    @intent_handler("flip-a-coin.intent")
    def handle_flip_a_coin(self, message: Message):  # pylint: disable=unused-argument
        """Flip a coin."""
        self.play_audio(f"{dirname(__file__)}/coin-flip.wav")
        try:
            result = Die(["heads", "tails"]).sample()
        except TypeError:
            result = Die("heads", "tails").sample()
        self.speak_dialog("coin-result", data={"result": result})
        self.gui.show_text(result)
        self.enclosure.system_blink(3)
        self.enclosure.mouth_text(result)

    @intent_handler("fortune-teller.intent")
    def handle_fortune_teller(self, message: Message):  # pylint: disable=unused-argument
        """Get a random fortune."""
        self.play_audio(f"{dirname(__file__)}/magic.mp3")
        fortune = self.get_response("fortune-query")
        try:
            answer = Die(["yes", "no"]).sample()
        except TypeError:
            answer = Die("yes", "no").sample()
        self.speak_dialog("fortune-result", {"answer": answer})
        fortune_with_answer = f"{fortune}? ...{answer}"
        self.gui.show_text(fortune_with_answer)
        self.enclosure.eyes_spin()
        self.enclosure.mouth_text(fortune_with_answer)

    @intent_handler("roll-dice.intent")
    def handle_roll_dice(self, message: Message):
        """Roll a die."""
        self.log.debug(f"Roll dice message: {message.serialize()}")
        self.play_audio(f"{dirname(__file__)}/die-roll.wav")
        number = message.data.get("number", 1)
        faces = message.data.get("faces", 6)
        result = 0
        if int(number) > 1:
            self.log.debug(f"rolling {number} dice")
            result_string = ""
            for _ in range(1, int(number) + 1):
                # Create a dialog string
                r = Die(d(int(faces))).sample()
                result += r
                result_string = result_string + ", " + str(r)
            result = result_string + f" for a total of {result}"
        else:
            result = Die(d(int(faces))).sample()
        self.speak_dialog("die-result", data={"result": result})
        self.gui.show_text(str(result))
        self.enclosure.eyes_spin()
        self.enclosure.mouth_text(str(result))

    @intent_handler("roll-common-dice.intent")
    def handle_roll_common_dice(self, message: Message):
        """Roll traditional six-sided dice."""
        self.play_audio(f"{dirname(__file__)}/die-roll.wav")
        self.log.debug("Rolling a six-sided die")
        result = d6.sample()
        self.speak_dialog("die-result", data={"result": result})
        self.gui.show_text(str(result))
        self.enclosure.eyes_spin()
        self.enclosure.mouth_text(str(result))
