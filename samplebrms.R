
library(brms)
library(tidyverse)


set.seed(33)
N        <- 100
rain_low     <- runif(N, 0, 5)
rain_mid    <- runif(N, 0, 5)# mm/h
β0_low   <- 5;   β1_low   <- -0.5
β0_mid   <- 6;   β1_mid   <- -1.0


# generate y for each elevation
y_low    <- β0_low + β1_low * rain_low + rnorm(N, 0, 1)
y_mid    <- β0_mid + β1_mid * rain_mid + rnorm(N, 0, 1)

df <- tibble(
  rain = c(rain_low, rain_mid),
  elev = factor(rep(c("Low","Mid"), each = N), levels = c("Low","Mid")),
  y    = c(y_low, y_mid)
)

#Center rain
mean_rain <- mean(df$rain)
df <- df %>% mutate(rain_c = rain - mean_rain)

#–– 3. Fit brms ––
fit <- brm(
  formula = y ~ elev * rain_c,
  data    = df,
  family  = gaussian(),
  cores   = 4,
  seed    = 123
)

#Extract posterior draws for the effect difference
post <- as_draws_df(fit )


x_grid <- seq(min(df$rain), max(df$rain), length = 200)


diff_df <- post |>
  mutate(.draw = row_number()) |>
  crossing(x = x_grid) |>
  mutate(diff = b_elevMid + `b_elevMid:rain_c` * (x - mean_rain)) |>
  group_by(x) |>
  summarize(
    diff_mean = mean(diff),
    lower     = quantile(diff, 0.025),
    upper     = quantile(diff, 0.975)
  )

# the true (simulated) difference function
true_df <- tibble(
  x    = x_grid,
  true = (β0_mid - β0_low) + (β1_mid - β1_low) * x
)

# observed differences, use bins :
df_bins <- df |>
  mutate(bin = cut(rain, breaks = 10, labels = FALSE)) |>
  group_by(bin, elev) |>
  summarize(
    rain_bin = mean(rain),
    y_bar    = mean(y),
    .groups  = "drop"
  )

# now compute observed diff at each bin center
obs_df <- df_bins |>
  pivot_wider(names_from = elev, values_from = c(rain_bin, y_bar)) |>
  transmute(
    x   = (rain_bin_Low + rain_bin_Mid)/2,
    obs = y_bar_Mid - y_bar_Low
  )


ggplot() +

  geom_point(data = obs_df, aes(x = x, y = obs), size = 2, color = "black") +
  # 95% credible ribbon
  geom_ribbon(data = diff_df, aes(x = x, ymin = lower, ymax = upper), alpha = 0.2) +
  # posterior mean curve
  geom_line(data = diff_df, aes(x = x, y = diff_mean), size = 1) +
  # true dashed line
  geom_line(data = true_df, aes(x = x, y = true),
            linetype = "dashed", size = 1) +
  labs(
    x     = "Rain (mm/h)",
    y     = "Mid – Low response",
    title = "Predicted difference (Mid vs Low) vs Rainfall"
  ) +
  theme_minimal()

