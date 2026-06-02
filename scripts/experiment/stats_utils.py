"""Small, dependency-light statistics helpers (numpy + scipy only)."""
import numpy as np
from scipy import stats


def zscore(x):
    x = np.asarray(x, float)
    return (x - np.nanmean(x)) / np.nanstd(x, ddof=1)


def cronbach_alpha(items):
    items = np.asarray(items, float)
    items = items[~np.isnan(items).any(axis=1)]
    k = items.shape[1]
    item_var = items.var(axis=0, ddof=1).sum()
    total_var = items.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_var / total_var)


def cohen_d(a, b):
    a = np.asarray(a, float); a = a[~np.isnan(a)]
    b = np.asarray(b, float); b = b[~np.isnan(b)]
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    return (a.mean() - b.mean()) / sp


def welch_test(a, b, direction=0):
    """Welch t-test. direction +1/-1 -> one-sided in that direction; 0 -> two-sided."""
    a = np.asarray(a, float); a = a[~np.isnan(a)]
    b = np.asarray(b, float); b = b[~np.isnan(b)]
    t, p_two = stats.ttest_ind(a, b, equal_var=False)
    if direction == 0:
        p = p_two
    else:
        favorable = direction * (a.mean() - b.mean()) > 0
        p = p_two / 2 if favorable else 1 - p_two / 2
    va, vb, na, nb = a.var(ddof=1), b.var(ddof=1), len(a), len(b)
    se = np.sqrt(va / na + vb / nb)
    dfree = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    diff = a.mean() - b.mean()
    tcrit = stats.t.ppf(0.975, dfree)
    return {"diff": diff, "ci_low": diff - tcrit * se, "ci_high": diff + tcrit * se,
            "t": t, "df": dfree, "p": p, "d": cohen_d(a, b)}


def one_way_anova(groups):
    groups = [np.asarray(g, float) for g in groups]
    groups = [g[~np.isnan(g)] for g in groups]
    f, p = stats.f_oneway(*groups)
    grand = np.concatenate(groups).mean()
    ss_b = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
    ss_w = sum(((g - g.mean()) ** 2).sum() for g in groups)
    return {"F": f, "p": p, "eta2_partial": ss_b / (ss_b + ss_w)}


def ols(y, X, names):
    """Ordinary least squares. X must include an intercept column."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    mask = ~np.isnan(y) & ~np.isnan(X).any(axis=1)
    y, X = y[mask], X[mask]
    n, k = X.shape
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = n - k
    cov = (resid @ resid) / dof * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    t = beta / se
    p = 2 * stats.t.sf(np.abs(t), dof)
    return {nm: {"beta": float(b), "se": float(s), "t": float(tt), "p": float(pp)}
            for nm, b, s, tt, pp in zip(names, beta, se, t, p)}


def holm(pvals):
    pvals = np.asarray(pvals, float)
    m = len(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(np.argsort(pvals)):
        running = max(running, (m - rank) * pvals[idx])
        adj[idx] = min(running, 1.0)
    return adj
