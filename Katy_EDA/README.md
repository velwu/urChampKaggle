Event_1 weighted encoding:
1. First submission- Roughly using total sales (2011-2016, all states, all categories) to add weight.
   outcome Error Score = 6.23
2. Second submission- normalize the encoding as range 0-1, but the outcome is the same.
   There is no need to normalize when using LSTM (and other tree-based) model.
3. Other thoughts: to encode by category or by state.
   But how to make it comparable between different categories/states?
   The basements of each category/each state are different.
   (Ex. Super Bowl of FOODS is given "30", while Purim End of HOBBIES is also given "30". But the sales volume of FOODS is much more larger than that of HOBBIES. The same situation happens between different states- CA > TX & WI.)
