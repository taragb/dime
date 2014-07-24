ggplot(data = tabulated_data) +
  #geom_point(aes(y = '', x = meetings_held), colour = "red") +
  geom_point(aes(y = tax_raised, x = taxes_forecast, colour = region)) +
  #facet_grid( commune ~ . ) +
  theme_bw()

