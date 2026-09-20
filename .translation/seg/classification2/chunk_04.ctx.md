acc_eq_str = r"\mathrm{accuracy} = \frac{\mathrm{number \; of  \; correct  \; predictions}}{\mathrm{total \;  number \;  of  \; predictions}} = \frac{"
acc_eq_str += str(c00) + "+" + str(c11) + "}{" + str(c00) + "+" + str(c11) + "+" + str(c01) + "+" + str(c10) + "} = " + str( np.round(100*(c00+c11)/(c00+c11+c01+c10),2))
acc_eq_math = Math(acc_eq_str)
glue("acc_eq_math_glued", acc_eq_math)

prec_eq_str = r"\mathrm{precision} = \frac{\mathrm{number \; of  \; correct  \; positive \; predictions}}{\mathrm{total \;  number \;  of  \; positive \; predictions}} = \frac{"
prec_eq_str += str(c11) + "}{" + str(c11) + "+" + str(c01) + "} = " + str( np.round(100*c11/(c11+c01), 2))
prec_eq_math = Math(prec_eq_str)
glue("prec_eq_math_glued", prec_eq_math)

rec_eq_str = r"\mathrm{recall} = \frac{\mathrm{number \; of  \; correct  \; positive \; predictions}}{\mathrm{total \;  number \;  of  \; positive \; test \; set \; observations}} = \frac{"
rec_eq_str += str(c11) + "}{" + str(c11) + "+" + str(c10) + "} = " + str( np.round(100*c11/(c11+c10), 2))
rec_eq_math = Math(rec_eq_str)
glue("rec_eq_math_glued", rec_eq_math)
```

```{glue:math} acc_eq_math_glued
```	

```{glue:math} prec_eq_math_glued
```	

```{glue:math} rec_eq_math_glued
```	

