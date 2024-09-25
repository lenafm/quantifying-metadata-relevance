# Quantifying metadata relevance

This repository can be used to generate the results in

[Mangold, Lena and Camille Roth. “Quantifying metadata-structure relationships in networks using 
description length.” (2023) arXiv:2311.18705 [cs.SI]](https://arxiv.org/abs/2311.18705).

It contains the `metablox` (metadata block structure exploration) Python library and the python and notebook files 
to reproduce the figures in the paper. This README contains an explanation on how to reproduce the results in the paper. 
The methods from the `metablox` library can be used directly from the `.py` modules. Alternatively, you 
can install the library (see the [`metablox` repository](https://github.com/lenafm/metablox) for instructions for the 
installation and for examples).

## Reproduce results

To reproduce the results from the paper, you need to run the calculations as explained below. After that, 
you can create the figures in the jupyter notebooks, as explained at the bottom of this page.

### Run experiments

To create the plots in the paper, the metablox values must first be computed for both the synthetic and the real
networks. After that, the figures can be produced in the Jupyter notebooks.

#### Motivational network

To run the experiments on the motivational network in the paper and to generate Figure 3, run

``` 
python run_synthetic_motivational.py
```


#### Synthetic networks

To run the experiments for the synthetic networks on varying the block structure signal strength $`\mu`$, and generate
Figure 6, run:

``` 
python run_synthetic_mu.py
```

To run the experiments for the synthetic networks on varying the network size $`N`$, and generate Figure 7, run:

``` 
python run_synthetic_N.py
```

To run the experiments for the synthetic networks on varying the number of blocks $`B`$, and generate Figure 8, run:

``` 
python run_synthetic_B.py
```

#### Empirical networks

To calculate the gamma values for the empirical networks for Figures 4 and 5, run the below. In the code, the data for 
the law firm networks[^1] is accessed through the [netzschleuder repository](https://networks.skewed.de/) [^2]. 
The code expects the data for the Twitter/X networks on Impact Investing[^3] (II) and Polarisation[^4] (pol) to be in 
the folders `data/network_data/impinv_data` and `data/network_data/polarisation_data`. The II data can be downloaded
from the [NAKALA repository](https://nakala.fr/10.34847/nkl.dbd8q853#a665ada9528b1f30499f2f2cd109450b65c14067) [^5]. 
For the pol data was originally collected by the authors of ref.[^4]; the networks used in this paper were recollected
by the authors of ref.[^6], who make them publicly available 
[here](https://drive.google.com/drive/folders/1oYM3Je87LBeqA3rmWgSmPOzB4dWKmC_E). The node metadata for the pol networks
need to be estimated using URLs shared by users and a categorisation of these URLs on https://mediabiasfactcheck.com [^7].

``` 
python run_empirical.py
```

### Generate figures and tables

The figures can be generated using the `make_figures.ipynb` notebook, after the data was generated.

[^1]: Lazega, Emmanuel. The collegial phenomenon: The social mechanisms of cooperation among peers in a corporate law partnership. Oxford University Press, USA, 2001.

[^2]: Tiago P. Peixoto. (2020). The Netzschleuder network catalogue and repository. Zenodo. https://doi.org/10.5281/zenodo.7839981

[^3]: Chiapello, Eve, and Lisa Knoll. "Social finance and impact investing. Governing welfare in the era of financialization." Historical Social Research/Historische Sozialforschung 45.3 (2020): 7-30.

[^4]: Garimella, Kiran, et al. "Political discourse on social media: Echo chambers, gatekeepers, and the price of bipartisanship." Proceedings of the 2018 world wide web conference. 2018.

[^5]: Roth, Camille (2024) «ERC Socsemics – Dataset description Impact Investing - Global Dataset - retweet graphs 2008-22» [Dataset] NAKALA. https://doi.org/10.34847/nkl.dbd8q853

[^6]: Hohmann, Marilena, Karel Devriendt, and Michele Coscia. "Quantifying ideological polarization on a network using generalized Euclidean distance." Science Advances 9.9 (2023): eabq2044.

[^7]: Cinelli, Matteo, et al. "The echo chamber effect on social media." Proceedings of the National Academy of Sciences 118.9 (2021): e2023301118.
