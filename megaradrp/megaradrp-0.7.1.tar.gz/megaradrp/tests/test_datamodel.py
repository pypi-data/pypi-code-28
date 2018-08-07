#
# Copyright 2015-2018 Universidad Complutense de Madrid
#
# This file is part of Megara DRP
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#


import astropy.io.fits as fits
import astropy.table
import pytest

from ..datamodel import MegaraDataModel, FibersConf


def create_empty_img(insmode):
    img = fits.HDUList([fits.PrimaryHDU()])
    img[0].header['insmode'] = insmode
    return img


BASE_LCB = ("LCB", 'b7dcd9d1-0b60-4b43-b26e-d2c9868d5e20', 9, 623)
BASE_MOS = ("MOS", '00000000-0000-0000-0000-000000000000', 92, 644)


@pytest.mark.parametrize("name, confid, nbundles, nfibers",
                         [BASE_LCB, BASE_MOS])
def test_fiberconf_1(name, confid, nbundles, nfibers):

    datamodel = MegaraDataModel()

    img = create_empty_img(name)

    conf = datamodel.get_fiberconf(img)

    assert isinstance(conf, FibersConf)
    # Default values from file
    assert conf.name == name
    assert conf.conf_id == confid
    assert conf.nbundles == nbundles
    assert conf.nfibers ==  nfibers


def test_fiberconf_other():

    datamodel = MegaraDataModel()

    img = create_empty_img('OTHER')

    with pytest.raises(ValueError):
        datamodel.get_fiberconf(img)


@pytest.mark.parametrize("name, confid, nbundles, nfibers",
                         [BASE_LCB, BASE_MOS])
def test_bundles_to_table(name, confid, nbundles, nfibers):

    datamodel = MegaraDataModel()

    img = create_empty_img(name)

    conf = datamodel.get_fiberconf(img)

    bundles_t = conf.bundles_to_table()
    assert isinstance(bundles_t, astropy.table.Table)
    assert len(bundles_t) == nbundles
    assert bundles_t.colnames == ['bundle_id', 'x', 'y', 'pa', 'enabled',
                                  'target_type', 'target_priority', 'target_name']


@pytest.mark.parametrize("name, confid, nbundles, nfibers",
                         [BASE_LCB, BASE_MOS])
def test_fibers_to_table(name, confid, nbundles, nfibers):

    datamodel = MegaraDataModel()

    img = create_empty_img(name)

    conf = datamodel.get_fiberconf(img)

    fibers_t = conf.fibers_to_table()
    assert isinstance(fibers_t, astropy.table.Table)
    assert len(fibers_t) == nfibers
    assert fibers_t.colnames == ['fibid', 'name', 'x', 'y',
                                 'inactive', 'valid',
                                 'bundle_id']
