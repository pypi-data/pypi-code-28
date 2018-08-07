import unittest
import numpy as np
from phonopy.qha.electron import ElectronFreeEnergy, get_free_energy_at_T

eigvals_Al = """ -3.1277  20.6836  20.6836  20.6836  22.1491  22.1491  22.1491  24.4979  27.5181  27.5181  30.3260  32.6840
 -2.9388  18.0492  20.1052  20.1052  22.8186  23.0196  23.0196  26.3365  26.5334  26.5334  29.6719  33.6291
 -2.3735  14.6746  19.3975  19.3975  22.6320  24.0932  24.0932  25.3438  25.3438  28.3204  29.5706  36.0714
 -1.4364  11.4634  18.9510  18.9510  22.3995  22.8160  22.8160  26.8047  26.9530  26.9530  32.6888  39.6579
 -0.1346   8.5159  18.8099  18.8099  21.4127  21.4127  22.3759  25.3790  29.2176  29.2176  35.6322  42.6390
  1.5221   5.8657  18.9847  18.9847  20.2918  20.2918  22.6465  24.1761  31.5666  31.5666  38.3066  40.4901
  3.4186   3.6381  19.4442  19.4442  19.5221  19.5221  23.1558  23.3545  32.9258  32.9258  38.9022  38.9022
 -2.8758  18.9505  18.9505  19.2472  21.5769  24.2562  24.2562  24.8357  26.4379  27.7554  30.6552  32.9737
 -2.4362  15.8850  18.0658  19.3526  21.9439  22.8664  24.6306  25.6366  27.1817  29.1447  30.0695  34.6029
 -1.6233  12.6395  17.4906  19.0119  20.8203  23.7369  24.5307  25.0979  28.0860  28.5913  32.3824  37.6111
 -0.4435   9.6144  17.2336  18.8057  19.2655  23.7046  24.2555  25.9221  27.3519  30.1704  35.4034  40.7533
  1.0942   6.8692  17.2968  17.9784  18.9243  22.5071  24.4342  25.6721  28.8218  32.2635  38.2124  40.1962
  2.9744   4.4380  17.0381  17.6817  19.3430  21.6029  24.5913  25.0359  31.2280  32.9637  39.1395  39.1931
  2.3121   5.2101  16.4244  18.3885  20.0896  21.0092  23.9865  25.7133  31.0912  32.2886  38.2309  40.0713
  0.5427   7.7489  16.1423  19.4079  20.7331  21.1501  23.6107  26.7041  28.5427  30.7951  37.4157  40.3394
 -0.8771  10.5866  16.1970  20.5854  20.9133  22.5016  23.5127  26.1216  27.4579  29.1097  34.5738  39.2435
 -1.9354  13.6715  16.6023  21.0073  22.3283  23.5478  24.1220  24.1358  26.1200  29.7584  31.5637  35.6661
 -2.6244  16.6578  17.6073  21.1782  22.4320  23.4320  24.4533  24.5964  25.9025  28.4526  30.3428  33.3116
 -2.1230  17.0498  17.0499  17.2117  20.3324  20.5199  27.1756  27.1756  28.4495  29.9827  32.3264  33.9139
 -1.4364  14.0702  16.3562  17.6688  18.4931  20.7396  27.4875  27.7483  29.3160  31.3391  32.8856  35.8011
 -0.3818  11.0239  15.9867  16.7172  17.6464  22.5592  26.2470  27.7819  29.9376  31.2676  35.9602  38.8919
  1.0324   8.2083  15.3220  15.9396  17.6733  24.8225  25.0254  27.8554  28.8179  33.0868  38.8945  40.2488
  2.7938   5.6834  14.2496  16.2151  18.0107  24.0438  26.3596  28.3519  28.7038  33.1391  39.4687  39.8233
  3.4546   4.9101  13.5162  16.8135  18.6785  23.3514  26.0635  29.0454  30.4550  30.8867  37.2317  41.9795
  1.5826   7.3154  13.1357  17.7333  19.6719  22.9643  25.6046  28.1638  29.5182  31.1078  37.0549  40.4665
  0.0503   9.9872  13.1483  18.9708  20.9766  22.8626  25.2627  25.6330  28.4632  31.5926  35.8711  40.1853
 -1.1254  12.5101  13.9308  20.5052  22.5348  22.6411  23.8516  24.7422  26.9138  32.1269  33.2147  36.8510
 -0.8772  15.5164  15.5484  15.5484  16.2930  19.0542  29.5612  30.0381  30.0381  34.1852  34.5512  35.7550
  0.0499  12.6854  14.4255  15.0677  16.3290  19.5669  28.9196  30.6637  32.0964  33.6578  36.8771  37.9212
  1.3364   9.8550  12.8859  14.9107  16.4954  21.5901  27.7818  30.3954  32.8147  33.7966  39.8767  40.6293
  2.9701   7.2633  11.6838  15.0766  16.7762  24.1581  26.7639  29.6695  32.6267  33.4293  39.9905  40.8154
  4.8133   5.0847  10.8359  15.5660  17.3558  25.9996  26.7799  28.9706  30.9545  32.6742  37.6272  42.9814
  2.9762   7.1822  10.3939  16.3788  18.2658  25.5158  27.6668  28.0986  29.4689  32.6027  36.6015  40.3587
  1.3386   9.2581  10.7780  17.5157  19.4890  25.0503  25.7043  26.8065  29.2348  33.3919  35.8723  38.9980
  0.8471  12.4050  14.2859  14.4763  14.4764  18.0073  31.0512  32.4353  32.4353  37.0880  38.7236  38.7236
  2.0018  10.7106  11.7903  14.2095  15.3867  18.7232  30.6140  32.7541  34.0716  36.9988  40.9089  41.0450
  3.4977   9.0487   9.5311  14.2659  15.7864  20.9765  29.6757  32.0834  33.8425  36.6240  40.9498  41.6014
  5.2805   6.7761   8.5219  14.6456  16.3071  23.7886  28.8830  31.0008  31.3121  35.7834  39.4960  43.4559
  4.7094   6.9396   8.4165  15.3505  17.1299  26.7616  28.3497  28.3536  29.6164  34.2307  38.9455  40.2089
  3.0171   8.9287  13.5473  13.8336  13.8337  17.3391  32.6592  34.2449  34.2449  39.7783  41.5730  41.5730
  4.3406   7.5139  11.3135  13.7809  14.9121  18.2871  32.4082  34.1511  34.3731  39.8351  41.2857  41.8528
  5.5518   6.8934   8.9633  14.0512  15.5459  20.7675  31.4820  32.2752  32.8940  38.0395  42.0569  43.0097
  5.0903   6.4198  13.2988  13.6195  13.6195  17.1106  33.5260  35.0595  35.0595  40.6400  41.4881  41.4881
 -1.8729  14.5983  15.7752  20.0507  20.6408  21.9012  25.8147  25.8394  27.2214  31.3730  31.4693  34.5407
 -0.9391  11.8364  14.8883  18.8718  20.2343  23.2004  24.4738  26.1256  28.6676  30.8113  34.3788  37.5689
  0.3582   8.9565  14.6749  17.3823  20.2102  22.9433  25.3549  26.4385  29.0862  31.2195  37.2961  40.1885
  2.0082   6.3313  14.8252  16.2177  20.4216  21.8312  26.2124  27.7848  28.7446  32.4783  38.1010  40.4889
  3.8848   4.1277  15.1821  15.5231  20.7975  21.1450  26.4911  27.5154  30.4774  31.7924  38.7916  39.5810
 -0.6292  12.9792  14.2427  16.5505  18.5385  20.6536  26.9617  29.1511  30.3991  32.8989  34.2067  37.3428
  0.5420  10.4434  13.5244  14.9335  18.9938  22.1878  25.6915  29.5785  31.7926  32.4728  36.8529  40.5648
  2.0672   7.7813  13.3491  13.8065  19.2194  24.1499  24.9634  29.6058  31.2837  33.0395  38.6684  40.8047
  3.9268   5.3861  12.5780  13.9932  19.6732  23.4970  27.2392  29.1851  31.0195  31.7357  39.1919  40.2956
  3.2758   6.1349  11.9830  14.7085  20.4249  22.8833  27.7011  28.6745  30.8156  31.5522  37.2563  41.9681
  1.5213   8.5869  11.7767  15.7741  21.4613  22.5212  25.3846  28.2720  30.7702  32.4722  36.7284  39.6965
  0.1119  10.8840  12.3677  17.1689  21.9260  22.6607  23.6917  27.5822  29.4141  33.2039  34.7654  40.4939
  1.0919  11.8165  12.5383  13.2743  17.4048  19.6643  28.4790  32.1041  33.0081  35.2884  37.2198  41.3866
  2.4868   9.4996  11.1896  12.7092  18.1054  21.4132  27.3901  32.0921  33.5785  35.2106  39.6399  40.6491
  4.2143   7.0694  10.1259  12.9167  18.5671  24.0127  26.4590  30.7158  32.5356  35.0403  40.0058  41.4346
  4.8799   6.2477   9.4489  13.5225  19.2527  25.5229  26.9553  28.3747  31.3499  34.7116  38.3165  41.9474
  3.0354   8.0981   9.5993  14.4813  20.2300  24.7073  25.8500  29.7277  30.0591  33.8250  37.5670  39.0913
  3.2574   9.1550  11.1192  12.5153  16.7204  19.0343  30.3287  33.6445  34.2078  38.5007  40.9696  41.0959
  4.8135   7.9633   9.0879  12.2290  17.6533  21.0074  29.4325  31.5949  34.2321  38.4291  41.5998  42.0746
  6.2450   6.7644   7.7368  12.6826  18.3452  23.8436  28.3090  29.1089  33.0561  36.9471  40.9009  41.9419
  5.3209   6.6614  10.8866  12.2842  16.4922  18.8192  32.2083  32.4183  35.1006  40.3870  41.4306  41.6230
  1.8240   9.7233  11.1917  13.4056  20.8674  22.5153  24.4975  31.1765  32.0183  34.4649  36.8893  39.5759
  3.4518   7.6483  10.8039  12.2290  21.6687  23.1221  24.8497  30.3322  32.2200  34.5737  38.4224  40.8270
  5.2762   5.5505  11.0226  11.6097  22.0715  22.5661  27.0183  28.1663  32.4880  34.4399  40.0294  40.8607
  3.9768   9.0269   9.7357  10.7187  20.1990  22.0127  26.3436  31.0282  34.0386  37.6527  40.1521  40.4888
  5.7516   7.1691   8.9266  10.4890  21.2577  24.1281  25.4547  28.2380  34.3710  38.0208  41.3410  42.0288
  5.1648   7.4030   8.8536  11.1407  22.0811  24.0947  25.3453  27.7602  33.6054  37.1388  40.1252  40.8104
  6.0139   7.3687   8.7944  10.3799  19.9725  21.8262  28.1228  29.1805  35.1953  40.0277  42.0199  42.2035
  7.1712   7.1712   8.1868   9.1337  23.8810  23.8810  24.4184  26.4784  35.2568  40.0588  42.6207  42.6207"""


class TestElectronFreeEnergy(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Al(self):
        """

        VASP 5.4.4 was run with following setting parameters.

        POSCAR
        ------
        Fm-3m (225) / -F 4 2 3 (523) / m-3m
           1.0
             0.0000000000000000    2.0196332190180484    2.0196332190180484
             2.0196332190180484    0.0000000000000000    2.0196332190180484
             2.0196332190180484    2.0196332190180484    0.0000000000000000
         Al
           1
        Direct
           0.0000000000000000  0.0000000000000000  0.0000000000000000

        INCAR
        -----
           PREC = Accurate
         IBRION = -1
            NSW = 1
           ISIF = 2
         NELMIN = 5
          ENCUT = 300
          EDIFF = 1.000000e-08
         EDIFFG = -1.000000e-08
         ISMEAR = -1
          SIGMA = 0.08617338256808316
          IALGO = 38
          LREAL = .FALSE.
        ADDGRID = .TRUE.
          LWAVE = .FALSE.
         LCHARG = .FALSE.

        KPOINTS
        -------
        Automatic mesh
        0
        Gamma
        12 12 12
             0     0     0

        POTCAR
        ------
        PAW_PBE Al 04Jan2001

        """

        weights = np.array(
            [1, 8, 8, 8, 8, 8, 4, 6, 24, 24, 24, 24, 24, 24, 24, 24, 24, 12,
             6, 24, 24, 24, 24, 24, 24, 24, 12, 6, 24, 24, 24, 24, 24, 12,
             6, 24, 24, 24, 12, 6, 24, 12, 3, 24, 48, 48, 48, 24, 24, 48,
             48, 48, 48, 48, 24, 24, 48, 48, 48, 24, 24, 48, 24, 12, 24, 48,
             24, 24, 48, 24, 12, 6], dtype='intc')
        eigvals = np.reshape([float(x) for x in eigvals_Al.split()],
                             (1, len(weights), -1))
        n_electrons = 3.0
        efe = ElectronFreeEnergy(eigvals, weights, n_electrons)
        efe.run(1000)
        _efermi = efe.mu  # E-fermi :   7.9104
        _entropy = efe.entropy  # EENTRO = -0.00959209
        _energy = efe.energy  # EBANDS = 10.76680671

        self.assertTrue(np.abs(_efermi - 7.9104) < 1e-4)
        self.assertTrue(np.abs(_entropy - 0.00959209) < 1e-6)
        self.assertTrue(np.abs(_energy - 10.76680671) < 1e-6)

        (temperaturs,
         free_energy) = get_free_energy_at_T(0, 1000, 10,
                                             eigvals, weights, n_electrons)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestElectronFreeEnergy)
    unittest.TextTestRunner(verbosity=2).run(suite)
