from datetime import datetime, timedelta
from unittest.mock import patch
import unittest

from pomodoro import Timer, StateController, TimerState


class TestTimer(unittest.TestCase):

    def setUp(self):
        self.timer = Timer("10:00")

    def test_timer_exists(self):
        self.assertIsNotNone(self.timer)

    def test_time_str(self):
        self.assertEqual(str(self.timer), "10:00")

    def test_timer_state(self):
        self.assertEqual(self.timer.state.is_running(), False)

    def test_time_property(self):
        self.assertEqual(self.timer.time, "10:00")
        self.assertIsInstance(self.timer.time, str)
        self.timer._time = timedelta(seconds=120)
        self.assertEqual(self.timer.time, "02:00")

    def test_time_setter(self):
        self.timer.time = "20"
        self.assertEqual(self.timer.time, "20:00")

    def test_time_setter_raises_type_error(self):
        self.assertRaises(TypeError, Timer, 10)

    def test_time_setter_raises_value_error(self):
        self.assertRaises(ValueError, Timer, "abc")

    def test_refresh_end_time(self):
        now = datetime.now()
        self.timer._time = timedelta(seconds=120)
        self.timer.refresh_end_time()
        self.assertGreater(self.timer._end_time, now)

    def test_time_property_timer_running_before_end_time(self):
        # Set timer state to running
        self.timer.state.start()

        # Set a future end time for the timer
        future_end_time = datetime.now() + timedelta(minutes=5)
        self.timer._end_time = future_end_time

        # Mock datetime.now() to return a time before the end time
        with patch("pomodoro.model.timer.datetime") as mocked_datetime:
            # Set the mocked current time to a moment just before the future end time
            mocked_datetime.now.return_value = future_end_time - timedelta(
                seconds=10
            )

            # Calculate the expected remaining time based on the mocked time
            expected_remaining_time = "00:10"  # Oczekiwany pozostały czas na podstawie zmocowanego czasu

            # Sprawdź, czy właściwość time zwraca oczekiwany pozostały czas
            self.assertEqual(self.timer.time, expected_remaining_time)

    def test_time_property_timer_running_past_end_time(self):
        self.timer.state.start()

        # Set a past end time for the timer
        past_end_time = datetime.now() - timedelta(minutes=1)
        self.timer._end_time = past_end_time

        # Mock datetime.now() to return a time after the end time
        with patch("datetime.datetime") as mocked_datetime:
            mocked_datetime.now.return_value = past_end_time + timedelta(
                minutes=1
            )

            # Check that the time property returns "00:00" or a similar expected value
            expected_remaining_time = (
                "00:00"  # Adjust this based on the expected remaining time
            )
            self.assertEqual(self.timer.time, expected_remaining_time)


class TestStateController(unittest.TestCase):

    def setUp(self):
        self.state_controller = StateController()

    def test_initialization(self):
        self.assertEqual(self.state_controller.state, TimerState.STOPPED)

    def test_start(self):
        self.state_controller.start()
        self.assertEqual(self.state_controller.state, TimerState.RUNNING)

    def test_stop(self):
        self.state_controller.stop()
        self.assertEqual(self.state_controller.state, TimerState.STOPPED)

    def test_finish(self):
        self.state_controller.finish()
        self.assertEqual(self.state_controller.state, TimerState.FINISHED)

    def test_is_running(self):
        self.state_controller.start()
        self.assertTrue(self.state_controller.is_running())

    def test_is_finished(self):
        self.state_controller.finish()
        self.assertTrue(self.state_controller.is_finished())

    def test_is_stopped(self):
        self.state_controller.stop()
        self.assertTrue(self.state_controller.is_stopped())


class TestTimerState(unittest.TestCase):

    def test_enum_values(self):
        self.assertEqual(TimerState.RUNNING.value, "running")
        self.assertEqual(TimerState.STOPPED.value, "stopped")
        self.assertEqual(TimerState.FINISHED.value, "finished")
