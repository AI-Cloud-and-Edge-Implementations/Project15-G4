#!/usr/bin/env python
from elephantcallscounter.management.commands.command_groups import entry_point
from elephantcallscounter.management.commands.data_import_commands import data_import
from elephantcallscounter.management.commands.data_analysis_commands import data_analysis
from elephantcallscounter.management.commands.data_processing_commands import data_processing


if __name__ == "__main__":
    entry_point.add_command(data_import)
    entry_point.add_command(data_analysis)
    entry_point.add_command(data_processing)
    entry_point(obj = {})
