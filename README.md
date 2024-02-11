# equity-cycle

## Task list

- [ ] Finalize our framework and decide detail approach
- [ ] Weekly slides
- [ ] Stock data
  - [ ] Acquire stock data from bloomberg terminal (all NYSE, AMEX, and NASDAQ firms)
  - [ ] Stock data exploratory data analysis (graphs, summaries, covariance matrices, etc)
  - [ ] Construct portfolios (either do it our self or use portfolios contructed by others, e.g. French's data library)
- [ ] Risk factors (features)
  - [ ] Exploratory data analysis (average return, covariance matrices, etc)
  - [ ] We have 10 (FF5 + MOM + HXZ) factors so far, add 3-5 more candidates
  - [ ] Select 4-6 relevant risk factors for our models.
  - [x] Note that risk factors should NOT depend on individual stocks (e.g. do not use PE ratio of individual firm), or we cannot construct risk factors for portfolios.
- [ ] Business cycles
  - [ ] Some EDA (e.g. time series chart of business cycles)
  - [ ] Decide which index to use
  - [ ] Divide business cycles into 4 categories
- [ ] Optimization
- [ ] Model fitting
