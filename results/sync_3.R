d <- read.csv('results.txt')

# linear
# fit <- lm(Score ~ Year, data=d)

# polynomial
fit <- lm(Score ~ Year + poly(Year, degree=2), data=d)

out <- data.frame(Year=seq(min(d$Year), max(d$Year), len=100))
out$Score = predict(fit, newdata=out, type="response")

plot(Score~Year, data=d, col="red4")
lines(Score~Year, data=out, col="green4", lwd=2)
