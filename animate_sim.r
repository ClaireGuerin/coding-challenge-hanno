rm(list = ls())

#install.packages("tidyverse")
#install.packages("gganimate")
#install.packages("gifski")
library(tidyverse)
library(gganimate)

#library(fs)
#library(patchwork)
#library(rlang)

#==== Import vigilance data ====
#vigilance <- runif(n=100,min=0,max=1)
#time <- seq(1,length(vigilance))
# vigilance_data <- vigilance %>% 
#   as_tibble() %>%
#   rename(vigilance = value) %>%
#   add_column(generations = time)

vigilance <- read_csv("vigilance_out.txt") 
time <- seq(1,nrow(vigilance))

vigilance_data <- vigilance %>% 
  rename(vigilance = `0.5`) %>%
  add_column(generations = time)

#==== Plot Vigilance ====

vPlot <- vigilance_data %>%
  ggplot(aes(generations, vigilance)) +
  geom_line() +
  ylim(0,1) +
  theme_minimal() +
  transition_reveal(generations)

anim_save("vigilance.gif", vPlot)

#==== Import ecosystem data ====
#resources <- read_csv("resources.txt") 
#movement <- read_csv("movement.txt") 

#resources <- tibble(t = )
  
#==== Plot ecosystem