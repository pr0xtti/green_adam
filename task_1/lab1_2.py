from pprint import pformat, pprint
from typing import Callable, Any


def main():
    def create_handlers(callback: Callable) -> list[Callable]:
        # Make a new handler with decorator
        def make_handler(original_func: Callable, param: int):
            def new_handler() -> Any:
                return original_func(param)
            return new_handler

        # Adding handlers per each step (from 0 to 4)
        handlers: list = [
            make_handler(callback, step)
            for step in range(5)
        ]
        return handlers

    def execute_handlers(handlers: list[Callable]) -> list[Any]:
        # start added handlers (steps from 0 to 4)
        results: list = [
            handler()
            for handler in handlers
        ]
        return results

    def do_smth(deed):
        print(f"executing {deed} ...")
        return f"deed: {deed}"

    print(f"Making workers ...")
    workers = create_handlers(do_smth)
    # pprint(f"workers:\n {workers}")

    print(f"Executing ...")
    res = execute_handlers(workers)
    pprint(f"results:\n {res}")


if __name__ == '__main__':
    main()
