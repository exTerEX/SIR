#!/usr/bin/env python

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

default_kwargs = {
    "N0": (100, 1, 0),
    "T": 100,
    "dt": 0.1
}

plot_default_kwargs = {
    "facecolor": "#dddddd"
}


class SIR:
    def __init__(self, beta: float, gamma: float, ** kwargs) -> None:
        # TODO: Check beta/gamma
        self._beta = beta
        self._gamma = gamma

        kwargs = {**default_kwargs, **kwargs}

        if not isinstance(kwargs["N0"], (tuple, list)):
            raise TypeError

        if not isinstance(kwargs["T"], (int, float)):
            raise TypeError

        if not isinstance(kwargs["dt"], (int, float)):
            raise TypeError

        if kwargs["dt"] > kwargs["T"]:
            raise ValueError

        self._N0 = kwargs["N0"]
        self._T = kwargs["T"]
        self._dt = kwargs["dt"]

        self._calculate()

    def __call__(self, u: tuple, t: float) -> tuple:
        S, I, R = u

        return (-self._beta * S * I / sum(u),
                self._beta * S * I / sum(u) - self._gamma * I, self._gamma * I)

    def solve(self, u0: tuple, t: float) -> tuple:

        if not isinstance(u0, (list, tuple)):
            raise TypeError

        for element in u0:
            if not isinstance(element, (int, float)):
                raise ValueError

        if not isinstance(t, (int, float, np.ndarray)):
            raise TypeError

        return integrate.odeint(self, u0, t)

    def _calculate(self) -> None:
        self._total = sum(self._N0)
        self._t = t = np.linspace(0, self._T, int(self._T / self._dt))
        self._n = self.solve(self._N0, t)

    @property
    def show(self) -> None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5), dpi=150)
        fig.tight_layout()
        fig.set_facecolor("w")

        labels = ("Susceptible", "Infected", "Recovered")

        self._ax1 = ax1
        self._left_plot(labels)

        self._ax2 = ax2
        self._right_plot(labels)

        plt.show()

    def _left_plot(self, labels, **kwargs) -> None:
        kwargs = {**plot_default_kwargs, **kwargs}

        ax = self._ax1

        ax.set_title("Distribution of compartments per time", fontsize=12)

        ax.set_facecolor(kwargs["facecolor"])

        for label, element in zip(labels, self._n.T):
            ax.plot(self._t, element / self._total, alpha=0.5, lw=2, label=label)

        ax.set_xlabel("Time")
        ax.set_ylabel("Population")
        ax.set_ylim(0.0, 1.0)

        ax.xaxis.set_tick_params(length=0)
        ax.yaxis.set_tick_params(length=0)

        ax.grid(which="major", c="w", lw=2, ls="-")
        ax.set_axisbelow(True)

        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)

        for spine in ("top", "right", "bottom", "left"):
            ax.spines[spine].set_visible(False)

    def _right_plot(self, labels, **kwargs) -> None:
        kwargs = {**plot_default_kwargs, **kwargs}

        ax = self._ax2

        ax.set_title("Distribution at last time-point", fontsize=14)

        ax.set_facecolor(kwargs["facecolor"])

        for label, element in zip(labels, self._n[-1] / self._total):
            ax.bar(label[0], round(element, 2))

        ax.set_ylim(0.0, 1.0)

        ax.xaxis.set_tick_params(length=0)
        ax.yaxis.set_tick_params(length=0)

        ax.grid(which="major", c="w", lw=2, ls="-")
        ax.set_axisbelow(True)

        for spine in ("top", "right", "bottom", "left"):
            ax.spines[spine].set_visible(False)
