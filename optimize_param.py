#coding: utf-8

import numpy        as np
import argparse
from PIL            import Image
from ga.readDataset import readDataset
from ga.individual  import Individual
from ga.population  import Population
from ga.select      import Select
from ga.crossover   import Crossover
from ga.mutation    import Mutation
import six
if (six.PY2):
    from ga.ga4py2  import GA
if (six.PY3):
    from ga.ga4py3  import GA
from main           import main
from argments       import get_args

TCH_IMG = "./results/teach.jpg"
RES_IMG = "./results/result.jpg"

def cmp_imgs(imgpath1, imgpath2):
    tch_img = np.asarray(Image.open(imgpath1))
    res_img = np.asarray(Image.open(imgpath2))
    fitness = np.sum(abs(tch_img-res_img))/(tch_img.shape[0]*tch_img.shape[1]*tch_img.shape[2]*255)*100
    return (fitness)

class HoughGA(GA):
    """
    Optimize Hough transform paramater using GA
    """
    def evaluate(self, ind, args):
        # cvtColor
        """
        args.code  = int("".join(["".join(str(gene)) for gene in ind[0:7+1]]), 2)
        args.code  = 6 # DEBUG
        if (args.code>143):
            args.code = args.code-143
        """
        # GaussianBlur
        args.ksize = int("".join(["".join(str(gene)) for gene in ind[8:11+1]]), 2)
        if ((args.ksize%2)==0):
            args.ksize += 1
        args.sigx  = int("".join(["".join(str(gene)) for gene in ind[12:15+1]]), 2)
        # threshold
        args.pthreshold = int("".join(["".join(str(gene)) for gene in ind[16:23+1]]), 2)
        args.maxval     = int("".join(["".join(str(gene)) for gene in ind[24:31+1]]), 2)
        args.ttype      = int("".join(["".join(str(gene)) for gene in ind[32:35+1]]), 2)
        if (args.ttype==5 or args.ttype==13):
            args.ttype = 0
        if (args.ttype==6 or args.ttype==14):
            args.ttype = 1
        if (args.ttype==7 or args.ttype==15):
            args.ttype = 2
        # HoughLinesP
        args.rho       = 1
        args.theta     = np.pi/180
        args.threshold = int("".join(["".join(str(gene)) for gene in ind[36:43+1]]), 2)
        args.threshold = 100 # DEBUG
        args.lines     = int("".join(["".join(str(gene)) for gene in ind[44:51+1]]), 2)
        args.lines     = 1000 # DEBUG
        args.minLineLength = int("".join(["".join(str(gene)) for gene in ind[52:59+1]]), 2)
        args.maxLineGap    = int("".join(["".join(str(gene)) for gene in ind[60:67+1]]), 2)
        # Debug
        args.debug = True

        # execute hough transform
        main(args)
        fitness = cmp_imgs(args.teach_image, RES_IMG)
        """
        try:
            main(args)
            fitness = cmp_imgs(args.teach, RES_IMG)
        except:
            print(args.code)
            fitness = 999999
        """

        return (fitness)
        
    def revolution(self, args):
        # Config
        if   (args.crossmode=="one"):
            cross_func = Crossover.onePoint
        elif (args.crossmode=="two"):
            cross_func = Crossover.twoPoints
        else:
            cross_func = Crossover.randomPoints

        # Prepare dataset
        dataset = readDataset(args.dpath)
        
        # Create individuals & population
        ppl = Population()
        for i in range(args.individuals):
            individual = Individual()
            individual.createGene(dataset, args.gene)
            ppl.addInd(individual)

        # Evolution
        for i in range(args.revolution):
            # Evaluation population in individuals
            ppl.calcFitness(self.evaluate, args)
            if ((i%10)==0):
                ppl.show()

            # Select parents
            if (args.elite):
                parents = Select.Elite(ppl, args.esize, args.mode)
                parents.extend(Select.Tournament(ppl, args.individuals-args.esize, args.tornsize, args.mode))
            else:
                parents = Select.Tournament(ppl, args.individuals, args.tornsize, args.mode)

            # Clossover
            children = cross_func(parents, args.individuals, args.gene, args.crossrate)

            # Mutation
            children = Mutation.mutation(children, args.mutaterate, dataset)
            # Swap children
            ppl.setPpl(children)
            
        # show result
        ppl.calcFitness(self.evaluate, args)
        ppl.show()

if __name__ == "__main__":
    args = get_args()
    print("[argments list]")
    print(args)
    houghga = HoughGA()
    houghga.revolution(args)
