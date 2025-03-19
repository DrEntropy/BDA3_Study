# %% [markdown]
#  ## Recommended exercises:
# 
#   3.2, 3.3, 3.9 (model solutions availablefor these)
# 
# 
# 
#  Also look at [Course Exercises](https://avehtari.github.io/BDA_course_Aalto/assignments/assignment3.html)
# 
#  My plan is to look at #2 from the course, and #3.3 from the book. One is multinomial, the other is a normal distribution.

# %% [markdown]
# ### Exercise #2 (from course)
# 
# Basic set up is a an exeriment to estimate the effect of beta-blockers on mortality (in cardiac patients).  This was a random assigment exeriment:
# - 674 patients received the control, 39 died
# - 680 received the treatment, 22 died. 
# 
# Assume outcomes are independante and binomial, with probability of death $p_0$ for the control group, and $p_1$ for the treatment group.  

# %% [markdown]
# **2.1:**   $y_C$ is the number of deaths in the control group, $y_T$ is the number of deaths in the treatment group.   The data model can be written as:
# $$
# y_C \sim \text{Binomial}(n_C, p_0) \\
# y_T \sim \text{Binomial}(n_T, p_1)
# $$
# 
# where $n_C = 674$ and $n_T=680$ are the number of patients in the control and treatment groups, respectively.
# 
# **2.2**  I chose a weakly informative prior each probabilty, given the prior knowledge the the probability of death is more likely to be small:
#  
# $$
# p_0 \sim \text{Beta}(1, 2) \\
# p_1 \sim \text{Beta}(1, 2)
# $$

# %%
import numpy as np
from scipy.stats import beta, binom, beta
import matplotlib.pyplot as plt

plt.plot(np.linspace(0, 1, 100), beta.pdf(np.linspace(0, 1, 100), 1, 2))

# %% [markdown]
# 2.3  The resulting posterior (using my prior rather then the one used in the course) is:
# $$
# p_0 | y_C \sim \text{Beta}(40, 637) \\
# p_1 | y_T \sim \text{Beta}(23, 660)
# $$
# 
# We want to estimate teh Odds Ratio (OR) of death in the treatment group compared to the control group.  The OR is defined as:
# $$
# OR = \frac{p_1/(1-p_1)}{p_0/(1-p_0)}
# $$
# 
# We can compute the posterior by sampling from the posterior distributions of $p_0$ and $p_1$, and then computing the OR for each sample.   

# %%
p0_draws = beta.rvs(40, 637, size=10000)
p1_draws = beta.rvs(23, 660, size=10000)
OR = p1_draws /(1 - p1_draws) / (p0_draws / (1 - p0_draws))
plt.hist(OR, bins=30);
 

# %% [markdown]
# 2.4 Point estimate for $E(OR| y_0,y_1)$ is:

# %%
np.mean(OR)

# %% [markdown]
# **2.5** 95% central credible interval for $OR$ is:

# %%
np.percentile(OR, 2.5), np.percentile(OR, 97.5)

# %% [markdown]
# **2.6**  Consider using ohter priors instead.

# %%
def compute_odds(alphac, betac):
    nc = 674
    nt = 680
    yc = 39
    yt = 22
    p0_draws = beta.rvs(yc + alphac,nc- yc + betac, size=10000)
    p1_draws = beta.rvs(yt + alphac, nt-yt + betac, size=10000)
    OR = p1_draws /(1 - p1_draws) / (p0_draws / (1 - p0_draws))
    print(f"Mean OR for Beta 2,2 prior: {np.mean(OR)}, with 95% percental {np.percentile(OR, 2.5), np.percentile(OR, 97.5)}")
    print(f" Fraction below 1: {np.mean(OR < 1)}")
    print(f" Fraction below 0.5: {np.mean(OR < .5)}")

# %%
compute_odds(1,2)

# %%
compute_odds(2,2)

# %%
compute_odds(1,1)

# %% [markdown]
# No strong effect from these weak priors.

# %% [markdown]
# **2.7**  Use [Frank Harrells recommendations](https://hbiostat.org/blog/post/bayes-freq-stmts/) to report these results.   
# 
# Under a weakly informative prior, the probabilty that the treatment improves mortality compared to the control is 0.985. The probability the the treatment improves mortality odds ratio compared to control by a factor of two is about 0.35 

# %% [markdown]
# 

# %% [markdown]
# 

# %%



