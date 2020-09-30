from trueskill import TrueSkill,Rating, quality_1vs1,rate_1vs1
import itertools
import math
# from trueskill.mathematics import cdf

env = TrueSkill(mu=25.0, sigma=8.333333333333334, beta=4.167, tau=0.08333333333333334, draw_probability=0.0, backend=None)
env.make_as_global()
def win_probability(team1, team2):
    delta_mu = team1.mu - team2.mu
    sum_sigma = (team1.sigma **2) + (team2.sigma **2)
    size = 2
    # denom = math.sqrt(size * (0.05 * 0.05) + sum_sigma)
    denom = math.sqrt(sum_sigma)
    # ts = TrueSkill()
    return TrueSkill().cdf(delta_mu / denom)



# trueskill.setup(mu=25.0, sigma=8.333333333333334, beta=0.05, tau=0.08333333333333334, draw_probability=0.1, backend=None, env=None)
# print (env)
r1 = env.create_rating(mu=25.000, sigma=8.333)  # 1P's skill
r2 = env.create_rating(mu=42.00, sigma=8.333)  # 2P's skill
# r2.create_rating(mu=30, sigma=0.100, beta= 0.05)

print("Win Probability=",win_probability(r2,r1))
print ("Student:",r1)
print ("Ques:",r2)
x = env.quality_1vs1(r1, r2)
print('{:.1%} chance to draw'.format(x))
r1, r2 = env.rate_1vs1(r2, r1)
print ("Student:",r1)
print ("Ques:",r2)
