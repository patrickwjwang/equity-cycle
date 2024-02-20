# equity-cycle

## Task list

- [x] Finalize our framework and decide detail approach
- [x] Send project details (ddl TODAY Sun 02/11)
- [x] Send weekly slides (ddl Fri 02/16) 
- [ ] Stock data and risk factors
  - [ ] Acquire stock data and risk factors from bloomberg terminal (all NYSE, AMEX, and NASDAQ firms) (Brian)
  - [ ] Divide stock data by factors and calculate the return for the best and worst portfolio in each factor under different cycles (Brian)
  - [ ] Stock data exploratory data analysis (Patrick)
  - [ ] Construct optimal portfolios (Patrick)   
- [ ] Risk factors (features) (Kenny)
  - [ ] Construct portfolios to calculate risk factors return that are not in FF5 or HXZ (e.g. liquidity, credit score) 
  - [ ] Exploratory data analysis (average return, covariance matrices, etc) 
  - [ ] We have 10 (FF5 + MOM + HXZ) factors so far, add 3-5 more candidates
  - [ ] Select 4-6 relevant risk factors for our models.
  - [x] Note that risk factors should NOT depend on individual stocks (e.g. do not use PE ratio of individual firm), or we cannot construct risk factors for portfolios.
- [ ] Business cycles (Yoshi)
  - [ ] Some EDA (e.g. time series chart of business cycles)
  - [ ] Decide which index to use
  - [ ] Divide business cycles into 4 categories
- [ ] Model fitting: Do this after all the above are done, regress "optimal portfolios" on "selected factors"
