import requests
import random


epoch_count = 10
population_size = 10
mutation_rate = 0.15
mutation_range = (0.01, 0.15)

#def calc_k_network(k_cpu, k_gpu):
#    # TODO: network coef
#    return (k_cpu + k_gpu) * 1/5


def softmax_sample(sample):
    summ = sum(sample)
    return tuple(v / summ for v in sample)


def generate_init_population():
    res = []
    for _ in range(population_size):
        k_cpu = random.uniform(0.0, 1.0)
        k_gpu = random.uniform(0.0, 1.0)
        #k_network = calc_k_network(k_cpu, k_gpu)
        k_network = random.uniform(0.0, 1.0)
        summ = sum([k_cpu, k_gpu, k_network])
        k_cpu = k_cpu / summ
        k_gpu = k_gpu / summ
        k_network = k_network / summ
        res.append((k_cpu, k_gpu, k_network))

    return res


def breed(sample1, sample2):
    #print(f'breed sample1={sample1} sample2={sample2}')
    #new_sample1 = (sample1[0],
    #               sample2[1],
    #               calc_k_network(sample1[0], sample2[1]))
    #new_sample2 = (sample2[0],
    #               sample1[1],
    #               calc_k_network(sample2[0], sample1[1]))
    new_sample1, new_sample2 = [], []
    for i in range(3):
        if random.uniform(0.0, 1.0) >= 0.5:
            new_sample1.append(sample2[i])
            new_sample2.append(sample1[i])
        else:
            new_sample1.append(sample1[i])
            new_sample2.append(sample2[i])

    res = [softmax_sample(new_sample1), softmax_sample(new_sample2)]
    #print(f'breed res={res}')
    return res


def gen_breed_pairs():
    ret = []
    idxes = list(range(population_size))
    random.shuffle(idxes)
    for i in range(population_size // 2):
        ret.append((idxes[i*2],
                    idxes[i*2+1]))
    return ret


def mutate_sample(sample):
    print('mutate_sample')
    pos = random.randint(0, 2)
    val = sample[pos]
    mut_abs = random.uniform(*mutation_range)
    if random.uniform(0.0, 1.0) >= 0.5:
        val = val + mut_abs
    else:
        val = val - mut_abs
        if val < 0:
            val = 0.0

    new_sample = list(sample)
    new_sample[pos] = val
    summ = float(sum(new_sample))
    new_sample = tuple(v / summ for v in new_sample)

    print(locals())

    return new_sample


def test_sample(sample):
    # TODO
    return random.uniform(0.0, 1.0)
    

population = generate_init_population()

for epoch_idx in range(epoch_count):
    breed_pairs = gen_breed_pairs()
    new_samples = []
    for sample1_idx, sample2_idx in breed_pairs:
        new_samples.extend(breed(population[sample1_idx],
                                 population[sample2_idx]))

    for idx, sample in enumerate(new_samples):
        if random.uniform(0.0, 1.0) < mutation_rate:
            mutated_sample = mutate_sample(sample)
            new_samples[idx] = mutated_sample
 
    #exit()

    new_population = population.copy()
    new_population.extend(new_samples)

    samples_with_scores = []
    for sample in new_population:
        score = test_sample(sample)
        samples_with_scores.append((sample, score))

    new_population = sorted(samples_with_scores, lambda s: s[1], reverse=True)[:population_size]
    new_population = [item[0] for item in new_population]
    population = new_population


print('best sample', population[0])
