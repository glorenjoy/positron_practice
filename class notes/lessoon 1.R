install.packages("ggplot2")

library(ggplot2)

#Dataset
data(mpg)
datacars <- mpg

ggplot(data = datacars, 
  mapping = aes()) 

#Aes
ggplot(data = datacars, 
  mapping = aes(x = displ, y = hwy)) 

#Geom
ggplot(data = datacars, 
  mapping = aes(x = displ, y = hwy)) +
  geom_point()

#Facet
ggplot(data = datacars, 
  mapping = aes(x = displ, y = hwy, color = class)) +
  geom_point() +
  facet_wrap(~ class)




