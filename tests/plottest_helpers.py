#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.testing.compare import compare_images
import pytest


@pytest.fixture()
def disable_diff_save(monkeypatch):
    def do_nothing(*args, **kwargs):
        pass

    monkeypatch.setattr(
        matplotlib.testing.compare, 'save_diff_image', do_nothing
    )


@pytest.fixture
def assert_image_equal(disable_diff_save, pytestconfig):
    def inner(name, tol=1e-6):
        path = './reference_plots/' + name + '.png'
        if not os.path.exists(path):
            plt.savefig(path)
            raise ValueError('Reference plot did not exist.')
        else:
            with tempfile.NamedTemporaryFile(suffix='.png') as fp:
                plt.savefig(fp.name)
                if not pytestconfig.option.no_plot_compare:
                    assert compare_images(
                        path, fp.name, tol=tol, in_decorator=True
                    ) is None

    return inner
