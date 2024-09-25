import random
import pickle
import json
import numpy as np
import graph_tool.all as gt


def transform_prob(rho, B):
    return (rho*B-1)/(B-1)


def add_metadata(g, B, nprobs=10, probs=None):
    if probs is None:
        probs = np.arange(0, 1.01, 1/nprobs)
    metadata = []
    for i, prob in enumerate(probs):
        rho = transform_prob(prob, B)
        m = 'metadata{}'.format(i)
        metadata.append(m)
        meta_partition = np.array([g.vp.blocklabel[v] if random.random() < rho
                                   else random.randint(0, B - 1) for v in g.vertices()], dtype=np.int32)
        g.vp[m] = g.new_vp("int", vals=meta_partition)
    return g, metadata


def generate_network(N, B, mu, mean_degree, equal_block_sizes=False, micro_ers=False,
                     seed=None):
    M = create_block_count_matrix(mu=mu, N=N, B=B, mean_degree=mean_degree)
    b = create_block_membership_vector(N=N, B=B, equal_block_sizes=equal_block_sizes)
    if seed is not None:
        gt.seed_rng(seed)
    g = gt.generate_sbm(b=b, probs=M, micro_ers=micro_ers)
    g.vp.blocklabel = g.new_vp("int", vals=b)
    g = extract_lcc(g)
    return g


def create_block_membership_vector(N: int, B: int, equal_block_sizes: bool, sizes: np.ndarray = None) -> np.ndarray:
    if equal_block_sizes:
        assert N % B == 0, 'N must be a multiple of B if `equal_block_sizes = True`.'
        if sizes is not None:
            print('Ignoring `sizes` parameter as `equal_block_sizes = True`')
        x = np.repeat(np.arange(B), int(N/B))
        np.random.shuffle(x)
        return x
    else:
        if sizes is None:
            sizes = np.array([1/B] * B)
        else:
            assert np.isclose(np.sum(sizes), 1), 'The elements of `sizes` must sum to 1.'
        return np.random.choice(B, N, p=sizes)


def get_law_graph(g, name):
    if name == 'law_friendship':
        layer = 2
    elif name == 'law_cowork':
        layer = 3
    elif name == 'law_advice':
        layer = 1
    else:
        raise ValueError('Invalid graph type')
    g = gt.GraphView(g, efilt=lambda e: g.ep.layer[e] == layer)
    return extract_lcc(g)


def extract_lcc(g, directed=False, prune=True):
    g = gt.GraphView(g, vfilt=gt.label_largest_component(g, directed=directed))
    return gt.Graph(g, prune=prune)


def create_block_count_matrix(mu, N, B, mean_degree):
    c = 1 - mu
    E = mean_degree * N / 2
    M = np.zeros((B, B))
    for i in range(B):
        for j in range(B):
            if i == j:
                m_ij = c / B
            else:
                m_ij = (1 - c) / (B * (B - 1))
            M[i, j] = 2 * E * m_ij
    return np.around(M,0).astype(int)


def load_pickle(filename):
    with open(filename, 'rb') as f:
        pickledfile = pickle.load(f)
    return pickledfile


def write_pickle(file, filename):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)


def load_json(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data


def write_json(file, filename):
    with open(filename, 'w') as fp:
        json.dump(file, fp)
