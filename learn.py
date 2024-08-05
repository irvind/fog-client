import requests
import random


epoch_count = 10
population_size = 10


def calc_k_network(k_cpu, k_gpu):
    # TODO: network coef
    return (k_cpu + k_gpu) * 1


def generate_init_population():
    res = []
    for _ in range(population_size):
        k_cpu = random.uniform(0.0, 1.0)
        k_gpu = 1 - k_cpu
        k_network = calc_k_network(k_cpu, k_gpu)
        res.append((k_cpu, k_gpu, k_network))

    return res


def breed(sample1, sample2):
    new_sample1 = (sample1[0],
                   sample2[1],
                   calc_k_network(sample1[0], sample2[1]))
    new_sample2 = (sample2[0],
                   sample1[1],
                   calc_k_network(sample2[0], sample1[1]))
    return new_sample1, new_sample2


def gen_breed_pairs():
    # TODO: mutation
    ret = []
    idxes = list(range(population_size))
    random.shuffle(idxes)
    for i in range(population_size // 2):
        ret.append((idx[i*2],
                    idx[i*2+1]))
    return ret


def test_sample(sample):
    # TODO
    return 0
    

population = generate_init_population()

for epoch_idx in range(epoch_count):
    breed_pairs = gen_breed_pairs()
    new_samples = []
    for sample1_idx, sample2_idx in breed_pairs:
        new_samples.extend(*breed(population[sample1_idx,
                                  population[sample2_idx]]))
    
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
