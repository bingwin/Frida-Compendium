# Attach on running process and call a function with user-defined argument.
#
# Run: python call.py 
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

    # Address is in hex form
    addr = 0
    if len(sys.argv) > 1:
        addr = int(sys.argv[1], 16)
    else:
        addr = int(input("Address: "), 16)

    # Instrumentation script 
    # Hook to native function on certain address ex: ptr("0x123456")
    # returning void
    # with list of arguments ['int']
    jscode = load_script("call.js")
    script = session.create_script(jscode % (addr))

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