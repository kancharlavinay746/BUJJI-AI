from brain.router import Router

router = Router()

while True:
    cmd = input("Command: ")

    if cmd == "exit":
        break

    print(router.route(cmd))