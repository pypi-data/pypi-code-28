#
# Copyright 2011-2018 Universidad Complutense de Madrid
#
# This file is part of Megara DRP
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

"""Acquisition with LCB"""


import math

import numpy as np
from scipy.spatial import KDTree

from numina.core import Product, Parameter
from numina.constants import FWHM_G

from megaradrp.recipes.scientific.base import ImageRecipe
from megaradrp.types import ProcessedRSS, ProcessedFrame


class AcquireLCBRecipe(ImageRecipe):
    """Process Acquisition LCB images.

    This recipe processes a set of acquisition images
    obtained in **LCB Acquisition** mode and returns
    the offset and rotation required to center the
    fiducial object in its reference positions.

    See Also
    --------
    megaradrp.recipes.auxiliary.acquisitionmos.AcquireMOSRecipe

    Notes
    -----
    Images provided by `obresult` are trimmed and corrected
    from overscan, bad pixel mask (if `master_bpm` is not None),
    bias, dark current (if `master_dark` is not None) and
    slit-flat (if `master_slitflat` is not None).

    Images thus corrected are the stacked using the median.
    The result of the combination is saved as an intermediate result, named
    'reduced_image.fits'. This combined image is also returned in the field
    `reduced_image` of the recipe result.

    The apertures in the 2D image are extracted, using the information in
    `master_traces` and resampled according to the wavelength calibration in
    `master_wlcalib`. Then is divided by the `master_fiberflat`.
    The resulting RSS is saved as an intermediate
    result named 'reduced_rss.fits'. This RSS is also returned in the field
    `reduced_rss` of the recipe result.

    The sky is subtracted by combining the the fibers marked as `SKY`
    in the fibers configuration. The RSS with sky subtracted is returned ini the
    field `final_rss` of the recipe result.

    Then, the centroid of the fiducial object nearest to the center of the field
    is computed. The offset needed to center
    the fiducial object in the center of the LCB is returned.

    """

    # Requirements are defined in base class
    points = Parameter([(0, 0)], "Coordinates")
    extraction_region = Parameter(
        [1000, 3000],
        description='Region used to compute a mean flux',
        nelem=2
    )


    reduced_image = Product(ProcessedFrame)
    reduced_rss = Product(ProcessedRSS)
    final_rss = Product(ProcessedRSS)
    offset = Product(list)
    rotang = Product(float)

    def run(self, rinput):

        self.logger.info('starting AC LCB reduction')

        reduced2d, reduced1d = super(AcquireLCBRecipe, self).base_run(rinput)
        # rssdata = rss_data[0].data

        do_sky_subtraction = True
        if do_sky_subtraction:
            self.logger.info('start sky subtraction')
            final, origin, sky = self.run_sky_subtraction(reduced1d)
            self.logger.info('end sky subtraction')
        else:
            final =  reduced1d
            origin = final
            sky = final

        fiberconf = self.datamodel.get_fiberconf(final)
        self.logger.debug("LCB configuration is %s", fiberconf.conf_id)

        rssdata = final[0].data

        scale, funit = self.datamodel.fiber_scale_unit(final, unit=True)
        self.logger.debug('unit is %s', funit)
        platescale = self.datamodel.PLATESCALE

        cut1, cut2 = rinput.extraction_region

        # points = [(0, 0)] # Center of fiber 313
        points = list(rinput.points)

        flux_per_cell_all = rssdata[:, cut1:cut2].mean(axis=1)

        max_cell = flux_per_cell_all.argmax() + 1
        max_fiber_ = fiberconf.fibers[max_cell]

        self.logger.info("maximum flux in spaxel %d -- %s", max_cell, max_fiber_.name)
        # Extend points with the brightest spaxel
        points.append((max_fiber_.x, max_fiber_.y))

        fibers = fiberconf.conected_fibers(valid_only=True)

        grid_coords = []
        for fiber in fibers:
            grid_coords.append((fiber.x, fiber.y))
        # setup kdtree for searching
        kdtree = KDTree(grid_coords)

        # Other posibility is
        # query using radius instead
        # radius = 1.2
        # kdtree.query_ball_point(points, k=7, r=radius)

        npoints = 19 + 18
        # 1 + 6  for first ring
        # 1 + 6  + 12  for second ring
        # 1 + 6  + 12  + 18 for third ring
        dis_p, idx_p = kdtree.query(points, k=npoints)

        self.logger.info('Using %d nearest fibers', npoints)
        for diss, idxs, point in zip(dis_p, idx_p, points):
            # For each point
            value = [p * scale for p in point]
            value_mm = [(v / platescale) for v in value]
            self.logger.info('For point %s arcsec', value)
            self.logger.info('For point %s mm', value_mm)
            colids = []
            coords = []
            for dis, idx in zip(diss, idxs):
                fiber = fibers[idx]
                colids.append(fiber.fibid - 1)
                coords.append((fiber.x, fiber.y))
            self.logger.debug('nearest fibers')
            self.logger.debug('%s', [col + 1 for col in colids])
            coords = np.asarray(coords) * scale
            # flux_per_cell = flux_per_cell_all[colids]
            flux_per_cell = rssdata[colids, cut1:cut2].mean(axis=1)
            flux_per_cell_total = flux_per_cell.sum()
            flux_per_cell_norm = flux_per_cell / flux_per_cell_total
            # centroid
            scf = coords.T * flux_per_cell_norm
            centroid = scf.sum(axis=1)
            self.logger.info('centroid: %s arcsec', list(centroid))
            self.logger.info('centroid: %s mm', list(centroid / platescale))
            # central coords
            c_coords = coords - centroid
            scf0 = scf - centroid[:, np.newaxis] * flux_per_cell_norm
            mc2 = np.dot(scf0, c_coords)
            self.logger.info('2nd order moments, x2=%f, y2=%f, xy=%f arcsec^2', mc2[0,0], mc2[1,1], mc2[0,1])
            self.logger.info('FWHM , x=%f, y=%f arcsec',
                             FWHM_G * math.sqrt(mc2[0,0]),
                             FWHM_G * math.sqrt(mc2[1,1])
                             )

        if False:
            self.compute_dar(final)

        return self.create_result(
            reduced_image=reduced2d,
            reduced_rss=reduced1d,
            final_rss=final,
            offset=-centroid
        )
