import sys
from io import StringIO

def start(stdout):
    original = stdout
    # Save the current sys.stdout
    captured_output = StringIO()

    # Redirect sys.stdout to the captured_output
    stdout = captured_output

    return original, captured_output

def stop(original_stdout, captured_output):
    # Restore sys.stdout to its original value
    sys.stdout = original_stdout

    # Return the captured output
    return captured_output.getvalue()

