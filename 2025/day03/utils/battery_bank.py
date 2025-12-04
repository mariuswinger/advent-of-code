from __future__ import annotations

from dataclasses import dataclass

from day03.utils.argmax import argmax


@dataclass
class BatteryBank:
    joltages: tuple[int, ...]

    def __len__(self) -> int:
        return len(self.joltages)

    def get_largest_joltage(self, battery_count: int = 2) -> int:
        batteries = []
        search_window_start_index = 0
        for i in range(battery_count):
            remaining_battery_count = battery_count - i
            max_digit, max_digit_index = argmax(
                self.joltages,
                start_index=search_window_start_index,
                end_index=len(self) - remaining_battery_count + 1,
            )
            batteries.append(max_digit)
            search_window_start_index = max_digit_index + 1

        return int("".join(map(str, batteries)))


#   one battery => find max
#   two batteries => use prev max
#       if numbers to the right
#           find largest number to the right => done
#       else
#           find largest number to the left => done
#   three batteries => use prev max
#       if numbers to the right
#           find largest number to the right => done
#       else
#           find largest number to the left => done
#
#
#           41115117
#           412151176 => 7, 76, 576, 4576 42576, 421576
