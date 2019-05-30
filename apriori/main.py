from collections import defaultdict
import operator

# 模型参数，如果购买次数不到1000的，不纳入频繁项集
THRESHOLD_RAITO = 0.01

item_counts = defaultdict(int)
pair_counts = defaultdict(int)
triple_counts = defaultdict(int)

# 数据集中一共十万行
dataset_path = './dataset_100000_baskets_5000_objects.txt'
# dataset_path = './baskets.txt'
# dataset_path = './other_baskets.txt'

with open(dataset_path) as f:
    lines = f.readlines()

THRESHOLD = len(lines) * THRESHOLD_RAITO


def normalize_group(*args):
    return str(sorted(args))


def generate_pairs(*args):
    pairs = []
    for idx_1 in range(len(args) - 1):
        for idx_2 in range(idx_1 + 1, len(args)):
            pairs.append(normalize_group(args[idx_1], args[idx_2]))
    return pairs


# frist pass ------------------
for line in lines:
    for item in line.split():
        item_counts[item] += 1

frequent_items = set()
for key in item_counts:
    if item_counts[key] > THRESHOLD:
        frequent_items.add(key)

print('There are {} unique items, {} of which are frequent'.format(
    len(item_counts), len(frequent_items)))

# second pass
for line in lines:
    items = line.split()
    for idx_1 in range(len(items) - 1):
        # 如果商品不在频繁项中，直接跳过
        if items[idx_1] not in frequent_items:
            continue
        for idx_2 in range(idx_1, len(items)):
            if items[idx_2] not in frequent_items:
                continue
            pair = normalize_group(items[idx_1], items[idx_2])
            pair_counts[pair] += 1

frequent_pairs = set()
for key in pair_counts:
    if pair_counts[key] > THRESHOLD:
        frequent_pairs.add(key)

print('There are {0} candidate pairs, {1} of which are frequent'.format(
    len(pair_counts), len(frequent_pairs)))


# third pass - find candidate triples
# when building candidate triples, only consider frequent items and pairs
for line in lines:
    items = line.split()
    for idx_1 in range(len(items) - 2):
        if items[idx_1] not in frequent_items:  # first item must be frequent
            continue
        for idx_2 in range(idx_1 + 1, len(items) - 1):
            first_pair = normalize_group(items[idx_1], items[idx_2])
            # second item AND first pair must be frequent
            if items[idx_2] not in frequent_items or first_pair not in frequent_pairs:
                continue
            for idx_3 in range(idx_2 + 1, len(items)):
                if items[idx_3] not in frequent_items:
                    continue
                # now check that all pairs are frequent, since this is a precondition to being a frequent triple
                pairs = generate_pairs(
                    items[idx_1], items[idx_2], items[idx_3])
                if any(pair not in frequent_pairs for pair in pairs):
                    continue
                triple = normalize_group(
                    items[idx_1], items[idx_2], items[idx_3])
                triple_counts[triple] += 1

num_candidate_triples = len(triple_counts)  # before filtering
# filter for frequent triples
triple_counts = {k: v for k, v in triple_counts.items() if v > THRESHOLD}
print('There are {0} candidate triples, {1} of which are frequent'.format(
    num_candidate_triples, len(triple_counts)))

# VIEW OUR RESULTS -------------------------------------
print('--------------')
sorted_triples = sorted(triple_counts.items(), key=operator.itemgetter(1))

for entry in sorted_triples:
    print('{0}: {1}'.format(entry[0], entry[1]))
