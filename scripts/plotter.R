#!/usr/bin/env Rscript

library(ggplot2)
library(scales)
require(grid)

dd <- read.csv('data.csv')

plot.asml <- ggplot(
  dd, aes(x=times, y=rmses, color=method, shape=method)) +
  scale_x_continuous("Time (timestamp)") +
  scale_y_continuous("RMSE") + 
  geom_line(size=0.8) +
  #scale_linetype_manual(values=c("longdash", "dotdash", "dotted", "twodash")) +  
  theme_bw() + 
  theme(legend.justification=c(0,0), legend.position=c(0,0), legend.title=element_blank(),
    legend.text = element_text(size = 30), legend.key.width = unit(1.5, "cm"),
    axis.title.x = element_text(size=20), axis.title.y = element_text(size=20),
    axis.text.x = element_text(size=20), axis.text.y = element_text(size=20))

pdf("asml.pdf", width=9, height=6)
print(plot.asml)
dev.off()


