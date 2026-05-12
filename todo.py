def load_tasks():
    try:
        with open("todos.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open("todos.txt", "w") as f:
        for task in tasks:
            f.write(task + "\n")

def show_tasks(tasks):
    print("\nTask list:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

def main():
    tasks = load_tasks()

    while True:
        print("\n1 - add task")
        print("2 - view tasks")
        print("3 - exit")

        choice = input("Choose: ")

        if choice == "1":
            task = input("Enter task: ")
            tasks.append(task)
            save_tasks(tasks)

        elif choice == "2":
            show_tasks(tasks)

        elif choice == "3":
            break

        else:
            print("Invalid input")

if __name__ == "__main__":
    main()
