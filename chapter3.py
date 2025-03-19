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
# ## Exercise #3.3 (from book)
# 
# Estimation from two independent experiments: an experiment was performed on the
# effects of magnetic fields on the flow of calcium out of chicken brains. Two groups
# of chickens were involved: a control group of 32 chickens and an exposed group of 36
# chickens. One measurement was taken on each chicken, and the purpose of the experiment
# was to measure the average flow $\mu_c$ in untreated (control) chickens and the average flow
# $\mu_t$ in treated chickens. The 32 measurements on the control group had a sample mean of
# 1.013 and a sample standard deviation of 0.24. The 36 measurements on the treatment
# group had a sample mean of 1.173 and a sample standard deviation of 0.20.
# 
# 
# a) Assume the mesurements were taken at random from a normal distribution for each variable with mean $\mu_c$ and $\mu_t$ and standard deviation $\sigma_c$ and $\sigma_t$.   Assume prior uniform on $\mu_c, \mu_t, \log \sigma_c and \log \sigma_t$.  Compute the marginal posterior distribution of $\mu_c, \mu_t $
# 
# b) What is the posterior difference in means? Plot the histogram compute 95% posterior interval for $\mu_t - \mu_c$

# %% [markdown]
# ### Answer: 
# 
# The book gives the posterior distribution for this case:
# 
# $$
# \frac{\bar{y} - \mu}{s/\sqrt{n}} \sim t_{n-1}
# $$
# 
# where $\bar{y}$ is the sample mean, $s$ is the sample standard deviation, and $n$ is the sample size.   For the instant case we are given the sample means and sample standard deviations, so the posterior distributions are self evident.
# 
# To sample from these we will define a function:
# 

# %%
import numpy as np
from scipy.stats import t
import pandas as pd
import matplotlib.pyplot as plt

# %%
np.std(t.rvs(3, size=10000))

# %%
rng = np.random.default_rng(42)
def sample_post(y_c, y_t, n_c,n_t,sig_c,sig_t,rng, n= 10):
    draws_c = t.rvs(n_c - 1,random_state=rng, size=n)* sig_c / np.sqrt(n_c) + y_c
    draws_t = t.rvs(n_t - 1,random_state=rng, size=n) * sig_t / np.sqrt(n_t) + y_t
    return   draws_c, draws_t 


# %%

samples = sample_post(1.013, 1.173, 32, 36, 0.24, 0.20, rng, n= 10000)

df = pd.DataFrame({"Control": samples[0], "Treatment": samples[1], "Treatment Effect": samples[1] - samples[0]})
df_long = df.melt(value_vars=["Control", "Treatment", "Treatment Effect"], var_name="Group", value_name="Value")
df_long 

# %%
import seaborn as sns
sns.histplot(data=df_long, hue="Group", x="Value", kde=True, bins=30)

# %%
np.percentile(df["Treatment Effect"], [2.5, 97.5])

# %%
np.mean(df["Treatment Effect"] < 0)

# %% [markdown]
# There is > 99% probability that the treatment effect is positive, and the 95% posterior credible interval is from 0.05 to 0.27.

# %% [markdown]
# 


