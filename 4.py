import re
import sys

card_score_map = [0]
for line in open(sys.argv[1]).readlines():
    card_match = re.match(r"Card +(?P<card_id>[0-9]+): (?P<winners>[0-9 ]+) \| (?P<my_nums>[0-9 ]+)", line.strip())

    winners_map = {}
    for winner in re.split(r" +", card_match["winners"].strip()):
        winners_map[int(winner)] = 1

    # card_point = None
    # for my_num in re.split(r" +", card_match["my_nums"].strip()):
        # if int(my_num) in winners_map:
            # if card_point is None:
                # card_point = 1
            # else:
                # card_point *= 2

    # total += card_point or 0
    # print(card_match["card_id"], card_point)

    match_count = len(set(re.split(r" +", card_match["winners"].strip())).intersection(set(re.split(r" +", card_match["my_nums"].strip()))))
    card_score_map.append(match_count)

instance_count = [1] * len(card_score_map)
instance_count_total = 0
for i in range(1, len(card_score_map)):
    for j in range(card_score_map[i]):
        instance_count[i+j+1] += instance_count[i]

    instance_count_total += instance_count[i]

print(instance_count_total)
