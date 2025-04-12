# %% [markdown]
#  For week 4 the course jumps to Chapter 10.
# 
#  Recommended book exercises:
# 
#  10.1 and 10.2
# 
#  Also course exercises are [here](https://avehtari.github.io/BDA_course_Aalto/assignments/assignment4.html)
# 
#  My plan:  10.1 only, although it the course assignments have an intersting example with importance sampling.
# 
#  * If the prior is the proposal disribution then the importance weights are just (proportional to) the likelihood:
# 
#  $$ 
#  \begin{align*}
#  w_i &= \frac{p(\theta | y)}{p( \theta_i)} \\
# 
#     &\propto \frac{p(y | \theta_i) p(\theta_i)}{p( \theta_i)}\\
# 
#     &= p(y | \theta_i) \\
#      \end{align*}
#  $$
# 
# * This suggests one could reweight prior samples by the likelihood to get estimates of say the mean or variance of the posterior.   The exercise has one do this using the Bioassay example.  However i thik for the example they find a very small effective sample size, which makes sense because most of the weights will be very small. 
# 
# * THis is a form of ABC called ABC-IS (ABC with importance sampling).   Importance weights are also used with SMC-ABC
# 
# 
# 

# %% [markdown]
# ## 10.1
# Number of simulation draws: Suppose the scalar variable θ is approximately normally
# distributed in a posterior distribution that is summarized by n independent simulation
# draws. How large does n have to be so that the 2.5% and 97.5% quantiles of θ are
# specified to an accuracy of 0.1 sd(θ|y)?
# 
# (A) Figure this out mathematically
# 
# (B) Check your answer using simulation

# %% [markdown]
# (A) Without loss of generality we can assume $\mu = 0$  
# 
# For a normal distribution The quantile is given by this formula:
# $$Q_{0.025} =  - 1.96 \cdot \frac{\sigma}{\sqrt{n}}$$
# 
# so $dQ = 1.96/\sqrt{n} d\sigma$,  and if we want $dQ = 0.1 \cdot \sigma$ we must have $n = 1.96^2 / 0.1^2 = 384.16$

# %% [markdown]
# (B) Check your answer using simulation

# %%
# simulated data, assume sigma =1 , mu = 0
import numpy as np
def sim_data_q(n):
    data = np.random.normal(0, 1, n)
    quartile = np.percentile(data, 25)
    return quartile


sims = [sim_data_q(385) for _ in range(10000)]

np.abs(np.std(sims)/np.mean(sims))

# %% [markdown]
# Done.

# %%



