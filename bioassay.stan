
// The input data is a vector 'y' of length 'N'.
data {
  int<lower=0> N;
  array[N] int<lower=0> n; // number of animals
  vector[N] x;             // dose
  array[N] int<lower=0> y; // deaths
}

// The parameters accepted by the model. Our model
// accepts two parameters 'mu' and 'sigma'.
parameters {
  real alpha;
  real beta;
}

transformed parameters {
  vector[N] log_odds = alpha + beta * x;
}

// The model to be estimated. We model the output
// 'y' to be normally distributed with mean 'mu'
// and standard deviation 'sigma'.
model {
  alpha ~ normal(0,2);
  beta ~ normal(10,10);

  y ~ binomial_logit(n,  log_odds);
}

