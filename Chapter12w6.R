# Assignment 4  (Sort of)
# I decided to do this one in R for sake of keeping in practice
# I could not install the course r package, but the data is available
# here: https://github.com/avehtari/BDA_course_Aalto/
library(cmdstanr)
library(posterior)
library(ggplot2)
library(bayesplot)
library(dplyr)
library(tidyr)

ggplot2::theme_set(theme_minimal(base_size = 14))
bayesplot::bayesplot_theme_set(theme_minimal(base_size = 14))
data("bioassay") # Load data
data =list(n = bioassay$n, x = bioassay$x, y = bioassay$y, N = nrow(bioassay))


# Compile Model
mod <- cmdstan_model("bioassay.stan")


  # Sampling from the posterior distribution happens here:
fit <- mod$sample(data=data, refresh=0, show_messages=TRUE, seed = 4711, chains = 4, iter_warmup = 1000,
                    iter_sampling = 3000)

# This extracts the draws from the sampling result as a data.frame.
draws_df = fit$draws(format="draws_df")

# This is what you'll need for convergence diagnostics
summarise_draws(draws_df, Rhat=rhat_basic, ESS= ess_mean, ~ess_quantile(.x, probs = 0.05))

# Scatter plot of the draws
mcmc_scatter(draws_df, pars=c("alpha", "beta"))

# Plot the autocorrelation function and compare to last week
mcmc_acf(draws_df, pars = c("alpha","beta"))
