# equity-cycle

## Task list

- [ ] Finalize our framework and decide detail approach
- [ ] Send project details (ddl TODAY Sun 02/11)
- [ ] Send weekly slides (ddl Fri 02/16) 
- [ ] Stock data
  - [ ] Acquire stock data and risk factors from bloomberg terminal (all NYSE, AMEX, and NASDAQ firms)
  - [ ] Stock data exploratory data analysis (graphs, summaries, covariance matrices, etc)
  - [ ] Construct portfolios (either do it our self or use portfolios contructed by others, e.g. French's data library)
  - [ ] Construct portfolios to calculate risk factors return that are not in FF5 or HXZ (e.g. liquidity, credit score) 
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
