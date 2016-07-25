import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

filenames = []
path = "/home/user1/PycharmProjects/genuisify/texts"

for filename in os.listdir(path):
    filenames.append(filename)

print("unsorted")
print(filenames)

filenames_with_path = [os.path.join(path, fn) for fn in filenames]
raw_texts = []

for fn in filenames_with_path:
    with open(fn) as f:
        text = f.read()
        raw_texts.append(text)

vectorizer = CountVectorizer(input='content')
dtm = vectorizer.fit_transform(raw_texts)
vocab = np.array(vectorizer.get_feature_names())
# filoo = open("foo", "a")
# filoo.write(str(vocab))

dtm = dtm.toarray()
rates = np.around(1000 * dtm / np.sum(dtm, axis=1, keepdims=True), 2)

female_indices, male_indices = [], []

for index, fn in enumerate(filenames):
    if "FEMALE" in fn:
        female_indices.append(index)
    elif "MALE" in fn:
        male_indices.append(index)

print("0:" + str(len(female_indices)))
print(str(len(female_indices)) + ":" + str(len(female_indices) + len(male_indices)))

female_rates = rates[female_indices, :]
male_rates = rates[male_indices, :]

female_rates_avg = np.mean(female_rates, axis=0)
male_rates_avg = np.mean(male_rates, axis=0)

distinctive_indices = (female_rates_avg * male_rates_avg) == 0
np.count_nonzero(distinctive_indices)

ranking = np.argsort(female_rates_avg[distinctive_indices] + male_rates_avg[distinctive_indices])[::-1]
dtm = dtm[:, np.invert(distinctive_indices)]

rates = rates[:, np.invert(distinctive_indices)]
vocab = vocab[np.invert(distinctive_indices)]

female_rates = rates[female_indices, :]
male_rates = rates[male_indices, :]
female_rates_avg = np.mean(female_rates, axis=0)
male_rates_avg = np.mean(male_rates, axis=0)

keyness = np.abs(female_rates_avg - male_rates_avg)
ranking = np.argsort(keyness)[::-1]
rates_avg = np.mean(rates, axis=0)
keyness = np.abs(female_rates_avg - male_rates_avg) / rates_avg
ranking = np.argsort(keyness)[::-1]


def sample_posterior(y1, y2, mu0, sigma20, nu0, delta0, gamma20, tau20, S):
    """Draw samples from posterior distribution using Gibbs sampling
            Parameters
            ----------
            `S` is the number of samples
            Returns
            -------
            chains : dict of array
                Dictionary has keys: 'mu', 'delta', and 'sigma2'.
            """
    n1, n2 = len(y1), len(y2)
    mu = (np.mean(y1) + np.mean(y2)) / 2
    delta = (np.mean(y1) - np.mean(y2)) / 2
    vars = ['mu', 'delta', 'sigma2']
    chains = {key: np.empty(S) for key in vars}
    for s in range(S):
        a = (nu0 + n1 + n2) / 2
        b = (nu0 * sigma20 + np.sum((y1 - mu - delta) ** 2) + np.sum((y2 - mu + delta) ** 2)) / 2
        sigma2 = 1 / np.random.gamma(a, 1 / b)
        mu_var = 1 / (1 / gamma20 + (n1 + n2) / sigma2)
        mu_mean = mu_var * (mu0 / gamma20 + np.sum(y1 - delta) / sigma2 +
                            np.sum(y2 + delta) / sigma2)
        mu = np.random.normal(mu_mean, np.sqrt(mu_var))
        delta_var = 1 / (1 / tau20 + (n1 + n2) / sigma2)
        delta_mean = delta_var * (delta0 / tau20 + np.sum(y1 - mu) / sigma2 -
                                  np.sum(y2 - mu) / sigma2)
        delta = np.random.normal(delta_mean, np.sqrt(delta_var))
        chains['mu'][s] = mu
        chains['delta'][s] = delta
        chains['sigma2'][s] = sigma2
    return chains


# prior parameters
mu0 = 3
tau20 = 1.5 ** 2
nu0 = 1
sigma20 = 1
delta0 = 0
gamma20 = 1.5 ** 2
S = 1000


def delta_confidence(rates_one_word):
    female_rates = rates_one_word[0:len(female_indices)]  # obs, data dependent mathaafakkkerz!!
    bronte_rates = rates_one_word[len(female_indices):len(female_indices) + len(male_indices)]

    chains = sample_posterior(female_rates, bronte_rates, mu0, sigma20, nu0,
                              delta0, gamma20, tau20, S)
    delta = chains['delta']
    return np.max([np.mean(delta < 0), np.mean(delta > 0)])


keyness = np.apply_along_axis(delta_confidence, axis=0, arr=rates)
ranking = np.argsort(keyness)[::-1]  # from highest to lowest; [::-1] reverses order.

# print the top 10 words along with their rates and the difference
# THIS INCLUDES SWEDISH STOPWORDS!
# print(repr(vocab[ranking][0:10]))

print(vocab[ranking][0:5])
print(np.round(keyness[ranking][0:5], 2))
