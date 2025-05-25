# %% [markdown]
# 
# 
# # Week 8
# 
# Rough notes.
# 
# * Model checking and comparison
# 
# * Chapter 6 and Chapter 7 from BDA 3.
# 
# * For chapter 6, Vehtari recommends skimming 6.4 and reading instead [Visualization in Bayesian workflow](https://ar5iv.labs.arxiv.org/html/1709.01449)
# 
# * Also recommends reading [Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC](https://arxiv.org/abs/1507.04544) instead of 72 and 7.3 
# 
# 
# * See brms_demo.Rmd for demos of some of this material using BRMS
# 
# 
# * Introduces also [*priorsense* ](https://n-kall.github.io/priorsense/) which is pretty cool, it uses a power-scaling on the prior and likelihood to make an estimate of the sensitivity of the posterior to the prior and the likelihood. In many cases you would expect the posterior to be more sensitive to the likelihood than the prior..   I note that Arviz apparently can also support this in the new version!  Note that this powerlaw scaling is done with importance sampling, not re-running the MCMC sampler, so it is fast.
# 
# [Detecting and Diagnosing prior and likelihood sensitivity with power-scaling](https://link.springer.com/article/10.1007/s11222-023-10366-5)
# 
# * Also introduced and discussed PSIS-LOO, which can be used to estimate expected log predictive density (ELPD) and compare models as well as to calculating things like LOO-PIT and LOO-R2 .  (LOO-R2 was discussed, but not yet LOO-PIT, which is a way to assess the calibration of the model by comparing the posterior predictive distribution to the observed data using probability integral transforms (PITs).)
# 
# 
# For my own notes, this useful book by Osvaldo [Exploratory Analysis of Bayesian Models](https://arviz-devs.github.io/EABM/)

# %% [markdown]
# ## Exercise - 6.1

# %% [markdown]
# Posterior predictive checking:
# 
# (a) On page 120, the data from the SAT coaching experiments were checked against the
# model that assumed identical effects in all eight schools: the expected order statistics
# of the effect sizes were (26, 19, 14, 10, 6, 2, −3, −9), compared to observed data of (28,
# 18, 12, 8, 7, 1, −1, −3). Express this comparison formally as a posterior predictive
# check comparing this model to the data. Does the model fit the aspect of the data
# tested here?
# 
# (b) Explain why, even though the identical-schools model fits under this test, it is still
# unacceptable for some practical purposes.
# 
# 

# %% [markdown]
# Ans:
# 
# a)
# One idea is to simulate 8 draws from normal distribution with mean 8 and standard deviation 13 (which is the model used on pag 120) and sort the draws. Then compare the distribution of the sorted draws to the observed data. If the observed data in any case is outside the some prescribed interval of the simulated data, then we can might have reason to reject the model.    But can we do better? Can we use our draws and see how many are as 'extreme' as the observed set of data?  I think we can. 
#  

# %% [markdown]
# b)  Even though the model fits under this test it is still unacceptable because... 

# %% [markdown]
# 


