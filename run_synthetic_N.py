import argparse
import os
import numpy as np

from metablox import calculate_metadata_relevance
from utils import generate_network, add_metadata, write_json


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--outdir', type=str,
                        help='Output directory to save gamma values and graphs.',
                        default='data/synthetic')

    args = parser.parse_args()
    outdir = args.outdir

    B = 2
    mean_degree = 10
    mu = 0.1
    iters = 50

    sizes = np.arange(100, 1100, 100)
    probs = np.arange(0.7, 0.91, 0.1)
    rhos = {f'metadata{i}': round(x, 1) for i, x in enumerate(probs)}
    metadata_labels = list(rhos.keys())

    dir_gammas = os.path.join(outdir, 'gammas_sizes')
    dir_graphs = os.path.join(outdir, 'graphs_sizes')

    if not os.path.exists(dir_gammas):
        os.makedirs(dir_gammas)

    # uncomment the next line if you want to save the graphs
    # if not os.path.exists(dir_graphs):
    #     os.makedirs(dir_graphs)

    for N in sizes:
        print(N)
        for i in range(iters):
            g = generate_network(N, B, mu, mean_degree)
            g, _ = add_metadata(g=g, probs=list(rhos.values()), B=B)
            gamma = calculate_metadata_relevance(g=g, metadata=metadata_labels,
                                                 use_gt=True,
                                                 allow_multigraphs=True,
                                                 variants='all',
                                                 iters_rand=500,
                                                 uniform=True,
                                                 variants_infer='all',
                                                 refine_states=True,
                                                 verbose=True)
            # uncomment the next line if you want to save the graphs
            # g.save(os.path.join(dir_graphs, f'graph_{N}_{i}.graphml'), fmt='graphml')
            write_json(gamma, os.path.join(dir_gammas, f'gamma_{N}_{i}.json'))
