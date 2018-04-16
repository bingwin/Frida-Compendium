# Send and receive data to and from instrumented process.
#
# Run: python send.py 
import frida
import sys


def on_message(message, data):
    print(message)


def load_script(script_name):
    with open(script_name) as f:
        script = f.read() 
    return script 


def main():
    # Attach on running process
    session = frida.attach("target.exe")

    # Instrumentation script 
    # Send message to host
    # Two events generated: send event, error event.
    jscode = load_script("send-complex.js")
    script = session.create_script(jscode)

    # Set a callback, when frida is sending a string, we print it out
    script.on('message', on_message)

    # Load the script
    script.load()

    # Delay
    # Execution is happened on other process so we need to make our script 
    # running all the way to the end
    try:
        while True:
            sys.stdin.read()
    except KeyboardInterrupt:
        session.detach()
        sys.exit(0)


if __name__ == '__main__':
    main()