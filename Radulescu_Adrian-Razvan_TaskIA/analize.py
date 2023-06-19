
import numpy as np
import matplotlib.pyplot as plt
# games for one heuristic
games_per_side = 10

total_games = 20

glds_4side = [5, 4, 5, 0]
glds_5side = [0, 1, 0, 0]
glds_6side = [2, 5, 0, 0]


# am ales beam search 50
beam_4side = [5, 5, 5, 5]
beam_5side = [5, 5, 0, 0]
beam_6side = [5, 5, 0, 0]

glds_percentage_4side = (sum(glds_4side) / total_games) * 100
glds_percentage_5side = (sum(glds_5side) / total_games) * 100
glds_percentage_6side = (sum(glds_6side) / total_games) * 100

beam_percentage_4side = (sum(beam_4side) / total_games) * 100
beam_percentage_5side = (sum(beam_5side) / total_games) * 100
beam_percentage_6side = (sum(beam_6side) / total_games) * 100


data4side_beam = {'4-side': 20, '5-side': 10, '6-side': 10}
data4side_glds = {'4-side': 14, '5-side': 1, '6-side': 7}

type_of_game = list(data4side_beam.keys())
values_beam = list(data4side_beam.values())
values_glds = list(data4side_glds.values())

barWidth = 0.25
br1 = np.arange(len(values_beam))
br2 = [x + barWidth for x in br1]


plt.bar(br1, values_beam, color ='green', width = barWidth)
plt.bar(br2, values_glds, color ='red', width = barWidth)

plt.show()
plt.savefig('percentage.png')
