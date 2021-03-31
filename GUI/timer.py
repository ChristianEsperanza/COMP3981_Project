import time

import GUI
from GUI import gui_updater
from Utility.enum import *
from Models import game_state


class Timer:

    def __init__(self, limit, player: Turn, context: GUI, elapsed=0):
        self.limit = limit
        self.context = context
        self._total_agg_time = 0
        self.is_running = False
        self.player = player
        self.is_paused = False

    def start_timer(self):
        print(f"Starting timer for {self.player.name}: {self._total_agg_time}")
        # self.is_paused = False
        self.is_running = True

        time_start = time.time()
        time_stamp = None
        turn_elapsed_time = None
        while self.is_running:
            turn_elapsed_time = time.time() - time_start
            timestamp = turn_elapsed_time + self._total_agg_time
            if self.player == Turn.WHITE:
                game_state.game_state['white']['total_time'] = timestamp
            else:
                game_state.game_state['black']['total_time'] = timestamp
            gui_updater.update_gui_total_time(self.context, self.player, timestamp)
            gui_updater.update_gui_move_time(self.context, self.player, turn_elapsed_time)
            time.sleep(0.1)

        if self.player == Turn.WHITE:
            self._total_agg_time = game_state.game_state['white']['total_time']
            gui_updater.update_gui_total_time(self.context, Turn.WHITE, self._total_agg_time)
            gui_updater.update_gui_move_time(self.context, Turn.WHITE, turn_elapsed_time)
        else:
            self._total_agg_time = game_state.game_state['black']['total_time']
            gui_updater.update_gui_total_time(self.context, Turn.BLACK, self._total_agg_time)
            gui_updater.update_gui_move_time(self.context, Turn.BLACK, turn_elapsed_time)


    def pause_timer(self):
        self.is_running = False

    # def resume_timer(self):
