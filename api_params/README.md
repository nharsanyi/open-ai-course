## temperature 
__number or null Optional Defaults to 1__

What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

We generally recommend altering this or top_p but not both.

Better to use value between 0 and 1. 

## top P 
__number or null Optional Defaults to 1__

An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

We generally recommend altering this or temperature but not both.

Alters the creativity and randomness of the output

It controls the set of possible words/tokens that the model can choose from

It restricts the candidate words to the smallest set whose cumulative
probability is greater than or equal to a given threshold "p"

It's setting a sampling window, which dictates which tokens are allowed to choose
and which are not.

## frequency_penalty
__number or null Optional Defaults to 0__
Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood
to repeat the same line verbatim.
If you want to reduce repetitive samples, use 0.1-1
Negative values increase the likelyhood of repetition

## presence_penalty
__number or null Optional Defaults to 0__
Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.

Presence penalty is a one-off additive contribution that applies 
to all tokens that have been sampled at least once
Frequency penalty is a contribution that is proportional to how often a particular
token has already been sampled