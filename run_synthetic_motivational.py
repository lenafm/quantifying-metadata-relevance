import argparse
import os
import random
import numpy as np
import graph_tool.all as gt

from metablox import calculate_metadata_relevance
from utils import write_json


def sbm_entropy_gt(g, b, dc):
    state = gt.BlockState(g=g, b=b, deg_corr=dc)
    return state.entropy(dl=False)


def BESTest(g, b, dc, N):
    # BESTest method from
    # Peel, Leto, Daniel B. Larremore, and Aaron Clauset. "The ground truth about metadata and community detection in
    # networks." Science advances 3.5 (2017): e1602548.
    h = np.zeros(N)
    h_partition = sbm_entropy_gt(g,b,dc)
    for n in range(N):
        h[n] = sbm_entropy_gt(g,np.random.permutation(b),dc)
    return sum(h <= h_partition) / N


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--outdir', type=str,
                        help='Output directory to save metablox values and generated graphs.',
                        default='data/motivational')

    args = parser.parse_args()
    outdir = args.outdir

    g = gt.load_graph(os.path.join('data/scbm.graphml'))

    N = g.num_vertices()
    p1 = g.vp.blocklabel_p1.a
    p2 = g.vp.blocklabel_p2.a
    meta_partitions_bc = []
    meta_partitions_cp = []
    probs = np.arange(0, 1.01, 0.01)
    for prob in probs:
        meta_partitions_bc.append(np.array([p1[n] if random.random() < prob
                                            else random.randint(0, 1) for n in range(N)], dtype=np.int32))
        meta_partitions_cp.append(np.array([p2[n] if random.random() < prob
                                            else random.randint(0, 1) for n in range(N)], dtype=np.int32))
    metadata_syn = meta_partitions_bc + meta_partitions_cp
    # metadata labels
    probs_bc = ['bc{}'.format(str(round(p, 2)).replace('.', '')) for p in probs]
    probs_cp = ['cp{}'.format(str(round(p, 2)).replace('.', '')) for p in probs]
    new_metadata_names_syn = probs_bc + probs_cp
    # for plotting colors
    probs_cols = np.concatenate((probs, probs))

    bestest_bc_dc = [BESTest(g=g, b=b, dc=True, N=500) for b in meta_partitions_bc]
    bestest_cp_dc = [BESTest(g=g, b=b, dc=True, N=500) for b in meta_partitions_cp]

    gamma = calculate_metadata_relevance(g=g, metadata=metadata_syn,
                                         use_gt=True,
                                         allow_multigraphs=True,
                                         variants='all',
                                         iters_rand=500,
                                         uniform=True,
                                         variants_infer='all',
                                         refine_states=True,
                                         verbose=True)

    write_json(bestest_bc_dc, os.path.join(outdir, 'bestest_bc_dc_scbm.json'))
    write_json(bestest_cp_dc, os.path.join(outdir, 'bestest_cp_dc_scbm.json'))
    write_json(gamma, os.path.join(outdir, 'gamma_scbm.json'))





