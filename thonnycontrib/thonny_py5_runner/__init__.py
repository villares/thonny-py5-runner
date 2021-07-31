import subprocess
import sys
import os
from collections import namedtuple
import site
from tkinter.messagebox import showinfo
from thonny import get_workbench

name = "thonny-py5-runner"

ErrorMessage = namedtuple("ErrorMessage", ["error_type", "description"])

SUCCESS = "All done!"

NO_TEXT_TO_FORMAT = ErrorMessage("Nothing to do here", "There is no bot to execute.")
PACKAGE_NOT_FOUND = ErrorMessage(
    "Package not found",
    "Could not find py5/sbot. Is it installed and on your PATH?",
)
NOT_COMPATIBLE = ErrorMessage(
    "File not compatible!",
    "Looks like this is not a Python file. Did you already save it?",
)

# Temporary fix: this function comes from thonny.running, but importing that
# module may conflict with outdated Thonny installations from some Linux
# repositories.
# TODO: change this with thonny.running.get_interpreter_for_subprocess when
# possible and change Thonny version required.
_console_allocated = False


def get_interpreter_for_subprocess(candidate=None):
    if candidate is None:
        candidate = sys.executable

    pythonw = candidate.replace("python.exe", "pythonw.exe")
    if not _console_allocated and os.path.exists(pythonw):
        return pythonw
    else:
        return candidate.replace("pythonw.exe", "python.exe")


class py5Sbot:
    """
    Call py5's sbot command with the open source code document as argument

    Using subprocess, sbot is executed to run .bot or .py files displayed in
    Thonny. Whenever this plugin is executed, run_with_sbot is called. Depending
    on the result, final_title and final_message is displayed through
    tkinter.messagebox.showinfo().
    """

    def __init__(self) -> None:
        """Get the workbench to be later used to detect the file to format."""
        self.workbench = get_workbench()

    def run_with_sbot(self) -> None:
        """Handle the plugin execution."""
        self.editor = self.workbench.get_editor_notebook().get_current_editor()

        try:
            self.filename = self.editor.get_filename()
        except AttributeError:
            final_title = NO_TEXT_TO_FORMAT.error_type
            final_message = NO_TEXT_TO_FORMAT.description
        else:
            if self.filename is not None and self.filename[-3:] in (".py", "bot"):
                self.editor.save_file()
                sp = site.getsitepackages()[0] 
                py5_runner = os.path.join(sp, 'py5_tools', 'tools', 'run_sketch.py')
                run_sketch = subprocess.run(
                   [get_interpreter_for_subprocess(), "-m", py5_runner, self.filename, "-S"],
                  #  ["sbot", self.filename], 
                    capture_output=True,
                    text=True,
                )

                if run_sketch.stderr.find('No sbot found!') != -1:
                    final_title = PACKAGE_NOT_FOUND.error_type
                    final_message = PACKAGE_NOT_FOUND.description
                else:
                    # Emojis are not supported in Tkinter.
                    message_without_emojis = run_sketch.stderr.encode(
                        'ascii', 'ignore'
                    ).decode()
                    if run_sketch.returncode != 0:
                        final_title = 'Oh no!'
                        final_message = '\n'.join(
                            message_without_emojis.splitlines()[::2]
                        )

                        final_message = final_message[0].upper() + final_message[1:]

                    else:
                        self.editor._load_file(self.filename, keep_undo=True)
                        final_title = 'Done'
                        final_message = message_without_emojis.splitlines()[-1]  
            else:
                final_title = NOT_COMPATIBLE.error_type
                final_message = NOT_COMPATIBLE.description

        showinfo(title=final_title, message=final_message)

    def load_plugin(self) -> None:
        """
        Load the plugin on runtime.

        Using self.workbench.add_command(), the plugin is registered in Thonny
        with all the given arguments.
        """
        self.workbench.add_command(
            command_id="run_with_sbot",
            menu_name="tools",
            command_label="Execute py5's run_sketch command",
            handler=self.run_with_sbot,
            default_sequence="<Control-Alt-5>",
            extra_sequences=["<<CtrlAlt5InText>>"],
        )


if get_workbench() is not None:
    run = py5Sbot().load_plugin()
