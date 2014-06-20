from optparse import OptionParser
import pandas as pd
import AnnotationLib as al
import cPickle as pickle

class TrackerEvaluator(object):

    def evaluate(self, trackers, benchmarks, subsamples):
        names = [tracker.name for tracker in trackers]
        results = {}

        for benchmark in benchmarks:
            results[benchmark.name] = pd.DataFrame(index=subsamples,
                                                   columns=names)
            for tracker in trackers:
                ct = CarTracker(tracker)
                performances = []
                for ss in subsamples:
                    al_tracked = ct.run(benchmark.subsample(ss))
                    performance = benchmark.performance(al_tracked)
                    performances.append(performance)
            
            results[benchmark.name][tracker.name] = performances

        return results
                    
                    
class Benchmark(object):
    def __init__(self, al_file):
        self.anns = al.parse(al_file)

    def subsample(self, ss):
        return self.anns[::ss]

    def performance(self):
        pass


def main():
    opts = parse_args()
    te = TrackerEvaluator()
    
    # get the benchmark
    performance = te.evaluate(tracker, benchmark)
    print perforamnce
    
    results = np.load('results.pkl')
    results[benchmark][tracker] = performance
    with open('results.pkl','w') as fh:
        pickle.dump(results, fh, -1)
    

def parse_args():
    parser = OptionParser()
    parser.add_option('')
    

if __name__=='__main__':
    main()
    
    
