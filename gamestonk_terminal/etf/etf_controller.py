"""ETF Controller"""
__docformat__ = "numpy"

import argparse
from typing import List
import matplotlib.pyplot as plt
from prompt_toolkit.completion import NestedCompleter
from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.helper_funcs import get_flair
from gamestonk_terminal.menu import session
from gamestonk_terminal.etf.stockanalysis_model import (
    name_search,
    open_web,
    etf_overview,
    compare_etfs,
    etf_holdings,
)


class ETFController:
    CHOICES = ["help", "q", "quit", "web", "search", "overview", "compare", "holdings"]

    def __init__(self):
        """CONSTRUCTOR"""

        self.etf_parser = argparse.ArgumentParser(add_help=False, prog="etf")
        self.etf_parser.add_argument("cmd", choices=self.CHOICES)

    def print_help(self):
        """Print help"""
        print(
            "https://github.com/GamestonkTerminal/GamestonkTerminal/tree/main/gamestonk_terminal/etf"
        )
        print("\nETF:")
        print("   help          show this menu again")
        print("   q             quit this menu, and shows back to main menu")
        print("   quit          quit to abandon program")
        print("\nStockAnalysis.com")
        print("   web           open StockAnalysis.com/etf")
        print("   search        search ETFs matching name (i.e. BlackRock or Invesco)")
        print("   overview      get overview of ETF symbol")
        print("   holdings      get top holdings for ETF")
        print("   compare       compare overview of multiple ETF")

        print("")

    def switch(self, an_input: str):
        """Process and dispatch input

        Returns
        -------
        True, False or None
            False - quit the menu
            True - quit the program
            None - continue in the menu
        """
        (known_args, other_args) = self.etf_parser.parse_known_args(an_input.split())

        return getattr(
            self, "call_" + known_args.cmd, lambda: "Command not recognized!"
        )(other_args)

    def call_help(self, _):
        """Process Help command"""
        self.print_help()

    def call_q(self, _):
        """Process Q command - quit the menu"""
        return False

    def call_quit(self, _):
        """Process Quit command - quit the program"""
        return True

    def call_web(self, other_args: List[str]):
        """Process web command"""
        open_web(other_args)

    def call_search(self, other_args: List[str]):
        """Process search command"""
        name_search(other_args)

    def call_overview(self, other_args: List[str]):
        """Process overview command"""
        etf_overview(other_args)

    def call_holdings(self, other_args: List[str]):
        """Process holdings command"""
        etf_holdings(other_args)

    def call_compare(self, other_args):
        """Process compare command"""
        compare_etfs(other_args)


def menu():
    etf_controller = ETFController()
    etf_controller.print_help()
    plt.close("all")
    while True:
        # Get input command from user
        if session and gtff.USE_PROMPT_TOOLKIT:
            completer = NestedCompleter.from_nested_dict(
                {c: None for c in etf_controller.CHOICES}
            )
            an_input = session.prompt(
                f"{get_flair()} (etf)> ",
                completer=completer,
            )
        else:
            an_input = input(f"{get_flair()} (etf)> ")

        try:
            process_input = etf_controller.switch(an_input)

            if process_input is not None:
                return process_input

        except SystemExit:
            print("The command selected doesn't exist\n")
            continue
