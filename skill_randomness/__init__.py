"""A skill for all kinds of chance - make a choice, roll a die, flip a coin, etc."""
from icepool import Die, Pool
from ovos_bus_client.message import Message
from ovos_utils import classproperty
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill


class RandomnessSkill(OVOSSkill):
    """A skill for all kinds of chance - make a choice, roll a die, flip a coin, etc."""
    def __init__(self, *args, bus=None, skill_id="", **kwargs):
        super().__init__(*args, bus=bus, skill_id=skill_id, **kwargs)

    @classproperty
    def runtime_requirements(self):
        """Define any runtime requirements for the skill. This skill is entirely local with optional GUI."""
        return RuntimeRequirements(
            internet_before_load=False,
            network_before_load=False,
            gui_before_load=False,
            requires_internet=False,
            requires_network=False,
            requires_gui=False,
            no_internet_fallback=True,
            no_network_fallback=True,
            no_gui_fallback=True,
        )


    @intent_handler("make-a-choice.intent")
    def handle_make_a_choice_intent(self, message: Message):  # pylint: disable=unused-argument
        """Decide between two things."""
        first_choice = self.get_response("first-choice") or "the first one"
        second_choice = self.get_response("second-choice") or "the second one"
        result = Die([first_choice, second_choice]).sample()
        self.speak_dialog("choice-result", data={"choice": result})
        if self.gui:
            self.gui.show_text(result)
        if self.enclosure:
            self.enclosure.eyes_blink(2)
            self.enclosure.mouth_text(result)

    @intent_handler("pick-a-number.intent")  # TODO: Fix buffer overflow issue
    def handle_pick_a_number(self, message: Message):
        """Pick a number between two numbers."""
        lower_bound = message.data.get("lower", "")
        upper_bound = message.data.get("upper", "")
        if not lower_bound.isdigit() or not upper_bound.isdigit():
            lower_bound = 1
            upper_bound = 10
            self.speak_dialog("number-range-not-specified")
        if not lower_bound or not upper_bound:
            lower_bound = 1
            upper_bound = 10
            self.speak_dialog("number-range-not-specified")
        result = Die(range(int(lower_bound), int(upper_bound) + 1)).sample()
        self.speak_dialog("number-result", data={"number": result})
        if self.gui:
            self.gui.show_text(result)
        if self.enclosure:
            self.enclosure.eyes_look("left")
            self.enclosure.mouth_text(result)
            self.enclosure.eyes_look("right")

    @intent_handler("flip-a-coin.intent")
    def handle_flip_a_coin(self, message: Message):  # pylint: disable=unused-argument
        """Flip a coin."""
        self.play_audio("coin-flip.wav")
        result = Die(["heads", "tails"]).sample()
        self.speak_dialog("coin-result", data={"result": result})
        if self.gui:
            self.gui.show_text(result)
        if self.enclosure:
            self.enclosure.system_blink(3)
            self.enclosure.mouth_text(result)

    @intent_handler("fortune-teller.intent")
    def handle_fortune_teller(self, message: Message):  # pylint: disable=unused-argument
        """Get a random fortune."""
        self.play_audio("magic.mp3")
        fortune = self.get_response("fortune-query")
        answer = Die(["yes", "no"]).sample()
        self.speak_dialog("fortune-result", {"answer": answer})
        fortune_with_answer = f"{fortune}? ...{answer}"
        if self.gui:
            self.gui.show_text(fortune_with_answer)
        if self.enclosure:
            self.enclosure.eyes_spin()
            self.enclosure.mouth_text(fortune_with_answer)

    @intent_handler("roll-dice.intent")
    def handle_roll_dice(self, message: Message):
        """Roll a die."""
        self.play_audio("die-roll.wav")
        number = message.data.get("number", "1")  # TODO: Validate if we get a number or written number
        faces = message.data.get("faces", "6")
        if not number.isdigit() or not faces.isdigit():
            self.speak_dialog("unclear-dice", {"guess": f"{number} d {faces}"})
            return
        result = Pool(Die(range(1, faces + 1))).sum()
        self.speak_dialog("die-result", data={"result": result})
        if self.gui:
            self.gui.show_text(str(result))
        if self.enclosure:
            self.enclosure.eyes_spin()
            self.enclosure.mouth_text(str(result))
