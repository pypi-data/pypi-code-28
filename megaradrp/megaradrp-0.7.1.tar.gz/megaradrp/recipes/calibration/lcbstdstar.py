#
# Copyright 2011-2018 Universidad Complutense de Madrid
#
# This file is part of Megara DRP
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

"""LCB Standard Star Image Recipe for Megara"""


from scipy.interpolate import interp1d
import astropy.io.fits as fits
import astropy.units as u
from astropy import constants as const

from numina.core import Product, Parameter
from numina.core.requirements import Requirement
from numina.core.validator import range_validator
from numina.types.array import ArrayType

from megaradrp.processing.extractobj import extract_star, generate_sensitivity
from megaradrp.recipes.scientific.base import ImageRecipe
from megaradrp.types import ProcessedRSS, ProcessedFrame, ProcessedSpectrum
from megaradrp.types import ReferenceSpectrumTable, ReferenceExtinctionTable
from megaradrp.types import MasterSensitivity


class LCBStandardRecipe(ImageRecipe):
    """Process LCB Standard Star Recipe.

    This recipe processes a set of images
    obtained in **LCB Stardard Star image** mode and returns
    the total flux of the star.

    See Also
    --------
    megaradrp.recipes.calibration.mosstdstar.MOSStandardRecipe

    Notes
    -----
    Images provided by `obresult` are trimmed and corrected
    from overscan, bad pixel mask (if `master_bpm` is not None),
    bias, dark current (if `master_dark` is not None) and
    slit-flat (if `master_slitflat` is not None).

    Images thus corrected are then stacked using the median.
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

    The flux of the star is computed by adding summing the fibers in `nrings` around
    the central spaxel containing the star and returned as `star_spectrum`.

    """
    position = Requirement(list, "Position of the reference object", default=(0, 0))
    nrings = Parameter(3, "Number of rings to extract the star",
                       validator=range_validator(minval=1))
    reference_spectrum = Requirement(ReferenceSpectrumTable, "Spectrum of reference star")
    reference_spectrum_velocity = Parameter(0.0, 'Radial velocity (km/s) of reference spectrum')
    reference_extinction = Requirement(ReferenceExtinctionTable, "Reference extinction")
    sigma_resolution = Parameter(20.0, 'sigma Gaussian filter to degrade resolution ')

    reduced_image = Product(ProcessedFrame)
    final_rss = Product(ProcessedRSS)
    reduced_rss = Product(ProcessedRSS)
    sky_rss = Product(ProcessedRSS)
    star_spectrum = Product(ProcessedSpectrum)
    master_sensitivity = Product(MasterSensitivity)
    fiber_ids = Product(ArrayType)

    def run(self, rinput):

        self.logger.info('starting LCBStandardRecipe reduction')

        reduced2d, rss_data = super(LCBStandardRecipe, self).base_run(rinput)

        self.logger.info('start sky subtraction')
        final, origin, sky = self.run_sky_subtraction(rss_data)
        self.logger.info('end sky subtraction')

        # 1 + 6  for first ring
        # 1 + 6  + 12  for second ring
        # 1 + 6  + 12  + 18 for third ring
        # 1 + 6 * Sum_i=0^n =  1 + 3 * n * (n +1)
        # Using three rings around central point
        self.logger.debug('adding %d nrings', rinput.nrings)
        npoints = 1 + 3 * rinput.nrings * (rinput.nrings +1)
        self.logger.debug('adding %d fibers', npoints)

        fiberconf = self.datamodel.get_fiberconf(final)
        spectra_pack = extract_star(final, rinput.position, npoints,
                                    fiberconf, logger=self.logger)

        spectrum, colids, wl_cover1, wl_cover2 = spectra_pack
        star_spectrum = fits.PrimaryHDU(spectrum, header=final[0].header)

        rad_vel = rinput.reference_spectrum_velocity * u.km / u.s
        factor = 1 + rad_vel / const.c
        star_interp = interp1d(rinput.reference_spectrum[:,0] / factor,
                               rinput.reference_spectrum[:,1])

        extinc_interp = interp1d(rinput.reference_extinction[:, 0],
                               rinput.reference_extinction[:, 1])

        fiber_ids = [colid + 1 for colid in colids]
        sigma = rinput.sigma_resolution
        sens = generate_sensitivity(final, spectrum, star_interp, extinc_interp, wl_cover1, wl_cover2, sigma)
        self.logger.info('end LCBStandardRecipe reduction')

        return self.create_result(
            reduced_image=reduced2d,
            final_rss=final,
            reduced_rss=origin,
            sky_rss=sky,
            star_spectrum=star_spectrum,
            master_sensitivity=sens,
            fiber_ids=fiber_ids
        )
