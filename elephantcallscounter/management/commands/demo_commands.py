import click


from elephantcallscounter.management.commands.data_analysis_commands import \
    analyse_multiple_audio_files
from elephantcallscounter.management.commands.data_analysis_commands import find_elephants_command
from elephantcallscounter.management.commands.data_analysis_commands import run_cnn
from elephantcallscounter.management.commands.event_commands import device_simulator


@click.command('run_demo')
@click.pass_context
def run_demo(context):
    context.invoke(device_simulator)
    context.invoke(analyse_multiple_audio_files)
    context.invoke(find_elephants_command)
    context.invoke(run_cnn)
