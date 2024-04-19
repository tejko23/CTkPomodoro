from __future__ import annotations
from typing import Callable, Protocol

from .model import ConfigManager, Model


class View(Protocol):
    def mainloop(self) -> None: ...

    def bell(self) -> None: ...

    def run_job(self, time_ms: int, func: Callable) -> None: ...

    def cancel_job(self) -> None: ...

    def init_ui(self, config: ConfigManager, time: str) -> None: ...

    def set_clock_label(self, time: str) -> None: ...

    def bind_pomodoro_button(self, fn: Callable) -> None: ...

    def bind_break_button(self, fn: Callable) -> None: ...

    def bind_long_break_button(self, fn: Callable) -> None: ...

    def bind_button(self, type: str, command: Callable) -> None: ...

    def bind_ss_button(self, fn: Callable) -> None: ...


class PomodoroPresenter:
    def __init__(self, view: View, model: Model) -> None:
        self.view = view
        self.model = model

    def run(self) -> None:
        self.view.init_ui(config=self.model.config, time=str(self.model.timer))
        self.view.bind_button("pomodoro", lambda: self.set_time("pomodoro"))
        self.view.bind_button("break", lambda: self.set_time("break"))
        self.view.bind_button(
            "long_break", lambda: self.set_time("long_break")
        )
        self.view.bind_ss_button(self.handle_start_button)
        self.view.mainloop()

    def handle_stop_button(self) -> None:
        self.model.stop_timer()
        self.view.set_clock_label(str(self.model.timer))
        self.view.bind_ss_button(self.handle_start_button)

    def handle_start_button(self) -> None:
        self.model.start_timer()
        self.view.bind_ss_button(self.handle_stop_button)
        self.pomodoro()

    def set_time(self, time_type: str):
        self.model.set_time(time_type)
        self.view.set_clock_label(str(self.model.timer))

    def pomodoro(self) -> None:
        if self.model.state.is_running():
            self._update_running_state()
        elif self.model.state.is_finished():
            self._trigger_alert_on_finished_state()
        else:
            self._handle_stopped_state()

    def _update_running_state(self) -> None:
        self.view.set_clock_label(str(self.model.timer))
        self.model.finish_timer_if_done()
        self.view.run_job(200, self.pomodoro)

    def _trigger_alert_on_finished_state(self) -> None:
        self.view.bell()
        self.view.run_job(2000, self.pomodoro)

    def _handle_stopped_state(self) -> None:
        self.view.cancel_job()
