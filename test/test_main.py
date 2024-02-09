# pylint: disable=missing-docstring
from threading import Event
from unittest.mock import Mock
import pytest
# from skill_randomness import RandomnessSkill
from ovos_plugin_manager.skills import find_skill_plugins
from ovos_utils.fakebus import FakeBus
# TODO: Mock settings path, set up fixtures


def test_skill_is_a_valid_plugin():
    assert "skill-randomness.mikejgray" in find_skill_plugins()

if __name__ == "__main__":
    pytest.main()
