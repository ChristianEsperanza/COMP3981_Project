import time

import GUI
from GUI import gui_updater
from Utility.enum import *
from Models import game_state


class Timer:

    def __init__(self, limit, player: Turn, context: GUI):
        self.limit = limit
        self.context = context
        self._total_agg_time = 0
        self.current_move_time = 0
        self.is_running = False
        self.player = player
        self.is_paused = False
        self.is_soft_paused = False

    def start_timer(self):
        print(f"Starting timer for {self.player.name}: {self._total_agg_time}")
        self.is_running = True

        time_start = time.time()
        timestamp = None
        turn_elapsed_time = None

        if self.is_paused:
            self.is_paused = False
            self.is_soft_paused = False
            print(f"Resuming timer with move time {self.current_move_time}")
        elif not self.is_soft_paused:
            self.current_move_time = 0
            # print("is_resumed False")

        while self.is_running:
            time.sleep(0.01)

            # print(self.current_move_time)
            turn_elapsed_time = time.time() - time_start + self.current_move_time
            # print(f"Turn time {turn_elapsed_time}")
            # print(f"self.current_move_time {self.current_move_time}")
            timestamp = time.time() - time_start + self._total_agg_time
            # move_time_stamp = turn_elapsed_time
            if self.player == Turn.WHITE:
                game_state.game_state['white']['total_time'] = timestamp
            else:
                game_state.game_state['black']['total_time'] = timestamp
            gui_updater.update_gui_total_time(self.context, self.player, int(timestamp))
            gui_updater.update_gui_move_time(self.context, self.player, int(turn_elapsed_time))

        # Timer stopped. Cache timer details.
        if game_state.game_state['game']['state'] == 'paused':
            self.current_move_time = turn_elapsed_time
            # print(f"Caching current move time {turn_elapsed_time}")
        if self.player == Turn.WHITE:
            # if not self.is_soft_paused:
            self._total_agg_time = game_state.game_state['white']['total_time']
            gui_updater.update_gui_total_time(self.context, Turn.WHITE, int(timestamp))
            gui_updater.update_gui_move_time(self.context, Turn.WHITE, int(self.current_move_time))
        else:
            # if not self.is_soft_paused:
            self._total_agg_time = game_state.game_state['black']['total_time']
            gui_updater.update_gui_total_time(self.context, Turn.BLACK, int(timestamp))
            gui_updater.update_gui_move_time(self.context, Turn.BLACK, int(self.current_move_time))

    def pause_timer(self):
        self.is_running = False

    def pause_timer_temp(self):
        self.is_running = False
        self.is_paused = True
        self.is_soft_paused = True
        # print("is_resumed True")

    def resume_timer(self):
        self.is_soft_paused = False

    def reset_timer(self):
        self.is_running = False
        self._total_agg_time = 0
        game_state.game_state['white']["total_time"] = 0
        game_state.game_state['white']["move_time"] = 0
        game_state.game_state['black']["total_time"] = 0
        game_state.game_state['black']["move_time"] = 0

        time.sleep(.1)
        gui_updater.update_gui_total_time(self.context, Turn.WHITE, 0)
        gui_updater.update_gui_move_time(self.context, Turn.WHITE, 0)
        gui_updater.update_gui_total_time(self.context, Turn.BLACK, 0)
        gui_updater.update_gui_move_time(self.context, Turn.BLACK, 0)
