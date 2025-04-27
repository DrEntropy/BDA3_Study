data(sleepstudy, package = "lme4")
library(brms)


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
      normal(0,50),
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
