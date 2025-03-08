# %% [markdown]
#  ## Chapter 2. Single variable models
# 

# %% [markdown]
# ## 2.1
# 
# Posterior inference: suppose you have a Beta(4, 4) prior distribution on the probability θ
# that a coin will yield a ‘head’ when spun in a specified manner. The coin is independently
# spun ten times, and ‘heads’ appear fewer than 3 times. You are not told how many heads
# were seen, only that the number is less than 3. Calculate your exact posterior density
# (up to a proportionality constant) for θ and sketch it.
# 
# ## My Answer
# 
# The likelihood of observing fewer then 3 heads in 10 spins is given by summing the binomial distribution for all the possibilities:
# 
# $$
# L(\theta) = \sum_{k=0}^{2} \binom{10}{k} \theta^k (1-\theta)^{10-k}
# $$
# 
# We combine this with the Beta(4,4) prior to get the posterior:
# 
# $$
# \begin{align}
# p(\theta | data) &\propto L(\theta) \cdot p(\theta) \\
# &\propto \sum_{k=0}^{2} \binom{10}{k} \theta^k (1-\theta)^{10-k} \cdot \theta^{3} (1-\theta)^{3} \\
# 
# \end{align}
# $$
# 

# %%
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import binom

def post(theta):
    heads = [0, 1, 2]
    terms = [binom(10, h) * theta**(h+3) * (1 - theta)**(10 - h +3) for h in heads]
    return sum(terms  )

theta = np.linspace(0, 1, 100)
plt.plot(theta, post(theta))

# %% [markdown]
# ## 2.8 
# 
# Normal distribution with unknown mean: a random sample of n students is drawn
# from a large population, and their weights are measured. The average weight of the n
# sampled students is $\bar{y}$ = 150 pounds. Assume the weights in the population are normally
# distributed with unknown mean θ and known standard deviation 20 pounds. Suppose
# your prior distribution for θ is normal with mean 180 and standard deviation 40.
# 
# (a) Give your posterior distribution for θ. (Your answer will be a function of n.)
# 
# (b) A new student is sampled at random from the same population and has a weight of
# $\tilde{y}$ pounds. Give a posterior predictive distribution for $\tilde{y}$. (Your answer will still be a
# function of n.)
# 
# (c) For n = 10, give a 95% posterior interval for θ and a 95% posterior predictive interval
# for $\tilde{y}$.
# 
# (d) Do the same for n = 100.
# 
# ## My Answer
# 
# (a) The posterior distribution for θ will be normal with mean and variance given by:
# 
# $$
# \begin{align}
# \mu_{post} &= \frac{\frac{180}{40^2} + \frac{n \cdot 150}{20^2}}{\frac{1}{40^2} + \frac{n}{20^2}} \\
# \frac{1}{\sigma_{post}^2} &=  \frac{1}{40^2} + \frac{n}{20^2}
# \end{align}
# $$
# 
# (b) For a new student sampled, the posterior predictive distribution for $\tilde{y}$ will be normal with posterior mean and variance enlarged by the aleatoric uncertainty of the new observation:
# 
# $$
# \begin{align}
# \mu_{pred} &= \mu_{post} \\
# \sigma_{pred}^2 &= \sigma_{post}^2 + 20^2
# \end{align}
# $$
# 
# (c) and (d). 
# 
# Lets craft a little function to give these answers

# %%
from scipy.stats import norm

def classroom_post(n):
    var_post = 1.0/(1.0/40**2 + n / 20.0**2)
    mu_post = var_post * (180/40**2 + n / 20.0**2 * 150)
    print(f"posterior mean: {mu_post}, posteriors std: {np.sqrt(var_post)}")
    var_pred = var_post + 20**2
    print(f"posterior predictive std: {np.sqrt(var_pred)}")
    topp=norm.ppf(0.95, loc=mu_post, scale=np.sqrt(var_pred))
    botp = norm.ppf(0.05, loc=mu_post, scale=np.sqrt(var_pred))
    print(f"95% posterior predictive interval: [{botp}, {topp}]")

classroom_post(10)




# %%
classroom_post(100)

# %%
classroom_post(0)


