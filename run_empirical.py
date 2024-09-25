import argparse
import os
import csv
import graph_tool.all as gt

from metablox import calculate_metadata_relevance
from utils import write_pickle, write_json, extract_lcc, get_law_graph


def create_output(name, metadata, outdir):
    print(name)
    g, metadata = get_network_and_metadata(name=name, metadata=metadata)
    gamma = calculate_metadata_relevance(g=g, metadata=metadata,
                                         use_gt=True,
                                         allow_multigraphs=True,
                                         variants='all',
                                         iters_rand=500,
                                         uniform=False,
                                         variants_infer='all',
                                         refine_states=True,
                                         verbose=True)
    if not os.path.exists(os.path.join(outdir, 'gammas')):
        os.makedirs(os.path.join(outdir, 'gammas'))
    if not os.path.exists(os.path.join(outdir, 'graphs')):
        os.makedirs(os.path.join(outdir, 'graphs'))
    # uncomment the next line if you want to save the graphs
    # g.save(os.path.join(outdir, f'graphs/graph_{name}.graphml'))
    write_json(gamma, os.path.join(outdir, f'gammas/gamma_{name}.json'))


def get_network_and_metadata(name, metadata):
    if 'law_' in name:
        g_law = gt.collection.ns["law_firm"]
        g = get_law_graph(g_law, name)
    elif 'impinv_' in name:
        graph_dir = 'data/network_data/impinv_data'
        filename = f'retweets-impact-investing-{year}.gt'
        g = gt.load_graph(os.path.join(graph_dir, filename))
    elif name in ['abortion', 'guncontrol', 'obama']:
        graph_dir = 'data/network_data/polarization_data'
        g = gt.load_graph_from_csv(os.path.join(graph_dir, f'{name}_edges_anonym.csv'), hashed=False)
        meta = g.new_vp('int')
        file = f'{name}_nodes_anonym.csv'
        with open(file) as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                try:
                    meta[row[0]] = 0 if float(row[1]) < 0 else 1
                except ValueError:
                    pass
        g.vp.meta = meta
        g = extract_lcc(g)
    else:
        g = gt.collection.ns[name]
    return g, metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--outdir', type=str,
                        help='Output directory to save gamma values and graphs.',
                        default='data/empirical')

    args = parser.parse_args()

    # law networks
    law_metadata = ['nodeStatus', 'nodeGender', 'nodeOffice', 'nodePractice', 'nodeLawSchool']
    law_graphs = ['advice', 'friendship', 'cowork']
    for law_graph in law_graphs:
        create_output(name=f'law_{law_graph}', metadata=law_metadata, outdir=args.outdir)

    # polarisation networks
    pol_graphs = ['abortion', 'guncontrol', 'obama']
    for pol_graph in pol_graphs:
        create_output(name=pol_graph, metadata=['meta'], outdir=args.outdir)

    # impact investment networks
    for year in [str(x) for x in range(2009, 2022)]:
        create_output(name=f'impinv_{year}', metadata=['user_country'], outdir=args.outdir)
