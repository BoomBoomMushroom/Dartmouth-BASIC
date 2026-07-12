from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import has_focus

# Editable buffers
programWindow = TextArea(scrollbar=True, multiline=True,)
commandWindow = TextArea(height=1, multiline=False,)

outputBuffer = FormattedTextControl(text="")
outputWindow = Window(content=outputBuffer)

# Override the print
def print(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")

    outputBuffer.text += sep.join(map(str, args)) + end

root_container = VSplit([
    HSplit([
        programWindow,
        Window(height=1, char='-'),
        commandWindow
    ]),
    Window(width=1, char='|'),
    outputWindow,
])

layout = Layout(root_container, focused_element=programWindow)

def onCommandWindowClose():
    commandWindow.text = "Do Ctrl-S to type commands; Use `RUN` to execute code"

def executeCommand(command: str):
    if command == "RUN":
        program = programWindow.text
        if len(program) == 0:
            outputBuffer.text = ""
            print("Type something in the program!")
            return

        import io
        import contextlib
        output = io.StringIO()

        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            import interpreter
            i = interpreter.Interpreter(programText=program)
            i.RUN()
        
        outputBuffer.text = output.getvalue()

    pass

kb = KeyBindings()
@kb.add('c-c')
def exit_(event):
    """
    Pressing Ctrl-C will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit()

@kb.add('c-s')
def _(event):
    commandWindow.text = ""
    event.app.layout.focus(commandWindow)
    pass

@kb.add('enter', filter=has_focus(commandWindow))
def _(event):
    if event.app.current_buffer != commandWindow.buffer: return

    event.app.layout.focus(programWindow)
    command = commandWindow.text

    onCommandWindowClose()
    executeCommand(command)


print("Use the `RUN` command to run your program!")
onCommandWindowClose()

app = Application(layout=layout, full_screen=True, key_bindings=kb)
app.run() # You won't be able to Exit this app

