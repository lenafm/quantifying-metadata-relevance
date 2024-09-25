import argparse
import os

from metablox import calculate_metadata_relevance
from utils import generate_network, add_metadata, write_json


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--outdir', type=str,
                        help='Output directory to save gamma values and graphs.',
                        default='data/synthetic')

    args = parser.parse_args()
    outdir = args.outdir

    N = 400
    B = 2
    mean_degree = 10
    iters = 50

    mus = [0.1, 0.2, 0.3]
    variants = ['ndc', 'dc', 'pp']
    rhos = {'metadata0': 0.7, 'metadata1': 0.8, 'metadata2': 0.9}
    metadata_labels = list(rhos.keys())

    dir_gammas = os.path.join(outdir, 'gammas_mu')
    dir_graphs = os.path.join(outdir, 'graphs_mu')

    if not os.path.exists(dir_gammas):
        os.makedirs(dir_gammas)

    # uncomment the next line if you want to save the graphs
    # if not os.path.exists(dir_graphs):
    #     os.makedirs(dir_graphs)

    for mu in mus:
        print(mu)
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
            # g.save(os.path.join(dir_graphs, f'graph_{mu}_{i}.graphml'), fmt='graphml')
            write_json(gamma, os.path.join(dir_gammas, f'gamma_{mu}_{i}.json'))




