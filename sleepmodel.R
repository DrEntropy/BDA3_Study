data(sleepstudy, package = "lme4")
library(brms)

# Note this is essentially assignment 6 in week 7, or parts of it

## Random intercepts model

( priorsRI <- c(
  prior(
    normal(250, 100),
    class = "b",
    coef = "Intercept"
  ),
  prior(
    normal(0, 20),
    class = "b",
    coef = "Days"
  ),
  prior(
    normal(0,100),
    class = sd,
    group = "Subject",
    coef = "Intercept"

  ),
  prior(
    normal(0, 100),
    class = "sigma"
  )


))

fit <- brms::brm(bf(Reaction ~ Days +  (1 | Subject),family = "gaussian", center=FALSE),
                 prior = priorsRI, data = sleepstudy)

# we note that this gives for population level effect of days on reaction as 10.45 +- 0.79

## Random slopes version

( priorsRS <- c(
  prior(
    normal(250, 100),
    class = "b",
    coef = "Intercept"
  ),
  prior(
    normal(0, 20),
    class = "b",
    coef = "Days"
  ),
  prior(
    normal(0,100),
    class = sd,
    group = "Subject",
    coef = "Intercept"

  ),
  prior(
      normal(0,20),
      class = 'sd',
      coef = 'Days',
      group = 'Subject'
  ),
  prior(
    normal(0, 100),
    class = "sigma"
  ),
  prior(
    lkj(2),
    class = "cor"
  )


))

modelf <- bf(Reaction ~ Days +  ( 1 + Days | Subject),family = "gaussian", center=FALSE)

fit2 <- brms::brm(modelf,
                  prior = priorsRS,
                   data = sleepstudy)

# For random slopes version , the estimated slope on Days was 10.42 +-1.72 .
# Subject specific effect sd on days was 6.6


