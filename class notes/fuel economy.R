# R
library(ggplot2)
library(dplyr)

data(mpg)
datacars <- mpg

# Task 1
p1  <- ggplot(datacars, aes(x = displ, y = hwy)) +
  geom_point(alpha = 0.6)
p1b <- ggplot(datacars, aes(x = displ, y = hwy, color = class)) +
  geom_point(size = 2, alpha = 0.7)

# Task 2
p2a <- ggplot(datacars, aes(x = class)) +
  geom_bar() +
  labs(y = "count")
p2b <- ggplot(datacars, aes(x = class, fill = drv)) +
  geom_bar() +
  labs(y = "count", fill = "drive")

# Task 3
p3a <- ggplot(datacars, aes(x = hwy)) +
  geom_histogram(binwidth = 2, fill = "steelblue", color = "white", alpha = 0.85) +
  labs(x = "Highway MPG")
p3b <- ggplot(datacars, aes(x = hwy, fill = drv)) +
  geom_histogram(binwidth = 2, alpha = 0.6, position = "identity") +
  facet_wrap(~ drv) +
  labs(x = "Highway MPG", fill = "drive")

# Task 4
p4a <- ggplot(datacars, aes(x = class, y = hwy)) +
  geom_boxplot()
p4b <- ggplot(datacars, aes(x = class, y = hwy, fill = class)) +
  geom_boxplot() +
  theme(legend.position = "none")

# Task 5
p5 <- ggplot(datacars, aes(x = displ, y = cty)) +
  geom_point(alpha = 0.6) +
  facet_wrap(~ drv) +
  labs(x = "Displacement (L)", y = "City MPG")

# Task 6 — use Task 1-B with labels and a clean theme
p6 <- p1b +
  labs(
    title = "Engine displacement vs. Highway MPG",
    x = "Engine displacement (liters)",
    y = "Highway MPG",
    color = "Vehicle class"
  ) +
  theme_minimal()

# return list of plots
plots <- list(
  task1_a = p1, task1_b = p1b,
  task2_a = p2a, task2_b = p2b,
  task3_a = p3a, task3_b = p3b,
  task4_a = p4a, task4_b = p4b,
  task5   = p5, task6 = p6
)
plots