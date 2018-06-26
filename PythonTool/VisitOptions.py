import argparse
import ast

from visit import *

import MultipleWindows as Mw
import MultiSlice as Ms
import Orbit as Or


class VisitOptions(object):
    """
    Terminal execution settings.

    All of the following inserts data appropriately into scripts
    based on inputs to the terminal.
    """

    def __init__(self, Arguments=None, FilePlots=None, OperatorSet=None):
        self.Arguments = Arguments
        self.FilePlots = FilePlots
        self.OperatorSet = OperatorSet

    def Images(self):
        try:
            Mw.MultipleWindows(self.FilePlots, self.OperatorSet)
        except Exception:
            Mw.MultipleWindows(self.FilePlots)

    def Windows(self):
        try:
            Mw.MultipleWindows(self.FilePlots, self.OperatorSet, Windows=True)
        except Exception:
            Mw.MultipleWindows(self.FilePlots, Windows=True)

    def Default(self):
        self.OperatorSet = [
                           ["Slice", ("x")],
                           ["Slice", ("y")],
                           ["Slice", ("z")],
                           [{"Clip": {"oct": (1, 1, 1)}}],
                           ]

        Mw.MultipleWindows(self.FilePlots, self.OperatorSet, Windows=True)

    def MultiSlice(self):
        Axis = ast.literal_eval(self.Arguments.multislice)[0]
        Number = ast.literal_eval(self.Arguments.multislice)[1]
        myList = (str(Axis), int(Number))

        Ms.MultiSlice(self.FilePlots, myList)

    def Orbit(self):

        try:
            if self.OperatorSet is None:
                self.OperatorSet = False
        except Exception:
            pass

        Direction = ast.literal_eval(self.Arguments.orbit)[0]
        Iteration = ast.literal_eval(self.Arguments.orbit)[1]

        Or.Orbit(self.FilePlots, (Direction, Iteration), self.OperatorSet)
